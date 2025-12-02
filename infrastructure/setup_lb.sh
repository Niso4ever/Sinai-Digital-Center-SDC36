#!/bin/bash
set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
BACKEND_SERVICE_NAME="sdc36-backend"
FRONTEND_SERVICE_NAME="sdc36-frontend"

# LB Resources Names
IP_NAME="sdc36-global-ip"
BACKEND_NEG="sdc36-backend-neg"
FRONTEND_NEG="sdc36-frontend-neg"
BACKEND_BS="sdc36-backend-bs"
FRONTEND_BS="sdc36-frontend-bs"
URL_MAP="sdc36-url-map"
PROXY_NAME="sdc36-http-proxy"
FWD_RULE="sdc36-fwd-rule"

echo "Setting up Global Load Balancer..."

# 1. Reserve Global IP
if ! gcloud compute addresses describe $IP_NAME --global --project=$PROJECT_ID &>/dev/null; then
    gcloud compute addresses create $IP_NAME --global --project=$PROJECT_ID
fi
IP_ADDRESS=$(gcloud compute addresses describe $IP_NAME --global --format="value(address)" --project=$PROJECT_ID)
echo "Global IP: $IP_ADDRESS"

# 2. Create Serverless NEGs
if ! gcloud compute network-endpoint-groups describe $BACKEND_NEG --region=$REGION --project=$PROJECT_ID &>/dev/null; then
    gcloud compute network-endpoint-groups create $BACKEND_NEG \
        --region=$REGION \
        --network-endpoint-type=SERVERLESS \
        --cloud-run-service=$BACKEND_SERVICE_NAME \
        --project=$PROJECT_ID
fi

if ! gcloud compute network-endpoint-groups describe $FRONTEND_NEG --region=$REGION --project=$PROJECT_ID &>/dev/null; then
    gcloud compute network-endpoint-groups create $FRONTEND_NEG \
        --region=$REGION \
        --network-endpoint-type=SERVERLESS \
        --cloud-run-service=$FRONTEND_SERVICE_NAME \
        --project=$PROJECT_ID
fi

# 3. Create Backend Services
if ! gcloud compute backend-services describe $BACKEND_BS --global --project=$PROJECT_ID &>/dev/null; then
    gcloud compute backend-services create $BACKEND_BS --global --project=$PROJECT_ID
    gcloud compute backend-services add-backend $BACKEND_BS \
        --global \
        --network-endpoint-group=$BACKEND_NEG \
        --network-endpoint-group-region=$REGION \
        --project=$PROJECT_ID
fi

if ! gcloud compute backend-services describe $FRONTEND_BS --global --project=$PROJECT_ID &>/dev/null; then
    gcloud compute backend-services create $FRONTEND_BS --global --project=$PROJECT_ID
    gcloud compute backend-services add-backend $FRONTEND_BS \
        --global \
        --network-endpoint-group=$FRONTEND_NEG \
        --network-endpoint-group-region=$REGION \
        --project=$PROJECT_ID
fi

# 4. Create URL Map
# Route /api/* to backend, everything else to frontend
if ! gcloud compute url-maps describe $URL_MAP --project=$PROJECT_ID &>/dev/null; then
    gcloud compute url-maps create $URL_MAP \
        --default-service $FRONTEND_BS \
        --project=$PROJECT_ID
    
    gcloud compute url-maps add-path-matcher $URL_MAP \
        --path-matcher-name="api-paths" \
        --default-service=$FRONTEND_BS \
        --path-rules="/api/*=$BACKEND_BS" \
        --project=$PROJECT_ID
fi

# 5. Create Target HTTP Proxy
if ! gcloud compute target-http-proxies describe $PROXY_NAME --project=$PROJECT_ID &>/dev/null; then
    gcloud compute target-http-proxies create $PROXY_NAME \
        --url-map=$URL_MAP \
        --project=$PROJECT_ID
fi

# 6. Create Global Forwarding Rule
if ! gcloud compute forwarding-rules describe $FWD_RULE --global --project=$PROJECT_ID &>/dev/null; then
    gcloud compute forwarding-rules create $FWD_RULE \
        --global \
        --target-http-proxy=$PROXY_NAME \
        --ports=80 \
        --address=$IP_NAME \
        --project=$PROJECT_ID
fi

echo "Load Balancer Setup Complete."
echo "Wait a few minutes for the LB to provision."
echo "Access your app at: http://$IP_ADDRESS"
