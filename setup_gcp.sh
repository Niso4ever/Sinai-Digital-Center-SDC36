#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting SDC-36 Google Cloud Setup..."

# 1. Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI could not be found. Please install it first."
    exit 1
fi

# 2. Login check
echo "Checking authentication..."
gcloud auth print-access-token >/dev/null 2>&1 || { echo "Please run 'gcloud auth login' first"; exit 1; }

# 3. Project Setup
PROJECT_ID=$(gcloud config get-value project)
echo "✅ Project set to $PROJECT_ID"

# 4. Enable APIs
echo "Enable APIs (Vertex AI, Cloud Run, Cloud Build, Storage)..."
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    storage.googleapis.com \
    secretmanager.googleapis.com
echo "✅ APIs enabled"

# 5. Create GCS Bucket
BUCKET_NAME="${PROJECT_ID}-sdc36-data"
echo "Creating GCS Bucket: gs://$BUCKET_NAME ..."
if gsutil ls -b gs://$BUCKET_NAME >/dev/null 2>&1; then
    echo "✅ Bucket already exists"
else
    gsutil mb -l us-central1 gs://$BUCKET_NAME
    echo "✅ Bucket created"
fi

# 6. .env file
echo "ℹ️  Skipping .env file creation as it should already exist."

echo "🎉 Setup Complete! Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run ./deploy.sh to deploy to Cloud Run"
