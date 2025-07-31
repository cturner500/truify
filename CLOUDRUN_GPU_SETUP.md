# Google Cloud Run GPU Setup for Truify

This guide explains how to deploy Truify with GPU acceleration on Google Cloud Run.

## Prerequisites

### 1. Google Cloud Project Setup
```bash
# Set your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable compute.googleapis.com
```

### 2. GPU Quotas
- Request GPU quota for your region
- Ensure T4 or V100 GPU availability
- Minimum 16GB memory recommended

## Automated Deployment

### Option 1: Using Deployment Script
```bash
# Set environment variables
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"

# Deploy to Cloud Run
./deploy-cloudrun.sh [PROJECT_ID] [SERVICE_NAME] [REGION]
```

### Option 2: Manual Deployment
```bash
# Build and push image
docker build -f Dockerfile.gpu -t gcr.io/$PROJECT_ID/truify-gpu .
docker push gcr.io/$PROJECT_ID/truify-gpu

# Deploy to Cloud Run
gcloud run deploy truify-gpu \
  --image gcr.io/$PROJECT_ID/truify-gpu \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 16Gi \
  --cpu 4 \
  --concurrency 1 \
  --timeout 3600 \
  --set-env-vars "GMAIL_USER=$GMAIL_USER,GMAIL_APP_PASSWORD=$GMAIL_APP_PASSWORD"
```

## Cloud Run Configuration

### GPU Allocation
Cloud Run with GPU requires:
- **Memory**: 16GB minimum
- **CPU**: 4 cores minimum
- **GPU**: 1 T4 or V100 GPU
- **Timeout**: 3600 seconds (1 hour)

### Environment Variables
```yaml
CUDA_VISIBLE_DEVICES: "0"
NVIDIA_VISIBLE_DEVICES: "all"
GMAIL_USER: "your-email@gmail.com"
GMAIL_APP_PASSWORD: "your-app-password"
```

## Dockerfile.gpu Features

### NVIDIA Software Installation
The updated Dockerfile.gpu automatically installs:
- NVIDIA Container Toolkit
- NVIDIA Container Runtime
- CUDA 12.1 development tools
- NVIDIA drivers (downloaded during build)

### Build Process
1. **Base Image**: `nvidia/cuda:12.1-devel-ubuntu22.04`
2. **System Dependencies**: build-essential, cmake, git, wget, curl
3. **NVIDIA Tools**: Container toolkit and runtime
4. **Python Dependencies**: GPU-enabled PyTorch and other packages
5. **Model Download**: Mistral models during build
6. **Startup Script**: GPU detection and logging

### Key Improvements
- **Automated NVIDIA setup**: No manual installation required
- **Cloud Run optimized**: Proper port configuration (8501)
- **GPU detection**: Startup script checks GPU availability
- **Error handling**: Graceful fallback to CPU if GPU unavailable

## Performance Expectations

### Cloud Run GPU Performance
- **Cold Start**: 30-60 seconds (GPU initialization)
- **Warm Start**: 5-15 seconds
- **AI Inference**: 0.5-2 seconds per analysis
- **Memory Usage**: 8-16GB during operation

### Cost Optimization
- **Concurrency**: Set to 1 for GPU workloads
- **Timeout**: 3600 seconds for long-running AI tasks
- **Memory**: 16GB minimum for GPU models
- **CPU Throttling**: Disabled for better performance

## Troubleshooting

### Common Issues

1. **"GPU not available"**
   ```bash
   # Check GPU quota
   gcloud compute regions describe us-central1 --format="value(quotas[].limit)"
   
   # Request GPU quota
   gcloud compute regions describe us-central1 --format="value(quotas[].limit)"
   ```

2. **"Out of memory"**
   - Increase memory allocation to 32GB
   - Reduce model size or use CPU fallback
   - Check Cloud Run memory limits

3. **"CUDA version mismatch"**
   - Ensure CUDA 12.1 compatibility
   - Update NVIDIA drivers if needed
   - Check container CUDA version

4. **"Cold start timeout"**
   - Increase timeout to 3600 seconds
   - Use startup CPU boost
   - Pre-warm the service

### Monitoring
```bash
# Check service logs
gcloud run services logs read truify-gpu --region us-central1

# Monitor GPU usage
gcloud run services describe truify-gpu --region us-central1 --format="value(status.url)"
```

## Security Considerations

### Secrets Management
```bash
# Create secrets for sensitive data
echo -n "your-email@gmail.com" | gcloud secrets create gmail-user --data-file=-
echo -n "your-app-password" | gcloud secrets create gmail-password --data-file=-

# Reference in deployment
gcloud run deploy truify-gpu \
  --set-env-vars "GMAIL_USER=gmail-user,GMAIL_APP_PASSWORD=gmail-password"
```

### Network Security
- Use VPC connector for private networking
- Configure IAM roles appropriately
- Enable audit logging

## Cost Estimation

### Monthly Costs (US Central1)
- **GPU Instance**: ~$730/month (T4)
- **Memory**: ~$146/month (16GB)
- **CPU**: ~$73/month (4 cores)
- **Network**: ~$10-50/month (depending on usage)

### Optimization Tips
- Use spot instances for development
- Implement auto-scaling based on demand
- Monitor and optimize resource usage
- Consider CPU-only for non-critical workloads

## Support

For Cloud Run GPU issues:
1. Check Google Cloud documentation
2. Verify GPU quota and availability
3. Review service logs and metrics
4. Contact Google Cloud support for quota increases
