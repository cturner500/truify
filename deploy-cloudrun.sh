#!/bin/bash

# Cloud Run deployment script for Truify GPU
set -e

PROJECT_ID=${1:-$(gcloud config get-value project)}
SERVICE_NAME=${2:-truify-gpu}
REGION=${3:-us-central1}
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying Truify GPU to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"

# Build the GPU image
echo "Building GPU Docker image..."
docker build -f Dockerfile.gpu -t $IMAGE_NAME .

# Push to Google Container Registry
echo "Pushing image to GCR..."
docker push $IMAGE_NAME

# Deploy to Cloud Run with GPU
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 16Gi \
  --cpu 4 \
  --concurrency 1 \
  --timeout 3600 \
  --set-env-vars "GMAIL_USER=$GMAIL_USER,GMAIL_APP_PASSWORD=$GMAIL_APP_PASSWORD" \
  --port 8501

echo "Deployment complete!"
echo "Service URL: https://$SERVICE_NAME-$REGION-$PROJECT_ID.a.run.app"
echo ""
echo "Note: Cloud Run with GPU requires manual configuration:"
echo "1. Enable GPU in Cloud Run console"
echo "2. Set GPU allocation in service configuration"
echo "3. Ensure NVIDIA runtime is available in your region"
