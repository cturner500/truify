#!/bin/bash

echo "Building Truify GPU-enabled Docker image..."
echo "This will download ~4GB of AI models and may take several minutes."

# Check if NVIDIA Docker runtime is available
if ! docker info | grep -q "nvidia"; then
    echo "Warning: NVIDIA Docker runtime not detected. GPU acceleration may not work."
    echo "Please install nvidia-docker2: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
fi

# Build GPU image
docker build -f Dockerfile.gpu -t truify-gpu .

echo "GPU build complete!"
echo "To run with GPU: docker run --gpus all -p 8501:8501 truify-gpu"
echo "Or use: docker-compose -f docker-compose.gpu.yml up"
