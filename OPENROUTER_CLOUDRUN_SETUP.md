# OpenRouter Cloud Run Deployment with Email Alerts

This guide explains how to deploy the Truify OpenRouter version to Google Cloud Run with email alert functionality.

## Prerequisites

1. **Google Cloud Project** with Cloud Run enabled
2. **Gmail App Password** for sending email alerts
3. **OpenRouter API Key** for AI functionality
4. **Docker** installed locally

## Setup Steps

### 1. Set Environment Variables

```bash
# Set your Gmail credentials
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"

# Set your OpenRouter API key
export OPENROUTER_API_KEY="your-openrouter-api-key"

# Set your Google Cloud project ID
export PROJECT_ID="your-project-id"
```

### 2. Create Gmail Secret (Optional - for production)

```bash
# Create secret for Gmail user
echo -n "$GMAIL_USER" | gcloud secrets create gmail-secret --data-file=-

# Create secret for Gmail password
echo -n "$GMAIL_APP_PASSWORD" | gcloud secrets create gmail-password --data-file=-

# Create secret for OpenRouter API key
echo -n "$OPENROUTER_API_KEY" | gcloud secrets create openrouter-secret --data-file=-
```

### 3. Deploy Using Script

```bash
# Deploy with environment variables
./deploy-cloudrun-openrouter.sh

# Or specify custom parameters
./deploy-cloudrun-openrouter.sh PROJECT_ID SERVICE_NAME REGION
```

### 4. Deploy Using YAML (Alternative)

```bash
# Update PROJECT_ID in cloudrun-openrouter.yaml
# Then deploy using gcloud
gcloud run services replace cloudrun-openrouter.yaml
```

## What This Fixes

- ✅ **Email alerts work** in Cloud Run container
- ✅ **Gmail credentials** properly configured
- ✅ **OpenRouter API key** available for AI features
- ✅ **Consistent deployment** process

## Verification

After deployment, test that:
1. **App loads** correctly in Cloud Run
2. **Login triggers** email alert to ava@truify.ai
3. **AI features work** (PII analysis, compliance reports)
4. **No package errors** during container startup

## Troubleshooting

### Email Not Working
- Check Gmail environment variables are set
- Verify Gmail App Password is correct
- Check Cloud Run logs for email errors

### AI Features Not Working
- Verify OPENROUTER_API_KEY is set
- Check OpenRouter API quota/limits
- Review Cloud Run logs for API errors

### Container Build Issues
- Ensure Dockerfile.openrouter builds locally first
- Check all required packages install correctly
- Verify base image compatibility
