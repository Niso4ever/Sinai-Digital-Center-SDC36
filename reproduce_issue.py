import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.rag_vertex import vertex_rag
from app.config import settings

def test_rag():
    print(f"DEBUG: settings.PROJECT_ID = {settings.PROJECT_ID}")
    query = "Why 36?"
    print(f"Testing RAG with query: '{query}'")
    
    # 1. Test Embedding
    print("\n--- Testing Embedding ---")
    embedding = vertex_rag.get_embedding(query)
    if not embedding:
        print("❌ Failed to get embedding.")
        return
    print(f"✅ Got embedding (length: {len(embedding)})")

    # 2. Test Search
    print("\n--- Testing Search ---")
    results = vertex_rag.search(query)
    
    if not results:
        print("❌ Search returned no results.")
    else:
        print(f"✅ Search returned {len(results)} results.")
        print("First result preview:", results[0][:100])
        
        # Check if we got IDs or actual text
        if "Gemini.pdf" in results[0] or "gpt.pdf" in results[0]:
             print("⚠️ Warning: Results look like IDs, not text content. DB lookup might have failed.")
        else:
             print("✅ Results look like text content.")

if __name__ == "__main__":
    test_rag()
