FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download GPT4All models during build (after pip install)
RUN python -c "from gpt4all import GPT4All; import os; os.makedirs('/root/.local/share/nomic.ai/GPT4All', exist_ok=True); print('Downloading mistral-7b-instruct-v0.2.Q4_0.gguf...'); model1 = GPT4All('mistral-7b-instruct-v0.2.Q4_0.gguf', allow_download=True); print('Primary model downloaded successfully'); print('Downloading mistral-7b-openorca.Q4_0.gguf...'); model2 = GPT4All('mistral-7b-openorca.Q4_0.gguf', allow_download=True); print('Fallback model downloaded successfully')"

# Expose port
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "code/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
