# OpenRouter.ai Integration for Truify

This guide explains how to use OpenRouter.ai with Claude Sonnet instead of local GPT4All models.

## Benefits of OpenRouter.ai

- **No GPU Required**: Runs on any CPU-only container
- **Faster Deployment**: No large model downloads
- **Better Performance**: Claude Sonnet is more capable than local models
- **Simpler Setup**: Just need an API key
- **Cost Effective**: Pay per use instead of GPU resources

## Quick Setup

### 1. Get OpenRouter API Key
1. Go to https://openrouter.ai/
2. Sign up and get your API key
3. Set the environment variable:
   ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```

### 2. Switch to OpenRouter Implementation
```bash
python switch_to_openrouter.py
```

### 3. Build and Run
```bash
# Build the container
docker build -f Dockerfile.openrouter -t truify-openrouter .

# Run with API key
docker run -p 8501:8501 -e OPENROUTER_API_KEY='your-api-key' truify-openrouter
```

## API Configuration

### Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)

### Model Configuration
The implementation uses:
- **Model**: `anthropic/claude-3-sonnet:20240229`
- **Max Tokens**: 2000
- **Temperature**: 0.7

## Cost Estimation

### OpenRouter Pricing (as of 2024)
- **Claude Sonnet**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **Typical Analysis**: ~500-1000 tokens per analysis
- **Estimated Cost**: ~$0.01-0.02 per analysis

### Comparison with GPU
- **GPU Cloud Run**: ~$730/month (T4 GPU)
- **OpenRouter**: ~$10-50/month (depending on usage)
- **Savings**: 90%+ cost reduction

## Features

### Available Functions
1. **Dataset Description**: Comprehensive analysis of dataset content and purpose
2. **Bias Analysis**: Detailed assessment of potential data bias
3. **PII Assessment**: Identification of personally identifiable information
4. **Data Anonymization**: Hash-based anonymization of sensitive columns

### Error Handling
- Graceful fallback to statistical analysis if API fails
- Detailed error messages for troubleshooting
- Automatic retry logic for transient failures

## Switching Between Implementations

### To OpenRouter
```bash
python switch_to_openrouter.py
```

### Back to GPT4All
```bash
python switch_to_openrouter.py gpt4all
```

## Docker Deployment

### Simple Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "code/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Run Deployment
```bash
# Build and push
docker build -f Dockerfile.openrouter -t gcr.io/PROJECT_ID/truify-openrouter .
docker push gcr.io/PROJECT_ID/truify-openrouter

# Deploy
gcloud run deploy truify-openrouter \
  --image gcr.io/PROJECT_ID/truify-openrouter \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars "OPENROUTER_API_KEY=your-api-key"
```

## Troubleshooting

### Common Issues
1. **"API key not set"**: Ensure OPENROUTER_API_KEY environment variable is set
2. **"API call failed"**: Check internet connectivity and API key validity
3. **"Rate limit exceeded"**: OpenRouter has rate limits; implement retry logic if needed

### Monitoring
- Check API usage in OpenRouter dashboard
- Monitor costs and usage patterns
- Set up alerts for high usage

## Security Considerations

### API Key Management
- Use environment variables, not hardcoded keys
- Rotate API keys regularly
- Monitor API usage for unusual patterns

### Data Privacy
- OpenRouter processes data on their servers
- Ensure compliance with data protection regulations
- Consider data sensitivity before using cloud APIs
