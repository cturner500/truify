#!/bin/bash

# Production deployment script with platform detection
PLATFORM=$(uname -m)

echo "=== Truify Production Deployment ==="
echo "Detected platform: $PLATFORM"
echo ""

# Build the image
echo "Building Docker image..."
echo "📦 This will take longer as it downloads ~4GB of AI models..."
if [ "$PLATFORM" = "arm64" ] || [ "$PLATFORM" = "aarch64" ]; then
    echo "Using x86_64 emulation for GPT4All compatibility"
    docker buildx build --platform linux/amd64 -t truify --load .
else
    echo "Using native x86_64 platform"
    docker build -t truify .
fi

echo ""
echo "Build complete!"
echo ""
echo "=== Deployment Options ==="
echo ""
echo "1. Local deployment:"
echo "   docker-compose up -d"
echo ""
echo "2. Production deployment (with environment variables):"
echo "   docker run -d -p 8501:8501 \\"
echo "     -e GMAIL_USER=your-email@domain.com \\"
echo "     -e GMAIL_APP_PASSWORD=your-app-password \\"
echo "     -v \$(pwd)/data:/app/data \\"
echo "     -v \$(pwd)/email.csv:/app/email.csv \\"
echo "     -v \$(pwd)/users.csv:/app/users.csv \\"
echo "     --name truify-production \\"
echo "     truify"
echo ""
echo "3. Docker Compose with environment file:"
echo "   docker-compose --env-file .env.production up -d"
echo ""
echo "=== Access Information ==="
echo "Application will be available at: http://localhost:8501" 