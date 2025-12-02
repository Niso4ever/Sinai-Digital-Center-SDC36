from typing import List, Optional

import vertexai
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from sqlalchemy import text as sql_text

from app.config import settings
from app.database import engine

class VertexRAG:
    def __init__(self):
        self.embedding_model = None
        self.index_endpoint = None

    def _ensure_embedding_model(self):
        """Lazily load the embedding model and handle missing Vertex init."""
        if self.embedding_model:
            return self.embedding_model

        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        except Exception as e:
            print(f"Error initializing embedding model: {e}")
            self.embedding_model = None

        return self.embedding_model

    def _ensure_index_endpoint(self):
        """Lazily load the Matching Engine endpoint and guard misconfiguration."""
        if self.index_endpoint:
            return self.index_endpoint

        if not settings.INDEX_ENDPOINT_ID:
            print("Warning: VERTEX_INDEX_ENDPOINT_ID not set. RAG will not work.")
            return None

        try:
            aiplatform.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
                index_endpoint_name=settings.INDEX_ENDPOINT_ID
            )
        except Exception as e:
            print(f"Error initializing index endpoint: {e}")
            self.index_endpoint = None

        return self.index_endpoint

    def get_embedding(self, text: str) -> List[float]:
        """Generates embedding for a single text string."""
        res = self.get_batch_embeddings([text])
        return res[0] if res else []

    def get_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts (batching)."""
        model = self._ensure_embedding_model()
        if not model:
            return []

        # Simple retry with backoff
        import time
        for attempt in range(6):
            try:
                # Vertex AI TextEmbeddingModel supports batching (up to 5 or 250 depending on model)
                # We will assume the caller handles the batch size (e.g. 5)
                embeddings = model.get_embeddings(texts)
                return [e.values for e in embeddings]
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota" in error_str or "ResourceExhausted" in error_str:
                    wait = (2 ** attempt) * 5
                    print(f"⚠️ Quota exceeded. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"Error getting embedding: {e}")
                    return []
        return []

    def _fetch_text_from_db(self, ids: List[str]) -> List[str]:
        """Fetches text content for the given IDs from Cloud SQL."""
        if not engine or not ids:
            return []
        
        try:
            with engine.connect() as conn:
                # Use a parameterized query with IN clause
                query = sql_text("SELECT content FROM document_chunks WHERE id IN :ids")
                result = conn.execute(query, {"ids": tuple(ids)})
                return [row[0] for row in result]
        except Exception as e:
            print(f"Error fetching text from DB: {e}")
            return []

    def search(self, query: str, num_neighbors: int = 5) -> List[str]:
        """
        Searches the Vector DB for relevant context.
        Returns a list of text chunks.
        """
        # 1. Generate embedding for query
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []

        # 2. Search Index
        index_endpoint = self._ensure_index_endpoint()
        if not index_endpoint:
            return []

        try:
            response = index_endpoint.find_neighbors(
                deployed_index_id=settings.DEPLOYED_INDEX_ID,
                queries=[query_embedding],
                num_neighbors=num_neighbors
            )
            
            # Extract neighbors
            if response and response[0]:
                ids = [neighbor.id for neighbor in response[0]]
                print(f"RAG found IDs: {ids}")
                
                # 3. Fetch Text from DB
                texts = self._fetch_text_from_db(ids)
                if not texts:
                    print("Warning: Found IDs but no text in DB. Did you run ingestion?")
                    return ids # Fallback to IDs if DB empty (better than nothing, but still bad)
                
                return texts
            
            return []
        except Exception as e:
            print(f"Error searching index: {e}")
            return []

vertex_rag = VertexRAG()
