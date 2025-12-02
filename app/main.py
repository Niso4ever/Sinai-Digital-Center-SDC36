from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
# from app.agentic_engine import agentic_engine # Will be implemented later

app = FastAPI(title="SDC-36 Agentic AI App")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SDC-36 Agentic AI App is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/db")
def health_check_db():
    from app.database import engine, text
    if engine is None:
        return {"status": "error", "message": "Database not configured"}
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {"status": "healthy", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Placeholder for agent endpoint
from app.agentic_engine import agentic_engine, GenerationRequest
from fastapi import BackgroundTasks
from app.pdf_ingest_vertex import PDFIngestor
from app.database import engine, text

@app.post("/api/v1/generate")
async def generate_content(request: GenerationRequest):
    return agentic_engine.process(request)

@app.get("/api/v1/audit")
def audit_knowledge_base():
    """Returns a list of ingested files and their chunk counts."""
    if engine is None:
        return {"status": "error", "message": "Database not configured"}
    
    try:
        with engine.connect() as connection:
            # Count total chunks
            total_chunks = connection.execute(text("SELECT COUNT(*) FROM document_chunks")).scalar()
            
            # Group by source
            result = connection.execute(text("SELECT source, COUNT(*) FROM document_chunks GROUP BY source"))
            files = [{"filename": row[0], "chunks": row[1]} for row in result.fetchall()]
            
            return {
                "status": "success",
                "total_chunks": total_chunks,
                "files": files
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run_ingestion():
    """Background task to run ingestion."""
    try:
        print("🚀 Starting background ingestion...")
        ingestor = PDFIngestor()
        ingestor.process_all()
        ingestor.upload_to_gcs()
        print("✅ Background ingestion complete.")
    except Exception as e:
        print(f"❌ Background ingestion failed: {e}")

@app.post("/api/v1/ingest")
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """Triggers the ingestion process in the background."""
    background_tasks.add_task(run_ingestion)
    return {"status": "accepted", "message": "Ingestion started in background. Check logs for progress."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
