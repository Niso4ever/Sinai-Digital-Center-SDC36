import os
from dotenv import load_dotenv

# Ensure .env values override existing environment variables
load_dotenv(override=True)

class Config:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    
    # Vertex AI Vector Search
    INDEX_ENDPOINT_ID = os.getenv("VERTEX_INDEX_ENDPOINT_ID")
    DEPLOYED_INDEX_ID = os.getenv("VERTEX_DEPLOYED_INDEX_ID")

    # Database
    DB_USER = os.getenv("DB_USER", "sdc36-user")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "sdc36")
    DB_HOST = os.getenv("DB_HOST") # Private IP or localhost
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o") # Default to 4o until 5.1 is public/confirmed
    
    # App
    API_V1_STR = "/api/v1"

settings = Config()
