#!/usr/bin/env python3
"""
Script to switch Truify from local GPT4All to OpenRouter.ai
"""

import os
import shutil

def switch_to_openrouter():
    """Switch from local GPT4All to OpenRouter.ai implementation"""
    
    # Backup original genai.py
    if os.path.exists('code/genai.py'):
        shutil.copy('code/genai.py', 'code/genai_gpt4all_backup.py')
        print("✓ Backed up original genai.py to genai_gpt4all_backup.py")
    
    # Copy OpenRouter implementation
    if os.path.exists('code/genai_openrouter.py'):
        shutil.copy('code/genai_openrouter.py', 'code/genai.py')
        print("✓ Switched to OpenRouter implementation")
    else:
        print("✗ OpenRouter implementation not found")
        return False
    
    # Update requirements.txt to remove gpt4all
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Remove gpt4all line
        lines = content.split('\n')
        lines = [line for line in lines if 'gpt4all' not in line]
        
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✓ Removed gpt4all from requirements.txt")
    
    print("\n🎉 Successfully switched to OpenRouter.ai!")
    print("\nNext steps:")
    print("1. Set your OpenRouter API key: export OPENROUTER_API_KEY='your-key-here'")
    print("2. Build the Docker image: docker build -f Dockerfile.openrouter -t truify-openrouter .")
    print("3. Run the container: docker run -p 8501:8501 -e OPENROUTER_API_KEY='your-key' truify-openrouter")
    
    return True

def switch_back_to_gpt4all():
    """Switch back to local GPT4All implementation"""
    
    # Restore original genai.py
    if os.path.exists('code/genai_gpt4all_backup.py'):
        shutil.copy('code/genai_gpt4all_backup.py', 'code/genai.py')
        print("✓ Restored original GPT4All implementation")
    else:
        print("✗ GPT4All backup not found")
        return False
    
    # Restore gpt4all to requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        if 'gpt4all' not in content:
            lines = content.split('\n')
            lines.append('gpt4all')
            
            with open('requirements.txt', 'w') as f:
                f.write('\n'.join(lines))
            
            print("✓ Restored gpt4all to requirements.txt")
    
    print("\n🎉 Successfully switched back to GPT4All!")
    print("\nNext steps:")
    print("1. Build the Docker image: docker build -f Dockerfile.gpu -t truify-gpu .")
    print("2. Run with GPU: docker run --gpus all -p 8501:8501 truify-gpu")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "gpt4all":
        switch_back_to_gpt4all()
    else:
        switch_to_openrouter()
