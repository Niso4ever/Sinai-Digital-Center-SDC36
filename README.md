# SDC-36 Agentic AI App

This is the SDC-36 Agentic AI Application, designed to generate strategic content using Google Vertex AI RAG and OpenAI GPT-5.1.
 https://sdc36-frontend-q3acjiheyq-uc.a.run.app

## Architecture

PDFs -> GCS Bucket -> Vertex Embeddings -> Vertex Matching Engine
                               |
                         RAG Retriever
                               |
          User -> Antigravity UI -> FastAPI (Cloud Run)
                               |
                       GPT-5.1 Agentic Controller
                               |
                     Tools -> Final Output -> UI

## Setup

1.  **Environment Variables**: Copy `.env.example` to `.env` and fill in the values.
2.  **Install Dependencies**: `pip install -r requirements.txt`
3.  **Run Locally**: `uvicorn app.main:app --reload`
4.  **Run Frontend**: `streamlit run frontend/streamlit_app.py`

## Deployment

Deploy to Google Cloud Run using the provided scripts.
