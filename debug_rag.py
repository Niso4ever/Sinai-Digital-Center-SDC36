import os
from sqlalchemy import text as sql_text
from app.database import engine
from app.rag_vertex import vertex_rag

def check_db():
    print("--- Checking Database ---")
    if not engine:
        print("❌ Database engine not configured.")
        return

    try:
        with engine.connect() as conn:
            result = conn.execute(sql_text("SELECT COUNT(*) FROM document_chunks"))
            count = result.scalar()
            print(f"✅ 'document_chunks' row count: {count}")
            
            if count > 0:
                sample = conn.execute(sql_text("SELECT id, content FROM document_chunks LIMIT 1")).fetchone()
                print(f"   Sample ID: {sample[0]}")
                print(f"   Sample Content Preview: {sample[1][:50]}...")
    except Exception as e:
        print(f"❌ Error checking DB: {e}")

def test_rag(query):
    print(f"\n--- Testing RAG for query: '{query}' ---")
    try:
        results = vertex_rag.search(query, num_neighbors=3)
        print(f"Found {len(results)} chunks.")
        for i, chunk in enumerate(results):
            print(f"Chunk {i+1}: {chunk[:100]}...")
    except Exception as e:
        print(f"❌ Error testing RAG: {e}")

if __name__ == "__main__":
    check_db()
    test_rag("What's Nimbos Project?")
