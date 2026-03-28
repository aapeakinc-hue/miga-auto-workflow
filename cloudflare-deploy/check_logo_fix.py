#!/usr/bin/env python3
"""
Check and fix LOGO watermark removal
"""

from PIL import Image
import numpy as np

def check_logo_watermark():
    """Check the watermark removal status of LOGO"""
    
    logo_path = "images/MIGAC_logo.png"
    
    # Open image
    img = Image.open(logo_path)
    img_array = np.array(img)
    
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    
    # Check if image has transparency
    if img.mode == 'RGBA':
        print(f"Has alpha channel: Yes")
        alpha = img_array[:, :, 3]
        print(f"Alpha channel shape: {alpha.shape}")
        print(f"Alpha min/max: {alpha.min()}/{alpha.max()}")
    else:
        print(f"Has alpha channel: No")
    
    # Check bottom right corner
    width, height = img.size
    watermark_area = img_array[height-90:, width-260:]
    
    print(f"\nWatermark area shape: {watermark_area.shape}")
    
    # Check if the area is transparent or has a specific color
    if img.mode == 'RGBA':
        alpha_corner = watermark_area[:, :, 3]
        print(f"Corner alpha min/max: {alpha_corner.min()}/{alpha_corner.max()}")
        
        # Count transparent pixels
        transparent_pixels = np.sum(alpha_corner == 0)
        total_pixels = watermark_area.shape[0] * watermark_area.shape[1]
        print(f"Transparent pixels: {transparent_pixels}/{total_pixels} ({100*transparent_pixels/total_pixels:.1f}%)")
    
    return img, img_array

def fix_logo_background():
    """
    Fix the logo background to match website theme
    The website uses a clean white/transparent background
    """
    
    img, img_array = check_logo_watermark()
    
    # Check if the watermark area needs fixing
    width, height = img.size
    watermark_area = img_array[height-90:, width-260:]
    
    # If the watermark area has been cleared to white or transparent, ensure consistency
    if img.mode == 'RGBA':
        # Check if there are white pixels in the watermark area
        # If so, we might want to make them transparent or ensure they blend well
        alpha = img_array[:, :, 3]
        
        # Check the area that was previously the watermark
        corner_alpha = img_array[height-90:, width-260:, 3]
        
        # If corner has inconsistent transparency, fix it
        if corner_alpha.min() > 0 and corner_alpha.max() < 255:
            print("\n⚠️  Found inconsistent transparency in watermark area")
            print("   This may cause visual issues on different backgrounds")
            
            # Option 1: Make the area fully transparent
            # This is the best option for a logo that will appear on various backgrounds
            img_array[height-90:, width-260:, 3] = 0
            
            # Save fixed image
            fixed_img = Image.fromarray(img_array, 'RGBA')
            fixed_img.save("images/MIGAC_logo_fixed.png")
            print("✓ Created MIGAC_logo_fixed.png with fully transparent watermark area")
            
            # Check if we should replace the original
            # For now, just show the preview info
            return True
        else:
            print("\n✓ Watermark area transparency is consistent")
            return False
    
    return False

if __name__ == "__main__":
    print("Checking LOGO watermark removal status...")
    print("=" * 60)
    
    needs_fix = fix_logo_background()
    
    print("\n" + "=" * 60)
    if needs_fix:
        print("⚠️  A fixed version has been created: MIGAC_logo_fixed.png")
        print("   Please review and decide whether to replace the original")
    else:
        print("✓ LOGO watermark removal is correct")
