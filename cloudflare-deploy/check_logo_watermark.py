#!/usr/bin/env python3
"""
Check LOGO watermark removal status
"""

from PIL import Image
import numpy as np

def check_logo():
    """Check LOGO watermark removal"""
    
    logo_path = "images/MIGAC_logo.png"
    
    try:
        img = Image.open(logo_path)
        img_array = np.array(img)
        
        width, height = img.size
        print(f"Image size: {width} x {height}")
        print(f"Image mode: {img.mode}")
        
        # Check watermark area
        watermark_area = img_array[height-90:, width-260:]
        print(f"\nWatermark area shape: {watermark_area.shape}")
        
        if img.mode == 'RGBA':
            alpha = watermark_area[:, :, 3]
            print(f"Alpha channel min/max: {alpha.min()}/{alpha.max()}")
            
            # Count transparent pixels
            transparent_pixels = np.sum(alpha == 0)
            total_pixels = watermark_area.shape[0] * watermark_area.shape[1]
            
            print(f"Transparent pixels: {transparent_pixels}/{total_pixels} ({100*transparent_pixels/total_pixels:.1f}%)")
            
            if transparent_pixels == total_pixels:
                print("\n✓ Watermark area is fully transparent")
            else:
                print("\n✗ Watermark area is NOT fully transparent")
                print("   Some pixels are still visible")
                
                # Show sample pixel values
                print(f"\nSample pixel values (first 5x5):")
                print(f"RGBA values at top-left of watermark area:")
                for i in range(min(5, watermark_area.shape[0])):
                    for j in range(min(5, watermark_area.shape[1])):
                        pixel = watermark_area[i, j]
                        print(f"  [{i},{j}]: R={pixel[0]:3d} G={pixel[1]:3d} B={pixel[2]:3d} A={pixel[3]:3d}")
        
        return True
        
    except Exception as e:
        print(f"Error checking LOGO: {e}")
        return False

if __name__ == "__main__":
    print("Checking LOGO watermark removal...")
    print("=" * 60)
    check_logo()
