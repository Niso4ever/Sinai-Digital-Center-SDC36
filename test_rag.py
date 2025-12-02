import os
import sys

# Add the current directory to sys.path so we can import app modules
sys.path.append(os.getcwd())

from app.rag_vertex import vertex_rag
from app.config import settings

def test_rag():
    print(f"Testing RAG with:")
    print(f"  Project: {settings.PROJECT_ID}")
    print(f"  Endpoint ID: {settings.INDEX_ENDPOINT_ID}")
    print(f"  Deployed Index ID: {settings.DEPLOYED_INDEX_ID}")
    
    query = "Solar energy in Egypt"
    print(f"\n🔍 Searching for: '{query}'...")
    
    try:
        results = vertex_rag.search(query, num_neighbors=1)
        print(f"\n✅ Success! Found {len(results)} results.")
        print(f"Result IDs: {results}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible causes:")
        print("1. VERTEX_INDEX_ENDPOINT_ID is incorrect (it should NOT be the same as the Index ID).")
        print("2. The Index is not fully deployed yet.")
        print("3. Authentication issues (try 'gcloud auth login' and 'gcloud auth application-default login').")

if __name__ == "__main__":
    test_rag()
