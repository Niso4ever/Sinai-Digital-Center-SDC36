import os
import json
import glob
import time
from typing import List
from pypdf import PdfReader
from google.cloud import storage
from sqlalchemy import text as sql_text
from app.config import settings
from app.rag_vertex import vertex_rag
from app.database import engine

class PDFIngestor:
    def __init__(self):
        self.storage_client = storage.Client(project=settings.PROJECT_ID)
        self.bucket_name = settings.GCS_BUCKET_NAME
        self.source_dir = "data/raw_pdfs"
        self.output_dir = "data/index-source"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Ensure DB table exists
        self._init_db()

    def _init_db(self):
        if not engine:
            print("Warning: Database engine not configured. Text storage will fail.")
            return
        
        with engine.connect() as conn:
            conn.execute(sql_text("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id TEXT PRIMARY KEY,
                    content TEXT,
                    source TEXT
                )
            """))
            conn.commit()
            print("✅ Ensured 'document_chunks' table exists.")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ""

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Simple text chunking."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def store_chunks_in_db(self, ids: List[str], chunks: List[str], source: str):
        """Stores text chunks in Cloud SQL."""
        if not engine:
            return
            
        with engine.connect() as conn:
            for i, chunk_id in enumerate(ids):
                # Upsert (Insert or Update)
                conn.execute(sql_text("""
                    INSERT INTO document_chunks (id, content, source)
                    VALUES (:id, :content, :source)
                    ON CONFLICT (id) DO UPDATE SET content = :content
                """), {"id": chunk_id, "content": chunks[i], "source": source})
            conn.commit()

    def process_all(self):
        """Processes all PDFs in the source directory."""
        pdf_files = glob.glob(os.path.join(self.source_dir, "*.pdf"))
        if not pdf_files:
            print(f"No PDFs found in {self.source_dir}")
            return

        output_file = os.path.join(self.output_dir, "embeddings.json")
        
        with open(output_file, "w") as f:
            for pdf_path in pdf_files:
                print(f"Processing {pdf_path}...")
                text = self.extract_text_from_pdf(pdf_path)
                if not text:
                    continue
                
                chunks = self.chunk_text(text)
                filename = os.path.basename(pdf_path)
                
                # Process in batches of 5
                batch_size = 5
                for i in range(0, len(chunks), batch_size):
                    batch_chunks = chunks[i : i + batch_size]
                    batch_ids = [f"{filename}_{j}" for j in range(i, i + len(batch_chunks))]
                    
                    # Rate limiting
                    time.sleep(1)

                    # Generate Embeddings (Batch)
                    embeddings = vertex_rag.get_batch_embeddings(batch_chunks)
                    
                    if not embeddings:
                        print(f"  Skipping batch starting at {i} due to error.")
                        continue

                    # 1. Write to JSONL for Vector Search
                    for j, embedding in enumerate(embeddings):
                        chunk_id = batch_ids[j]
                        record = {
                            "id": chunk_id,
                            "embedding": embedding,
                        }
                        f.write(json.dumps(record) + "\n")
                    
                    # 2. Store Text in DB
                    self.store_chunks_in_db(batch_ids, batch_chunks, filename)
                    
                    print(f"  Processed chunks {i} to {i + len(batch_chunks) - 1}")

        print(f"✅ Generated embeddings in {output_file}")
        print(f"✅ Stored text chunks in Cloud SQL")
        
    def upload_to_gcs(self):
        """Uploads the generated JSONL to GCS."""
        local_file = os.path.join(self.output_dir, "embeddings.json")
        if not os.path.exists(local_file):
            print("No embeddings file to upload.")
            return

        blob_name = "index-source/embeddings.json"
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file)
        print(f"🚀 Uploaded {local_file} to gs://{self.bucket_name}/{blob_name}")

if __name__ == "__main__":
    ingestor = PDFIngestor()
    ingestor.process_all()
    ingestor.upload_to_gcs()
