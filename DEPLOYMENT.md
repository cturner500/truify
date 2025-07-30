# Truify Container Deployment Guide

## Overview
This guide explains how to deploy Truify as a Docker container with automatic startup of both the Streamlit app and SMTP server.

## Quick Start

### 1. Build and Run with Docker Compose
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 2. Build and Run with Docker
```bash
# Build the image
docker build -t truify .

# Run the container
docker run -d \
  -p 8501:8501 \
  -e GMAIL_USER=your_email@truify.ai \
  -e GMAIL_APP_PASSWORD=your_app_password \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/email.csv:/app/email.csv \
  -v $(pwd)/users.csv:/app/users.csv \
  --name truify-app \
  truify
```

## Container Architecture

### Single-Process Container
The container runs one process:
1. **Streamlit App** (port 8501) - Main web application with Gmail SMTP integration

### Process Management
- **Direct Streamlit process** - Simple and efficient
- **Auto-restart** on failure (handled by Docker)
- **Gmail SMTP** - External email service (no local SMTP needed)

## Environment Variables

### Required
- `GMAIL_USER` - Your Gmail/Google Workspace email
- `GMAIL_APP_PASSWORD` - Gmail App Password

### Optional
- `STREAMLIT_SERVER_PORT` - Streamlit port (default: 8501)

## Production Recommendations

### Option 1: Use External Email Service (Recommended)
Replace local SMTP with:
- **SendGrid** (free tier: 100 emails/day)
- **Mailgun** (free tier: 5,000 emails/month)
- **AWS SES** (very cheap)
- **Gmail SMTP** (current setup)

### Option 2: Use External Email Service
```yaml
# docker-compose.yml for production
version: '3.8'

services:
  truify-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GMAIL_USER=${GMAIL_USER}
      - GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}
    volumes:
      - ./data:/app/data
      - ./email.csv:/app/email.csv
      - ./users.csv:/app/users.csv
    restart: unless-stopped
```

## Deployment Platforms

### Docker Hub
```bash
# Tag and push
docker tag truify your-username/truify:latest
docker push your-username/truify:latest
```

### AWS ECS
```bash
# Create ECR repository
aws ecr create-repository --repository-name truify

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag truify:latest your-account.dkr.ecr.us-east-1.amazonaws.com/truify:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/truify:latest
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/truify
gcloud run deploy truify --image gcr.io/your-project/truify --platform managed
```

## Monitoring and Logs

### View Logs
```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f
```

### Health Checks
```bash
# Check if container is running
docker ps

# Check Streamlit logs
docker logs truify-app
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **Secrets Management**: Use Docker secrets or external secret managers
3. **Network Security**: Only expose necessary ports
4. **Image Security**: Use official base images and scan for vulnerabilities

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check if port is available
netstat -tulpn | grep :8501
```

### Email Not Working
1. Verify Gmail credentials are set
2. Check SMTP server logs
3. Test with external SMTP service

### Performance Issues
1. Monitor resource usage: `docker stats`
2. Scale horizontally with multiple containers
3. Use external databases for session storage 