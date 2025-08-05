#!/usr/bin/env python3
"""
Script to clean up TruifyLogo.png by removing dark dots and keeping only light blue and white colors.
"""

from PIL import Image
import numpy as np
from collections import Counter
import os

def clean_logo(input_path='images/TruifyLogo.png', output_path='TruifyLogo2.png'):
    """
    Clean the logo by removing dark dots and keeping only light blue and white colors.
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert to numpy array for easier processing
    img_array = np.array(img)
    
    # Get all unique colors and their counts
    colors = []
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            colors.append(tuple(img_array[y, x]))
    
    color_counts = Counter(colors)
    
    # Find the two most common colors (should be light blue and white)
    most_common_colors = color_counts.most_common(2)
    print(f"Most common colors: {most_common_colors}")
    
    # Extract the two main colors
    color1, count1 = most_common_colors[0]
    color2, count2 = most_common_colors[1]
    
    print(f"Color 1 (count {count1}): RGB{color1}")
    print(f"Color 2 (count {count2}): RGB{color2}")
    
    # Create a tolerance for color matching (in case there are slight variations)
    tolerance = 30
    
    # Create new image array
    cleaned_array = img_array.copy()
    
    # Process each pixel
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            pixel = img_array[y, x]
            
            # Check if pixel is close to either of the two main colors
            is_color1 = all(abs(pixel[i] - color1[i]) <= tolerance for i in range(3))
            is_color2 = all(abs(pixel[i] - color2[i]) <= tolerance for i in range(3))
            
            if is_color1:
                cleaned_array[y, x] = color1
            elif is_color2:
                cleaned_array[y, x] = color2
            else:
                # For pixels that don't match either color, find the closest one
                dist1 = sum((pixel[i] - color1[i])**2 for i in range(3))
                dist2 = sum((pixel[i] - color2[i])**2 for i in range(3))
                
                if dist1 < dist2:
                    cleaned_array[y, x] = color1
                else:
                    cleaned_array[y, x] = color2
    
    # Convert back to PIL Image
    cleaned_img = Image.fromarray(cleaned_array)
    
    # Save the cleaned image
    cleaned_img.save(output_path)
    print(f"Cleaned image saved as {output_path}")
    
    # Show some statistics
    unique_colors_after = set()
    for y in range(cleaned_array.shape[0]):
        for x in range(cleaned_array.shape[1]):
            unique_colors_after.add(tuple(cleaned_array[y, x]))
    
    print(f"Unique colors after cleaning: {len(unique_colors_after)}")
    print(f"Colors: {list(unique_colors_after)}")

if __name__ == "__main__":
    if os.path.exists('images/TruifyLogo.png'):
        clean_logo()
    else:
        print("images/TruifyLogo.png not found")
