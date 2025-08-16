#!/bin/bash

# Cloud Run deployment script for Truify OpenRouter
set -e

PROJECT_ID=${1:-$(gcloud config get-value project)}
SERVICE_NAME=${2:-truify-openrouter}
REGION=${3:-us-central1}
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying Truify OpenRouter to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"

# Check if Gmail environment variables are set
if [ -z "$GMAIL_USER" ] || [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "Error: Gmail environment variables not set!"
    echo "Please set:"
    echo "export GMAIL_USER=your-email@gmail.com"
    echo "export GMAIL_APP_PASSWORD=your-app-password"
    exit 1
fi

# Build the OpenRouter image
echo "Building OpenRouter Docker image..."
docker build -f Dockerfile.openrouter -t $IMAGE_NAME .

# Push to Google Container Registry
echo "Pushing image to GCR..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 8Gi \
  --cpu 2 \
  --concurrency 1 \
  --timeout 3600 \
  --set-env-vars "GMAIL_USER=$GMAIL_USER,GMAIL_APP_PASSWORD=$GMAIL_APP_PASSWORD,OPENROUTER_API_KEY=$OPENROUTER_API_KEY" \
  --port 8501

echo "Deployment complete!"
echo "Service URL: https://$SERVICE_NAME-$REGION-$PROJECT_ID.a.run.app"
echo ""
echo "Note: Make sure you have set the required environment variables:"
echo "- GMAIL_USER: $GMAIL_USER"
echo "- GMAIL_APP_PASSWORD: [set]"
echo "- OPENROUTER_API_KEY: [set]"
