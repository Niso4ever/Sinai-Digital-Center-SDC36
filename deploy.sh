#!/bin/bash
set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
REPO_NAME="sdc36-repo"
BACKEND_SERVICE="sdc36-backend"
FRONTEND_SERVICE="sdc36-frontend"
DB_INSTANCE_NAME="sdc36-db"
SECRET_NAME="sdc36-db-credentials"

INSTANCE_CONNECTION_NAME="$PROJECT_ID:$REGION:$DB_INSTANCE_NAME"

echo "Deploying to Project: $PROJECT_ID in Region: $REGION"

# Create Artifact Registry Repo if not exists
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION --project=$PROJECT_ID &>/dev/null; then
    gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="SDC-36 Repository" --project=$PROJECT_ID
fi

# 1. Deploy Backend
echo "Building and Deploying Backend..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$BACKEND_SERVICE .

gcloud run deploy $BACKEND_SERVICE \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$BACKEND_SERVICE \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --add-cloudsql-instances $INSTANCE_CONNECTION_NAME \
    --set-env-vars="DB_USER=sdc36-user,DB_NAME=sdc36,DB_HOST=/cloudsql/$INSTANCE_CONNECTION_NAME,DB_PASSWORD=$(grep DB_PASSWORD .env | sed 's/^DB_PASSWORD=//'),OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | sed 's/^OPENAI_API_KEY=//'),GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION,GCS_BUCKET_NAME=${PROJECT_ID}-sdc36-data,VERTEX_INDEX_ENDPOINT_ID=$(grep VERTEX_INDEX_ENDPOINT_ID .env | sed 's/^VERTEX_INDEX_ENDPOINT_ID=//'),VERTEX_DEPLOYED_INDEX_ID=$(grep VERTEX_DEPLOYED_INDEX_ID .env | sed 's/^VERTEX_DEPLOYED_INDEX_ID=//')"

# Get Backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region $REGION --format 'value(status.url)' --project=$PROJECT_ID)
echo "Backend URL: $BACKEND_URL"

# 2. Deploy Frontend
echo "Building and Deploying Frontend..."
gcloud builds submit --config cloudbuild_frontend.yaml --substitutions=_IMAGE_NAME=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$FRONTEND_SERVICE .

gcloud run deploy $FRONTEND_SERVICE \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$FRONTEND_SERVICE \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --set-env-vars="API_URL=$BACKEND_URL/api/v1/generate"

echo "Deployment Complete."
echo "Frontend URL: $(gcloud run services describe $FRONTEND_SERVICE --region $REGION --format 'value(status.url)' --project=$PROJECT_ID)"
