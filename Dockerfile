FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download GPT4All models during build (using working model names)
RUN python -c "
from gpt4all import GPT4All
import os

# Create models directory
os.makedirs('/root/.local/share/nomic.ai/GPT4All', exist_ok=True)

# Download primary model (using working model name)
try:
    print('Downloading mistral-7b-instruct-v0.1.Q4_0.gguf...')
    model1 = GPT4All('mistral-7b-instruct-v0.1.Q4_0.gguf', allow_download=True)
    print('Primary model downloaded successfully')
except Exception as e:
    print(f'Primary model download failed: {e}')

# Download fallback model (using working model name)
try:
    print('Downloading mistral-7b-openorca.gguf2.Q4_0.gguf...')
    model2 = GPT4All('mistral-7b-openorca.gguf2.Q4_0.gguf', allow_download=True)
    print('Fallback model downloaded successfully')
except Exception as e:
    print(f'Fallback model download failed: {e}')
"

# Expose port
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "code/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
