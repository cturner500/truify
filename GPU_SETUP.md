# GPU Setup for Truify

This guide explains how to run Truify with GPU acceleration for faster AI model inference.

## Prerequisites

### 1. NVIDIA GPU
- NVIDIA GPU with CUDA support (GTX 1060 or newer recommended)
- At least 8GB VRAM for optimal performance
- 16GB+ VRAM recommended for larger models

### 2. NVIDIA Drivers
Install the latest NVIDIA drivers for your GPU:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nvidia-driver-535

# CentOS/RHEL
sudo yum install nvidia-driver

# Check installation
nvidia-smi
```

### 3. NVIDIA Docker Runtime
Install nvidia-docker2:
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test installation
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
```

## Building and Running

### Option 1: Using Build Script
```bash
./build-gpu.sh
```

### Option 2: Manual Build
```bash
# Build GPU image
docker build -f Dockerfile.gpu -t truify-gpu .

# Run with GPU
docker run --gpus all -p 8501:8501 truify-gpu
```

### Option 3: Using Docker Compose
```bash
docker-compose -f docker-compose.gpu.yml up
```

## Performance Expectations

- **CPU-only**: ~2-5 seconds per AI analysis
- **GPU-accelerated**: ~0.5-2 seconds per AI analysis
- **Memory usage**: ~4-8GB VRAM during model loading

## Troubleshooting

### GPU Not Detected
```bash
# Check if NVIDIA runtime is available
docker info | grep nvidia

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
```

### Out of Memory
- Reduce model size or use CPU fallback
- Close other GPU applications
- Use smaller models in genai.py

### CUDA Version Mismatch
- Ensure host CUDA version matches container CUDA version
- Update NVIDIA drivers if needed

## Model Configuration

The GPU setup uses these models:
- `mistral-7b-instruct-v0.1.Q4_0.gguf` (~4GB)
- `mistral-7b-openorca.gguf2.Q4_0.gguf` (~4GB)

Models are automatically downloaded during the Docker build process.

## Environment Variables

Key GPU environment variables:
- `CUDA_VISIBLE_DEVICES=0`: Use first GPU
- `NVIDIA_VISIBLE_DEVICES=all`: Allow access to all GPUs
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility`: Enable compute capabilities

## Monitoring

Monitor GPU usage:
```bash
# Host monitoring
nvidia-smi

# Container monitoring
docker exec <container_id> nvidia-smi
```
