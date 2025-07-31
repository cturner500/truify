#!/usr/bin/env python3
"""
Script to download GPT4All models during Docker build
"""

from gpt4all import GPT4All
import os

def download_models():
    # Create models directory
    os.makedirs('/root/.local/share/nomic.ai/GPT4All', exist_ok=True)
    
    # Download primary model
    try:
        print('Downloading mistral-7b-instruct-v0.1.Q4_0.gguf...')
        model1 = GPT4All('mistral-7b-instruct-v0.1.Q4_0.gguf', allow_download=True)
        print('Primary model downloaded successfully')
    except Exception as e:
        print(f'Primary model download failed: {e}')
    
    # Download fallback model
    try:
        print('Downloading mistral-7b-openorca.gguf2.Q4_0.gguf...')
        model2 = GPT4All('mistral-7b-openorca.gguf2.Q4_0.gguf', allow_download=True)
        print('Fallback model downloaded successfully')
    except Exception as e:
        print(f'Fallback model download failed: {e}')

if __name__ == "__main__":
    download_models()
