import sys
import os
from sqlalchemy import text as sql_text

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.database import engine

def audit_db():
    if not engine:
        print("❌ Database engine not configured.")
        return

    print("--- Auditing Knowledge Base (Cloud SQL) ---")
    try:
        with engine.connect() as conn:
            # Count total chunks
            result = conn.execute(sql_text("SELECT COUNT(*) FROM document_chunks"))
            count = result.scalar()
            print(f"Total Chunks: {count}")

            # List unique sources (files) and their chunk counts
            print("\n--- Files in Database ---")
            result = conn.execute(sql_text("SELECT source, COUNT(*) FROM document_chunks GROUP BY source"))
            rows = result.fetchall()
            if not rows:
                print("No files found in database.")
            else:
                for row in rows:
                    print(f"📄 {row[0]}: {row[1]} chunks")

    except Exception as e:
        print(f"❌ Error querying database: {e}")

if __name__ == "__main__":
    audit_db()
