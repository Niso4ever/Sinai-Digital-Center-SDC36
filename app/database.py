import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Prefer a full connection string from Secret Manager when available.
DATABASE_URL = os.getenv("DB_CONNECTION_STRING")

if not DATABASE_URL:
    # Construct DATABASE_URL from individual parts
    if settings.DB_HOST and settings.DB_HOST.startswith("/cloudsql"):
        DATABASE_URL = (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@/{settings.DB_NAME}?host={settings.DB_HOST}"
        )
    else:
        DATABASE_URL = (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )

# Handle case where password/host/connection string might be missing (e.g. during build)
if not DATABASE_URL or "None" in DATABASE_URL:
    print("Warning: Database credentials not set. Database connection will fail.")
    engine = None
    SessionLocal = None
else:
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        print(f"Error creating database engine: {e}")
        engine = None
        SessionLocal = None


def get_db():
    if SessionLocal is None:
        raise Exception("Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
