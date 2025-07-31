#!/bin/bash

# Build script with platform detection
PLATFORM=$(uname -m)
ENVIRONMENT=${1:-local}

echo "Detected platform: $PLATFORM"
echo "Environment: $ENVIRONMENT"

if [ "$PLATFORM" = "arm64" ] || [ "$PLATFORM" = "aarch64" ]; then
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "Building for production on ARM64 - using native ARM64 for GPT4All compatibility"
        echo "📦 This will take longer as it copies ~4GB of AI models..."
        docker build -t truify .
    else
        echo "Building for local development on ARM64 - using native ARM64 for GPT4All compatibility"
        echo "📦 This will take longer as it copies ~4GB of AI models..."
        docker build -t truify .
    fi
else
    echo "Building for x86_64 - using native platform"
    echo "📦 This will take longer as it copies ~4GB of AI models..."
    docker build -t truify .
fi

echo "Build complete!"
echo ""
echo "To run the application:"
echo "  docker-compose up -d"
echo ""
echo "To access the application:"
echo "  http://localhost:8501" 