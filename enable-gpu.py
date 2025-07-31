#!/usr/bin/env python3
"""
Script to enable GPU support in genai.py
"""

import re

def enable_gpu_in_genai():
    """Modify genai.py to use GPU acceleration"""
    
    # Read the current genai.py file
    with open('code/genai.py', 'r') as f:
        content = f.read()
    
    # Add GPU device parameter to GPT4All initialization
    # Find the model initialization lines and add device='gpu'
    content = re.sub(
        r'model = GPT4All\(([^)]+)\)',
        r'model = GPT4All(\1, device="gpu")',
        content
    )
    
    # Add GPU availability check at the top of functions
    gpu_check = '''
    # Check for GPU availability
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        device = "gpu" if gpu_available else "cpu"
    except ImportError:
        device = "cpu"
'''
    
    # Add GPU check to describe_dataset_with_genai function
    content = re.sub(
        r'(def describe_dataset_with_genai\([^)]+\):\s*\n\s*"""[^"]*"""\s*\n)',
        r'\1' + gpu_check + '\n',
        content
    )
    
    # Add GPU check to analyze_bias_with_genai function
    content = re.sub(
        r'(def analyze_bias_with_genai\([^)]+\):\s*\n\s*"""[^"]*"""\s*\n)',
        r'\1' + gpu_check + '\n',
        content
    )
    
    # Add GPU check to PII_assessment function
    content = re.sub(
        r'(def PII_assessment\([^)]+\):\s*\n\s*"""[^"]*"""\s*\n)',
        r'\1' + gpu_check + '\n',
        content
    )
    
    # Write the modified content back
    with open('code/genai.py', 'w') as f:
        f.write(content)
    
    print("GPU support enabled in genai.py")
    print("Models will now use GPU acceleration when available")

if __name__ == "__main__":
    enable_gpu_in_genai()
