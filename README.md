# SDC-36 Agentic AI App
<p align="center">
  <img src="assets/Logo2.jpg" alt="Project Logo" width="200">
</p>

<h1 align="center">Sinai Digital Center — SDC36</h1>
<p align="center">Agentic AI • RAG • Google Cloud • Vertex AI</p>


This is the SDC-36 Agentic AI Application, designed to generate strategic content using Google Vertex AI RAG and OpenAI GPT-5.1.
Please use this link to Run the Project :  https://sdc36-frontend-q3acjiheyq-uc.a.run.app

## 🚀 Live Demo
**Public Endpoint:** https://sdc36-frontend-q3acjiheyq-uc.a.run.app

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
