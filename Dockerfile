FROM python:3.12

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to force Linux ARM64 build
ENV TARGET_ARCH=aarch64
ENV TARGET_PLATFORM=linux
ENV GPT4ALL_MODEL_DIR=/app/models
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory and download Linux models during build
RUN mkdir -p /app/models && \
    cd /app/models && \
    wget -O mistral-7b-instruct-v0.1.Q4_0.gguf https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf && \
    wget -O mistral-7b-openorca.gguf2.Q4_0.gguf https://gpt4all.io/models/gguf/mistral-7b-openorca.gguf2.Q4_0.gguf && \
    echo "Models downloaded successfully"

# Expose port
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "code/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
