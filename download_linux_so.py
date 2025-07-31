#!/usr/bin/env python3
"""
Download Linux-specific GPT4All .so files.
"""

import os
import subprocess
import sys
from pathlib import Path

def download_linux_so():
    """Download Linux-specific GPT4All .so files."""
    print("🔧 Downloading Linux GPT4All .so files...")
    
    # Create so directory
    so_dir = Path("linux_so")
    so_dir.mkdir(exist_ok=True)
    
    # Try different sources for Linux .so files
    sources = [
        {
            "libllama.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllama.so",
            "libllmodel.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllmodel.so"
        },
        {
            "libllama.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllama-linux.so",
            "libllmodel.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllmodel-linux.so"
        },
        {
            "libllama.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllama-aarch64.so",
            "libllmodel.so": "https://github.com/nomic-ai/gpt4all/releases/download/v2.8.2/libllmodel-aarch64.so"
        }
    ]
    
    success_count = 0
    for source in sources:
        print(f"Trying source {sources.index(source) + 1}...")
        
        for lib_name, url in source.items():
            lib_file = so_dir / lib_name
            
            if lib_file.exists():
                size_mb = lib_file.stat().st_size / (1024 * 1024)
                print(f"✅ Library already exists: {lib_name} ({size_mb:.1f} MB)")
                success_count += 1
                continue
                
            print(f"Downloading {lib_name} from {url}...")
            try:
                result = subprocess.run([
                    "curl", "-L", "-o", str(lib_file), url
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    size_mb = lib_file.stat().st_size / (1024 * 1024)
                    if size_mb > 0.1:  # Check if file is not empty
                        print(f"✅ Successfully downloaded {lib_name} ({size_mb:.1f} MB)")
                        success_count += 1
                    else:
                        print(f"❌ Downloaded file is too small: {size_mb:.1f} MB")
                        lib_file.unlink()  # Remove empty file
                else:
                    print(f"❌ Failed to download {lib_name}: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error downloading {lib_name}: {e}")
        
        if success_count >= 2:
            break
    
    print(f"📊 Download Summary:")
    print(f"   ✅ Successfully downloaded: {success_count}/2 libraries")
    
    if success_count >= 2:
        print("🎉 All Linux libraries downloaded successfully!")
        print("📦 Libraries are now in the 'linux_so' directory and will be included in Docker image")
        return True
    else:
        print("⚠️  Some libraries failed to download.")
        return False

if __name__ == "__main__":
    success = download_linux_so()
    sys.exit(0 if success else 1) 