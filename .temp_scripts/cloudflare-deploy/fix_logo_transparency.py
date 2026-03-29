#!/usr/bin/env python3
"""
Fix LOGO watermark by making it transparent instead of white
"""

from PIL import Image
import numpy as np

def fix_logo_transparency():
    """
    Make the watermark area fully transparent
    The watermark area should be transparent to work on any background
    """
    
    logo_path = "images/MIGAC_logo.png"
    
    # Open image
    img = Image.open(logo_path)
    img_array = np.array(img)
    
    width, height = img.size
    print(f"Image size: {width} x {height}")
    
    # Check watermark area
    watermark_area = img_array[height-90:, width-260:]
    print(f"Watermark area: {watermark_area.shape}")
    
    # Check the colors in watermark area
    rgb_area = watermark_area[:, :, :3]
    
    # Check if it's mostly white
    white_pixels = np.sum((rgb_area[:, :, 0] > 240) &
                         (rgb_area[:, :, 1] > 240) &
                         (rgb_area[:, :, 2] > 240))
    total_pixels = watermark_area.shape[0] * watermark_area.shape[1]
    
    print(f"White pixels in watermark area: {white_pixels}/{total_pixels} ({100*white_pixels/total_pixels:.1f}%)")
    
    # If mostly white, make it transparent
    if white_pixels / total_pixels > 0.9:
        print("\n⚠️  Watermark area is mostly white - making it transparent...")
        
        # Set alpha to 0 in watermark area
        img_array[height-90:, width-260:, 3] = 0
        
        # Save fixed image
        fixed_img = Image.fromarray(img_array, 'RGBA')
        fixed_img.save("images/MIGAC_logo.png")
        print("✓ Updated MIGAC_logo.png - watermark area is now transparent")
        return True
    else:
        print("\n✓ Watermark area is not mostly white, keeping as is")
        return False

if __name__ == "__main__":
    print("Fixing LOGO watermark transparency...")
    print("=" * 60)
    
    fix_logo_transparency()
    
    print("\n" + "=" * 60)
    print("✓ Done!")
