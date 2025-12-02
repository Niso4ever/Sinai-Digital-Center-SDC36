#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
DB_INSTANCE_NAME="sdc36-db"
DB_NAME="sdc36"
DB_USER="sdc36-user"
SECRET_NAME="sdc36-db-credentials"

echo "Setting up infrastructure for Project: $PROJECT_ID in Region: $REGION"

# 1. Enable APIs
echo "Enabling APIs..."
gcloud services enable \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    compute.googleapis.com

# 2. Secret Manager
echo "Setting up Secrets..."
if ! gcloud secrets describe $SECRET_NAME --project=$PROJECT_ID &>/dev/null; then
    gcloud secrets create $SECRET_NAME --replication-policy="automatic" --project=$PROJECT_ID
    # Initial dummy value, will be updated
    echo "dummy" | gcloud secrets versions add $SECRET_NAME --data-file=-
else
    echo "Secret $SECRET_NAME already exists."
fi

# 3. Cloud SQL (Public IP)
echo "Setting up Cloud SQL (Public IP)..."
if ! gcloud sql instances describe $DB_INSTANCE_NAME --project=$PROJECT_ID &>/dev/null; then
    # Create Instance with Public IP (default behavior when no --no-assign-ip is specified)
    # We remove --network and --no-assign-ip
    gcloud sql instances create $DB_INSTANCE_NAME \
        --database-version=POSTGRES_15 \
        --cpu=1 \
        --memory=3840MiB \
        --region=$REGION \
        --project=$PROJECT_ID
        
    # Create Database
    gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE_NAME --project=$PROJECT_ID

    # Create User & Password
    TEMP_PASSWORD=$(openssl rand -base64 16)
    gcloud sql users create $DB_USER --instance=$DB_INSTANCE_NAME --password=$TEMP_PASSWORD --project=$PROJECT_ID
    
    # Update Secret with connection string
    # For Cloud Run with Public IP/Auth Proxy, we usually use Unix Socket
    # Connection Name: PROJECT:REGION:INSTANCE
    INSTANCE_CONNECTION_NAME="$PROJECT_ID:$REGION:$DB_INSTANCE_NAME"
    
    # We store the password separately or the full URL. Let's store the full URL for simplicity in the app.
    # Format for Unix Socket: postgresql://USER:PASSWORD@/DB_NAME?host=/cloudsql/INSTANCE_CONNECTION_NAME
    echo -n "postgresql://$DB_USER:$TEMP_PASSWORD@/$DB_NAME?host=/cloudsql/$INSTANCE_CONNECTION_NAME" | \
        gcloud secrets versions add $SECRET_NAME --data-file=-
else
    echo "Cloud SQL Instance $DB_INSTANCE_NAME already exists."
    # If it exists, ensure it has Public IP enabled?
    # gcloud sql instances patch $DB_INSTANCE_NAME --assign-ip
fi

echo "Infrastructure setup complete."
