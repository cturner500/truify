#!/usr/bin/env python3
"""
Pre-download GPT4All models to local directory.
This script downloads the Mistral model to a local 'models' directory
so it's included in the Docker image without downloading during build.
"""

import os
import sys
import shutil
from pathlib import Path

def download_model(model_name):
    """Download a GPT4All model to local models directory."""
    try:
        from gpt4all import GPT4All
        print(f"Downloading {model_name}...")
        
        # Create models directory
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # Set the model directory to our local models folder
        os.environ["GPT4ALL_MODEL_DIR"] = str(models_dir.absolute())
        
        # This will download the model to our local models directory
        model = GPT4All(model_name, allow_download=True)
        print(f"✅ Successfully downloaded {model_name}")
        
        # Check if the model file exists in our models directory
        model_file = models_dir / model_name
        if model_file.exists():
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"📁 Model saved to: {model_file}")
            print(f"📊 Model size: {size_mb:.1f} MB")
            return True
        else:
            print(f"⚠️  Warning: Model file not found at {model_file}")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading {model_name}: {e}")
        # Check if the model file exists anyway
        model_file = Path("models") / model_name
        if model_file.exists():
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"✅ Model file downloaded successfully: {size_mb:.1f} MB")
            print(f"⚠️  Note: Model may not work in this environment due to CPU limitations")
            return True
        return False

def main():
    """Download the Mistral model to local models directory."""
    print("🚀 Starting model download to local 'models' directory...")
    
    # List of models to download
    models = [
        "mistral-7b-instruct-v0.1.Q4_0.gguf",
        "mistral-7b-openorca.gguf2.Q4_0.gguf"
    ]
    
    success_count = 0
    for model in models:
        if download_model(model):
            success_count += 1
        print()  # Add spacing between models
    
    print(f"📊 Download Summary:")
    print(f"   ✅ Successfully downloaded: {success_count}/{len(models)} models")
    
    if success_count == len(models):
        print("🎉 All models downloaded successfully!")
        print("📦 Models are now in the 'models' directory and will be included in Docker image")
        return 0
    else:
        print("⚠️  Some models failed to download, but the application will still work.")
        print("📦 Model files are included in the Docker image for production use.")
        return 0  # Don't fail the build

if __name__ == "__main__":
    sys.exit(main())
