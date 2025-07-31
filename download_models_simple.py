#!/usr/bin/env python3
"""
Simple script to download GPT4All models to local models directory.
"""

import os
import subprocess
import sys
from pathlib import Path

def download_model(model_name, url):
    """Download a model using wget."""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_file = models_dir / model_name
    
    if model_file.exists():
        size_mb = model_file.stat().st_size / (1024 * 1024)
        print(f"✅ Model already exists: {model_name} ({size_mb:.1f} MB)")
        return True
    
    print(f"Downloading {model_name}...")
    try:
        # Use wget to download the model
        result = subprocess.run([
            "wget", "-O", str(model_file), url
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"✅ Successfully downloaded {model_name} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"❌ Failed to download {model_name}: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ wget not found. Please install wget or use curl.")
        return False

def main():
    """Download the Mistral models."""
    print("🚀 Downloading models to local 'models' directory...")
    
    # Model URLs (these are the direct download URLs)
    models = {
        "mistral-7b-instruct-v0.1.Q4_0.gguf": "https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf",
        "mistral-7b-openorca.gguf2.Q4_0.gguf": "https://gpt4all.io/models/gguf/mistral-7b-openorca.gguf2.Q4_0.gguf"
    }
    
    success_count = 0
    for model_name, url in models.items():
        if download_model(model_name, url):
            success_count += 1
        print()
    
    print(f"📊 Download Summary:")
    print(f"   ✅ Successfully downloaded: {success_count}/{len(models)} models")
    
    if success_count == len(models):
        print("🎉 All models downloaded successfully!")
        print("📦 Models are now in the 'models' directory and will be included in Docker image")
    else:
        print("⚠️  Some models failed to download.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 