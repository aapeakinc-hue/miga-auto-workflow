#!/usr/bin/env python3
"""
Rename sample images with Chinese filenames to English filenames
"""

import os
import shutil

# Mapping of Chinese filenames to English filenames
rename_map = {
    "sample_微信圖片_20260321162810_44_2.jpg": "sample-classic-candelabra.jpg",
    "sample_微信圖片_20260321165154_518_2.jpg": "sample-tea-light-holder.jpg",
    "sample_微信圖片_20260321165225_547_2.jpg": "sample-chandelier.jpg",
    "sample_微信圖片_20260321165229_552_2.jpg": "sample-wall-sconce.jpg",
    "sample_微信圖片_20260321162605_25_2.jpg": "sample-ornament.jpg",
    "sample_微信圖片_20260321163151_67_2.jpg": "sample-votive-set.jpg",
    "sample_微信圖片_20260321165244_569_2.jpg": "sample-premium-candelabra.jpg",
    "sample_微信圖片_20260321165337_622_2.jpg": "sample-elegant-holder.jpg",
    "sample_微信圖片_20260321165358_643_2.jpg": "sample-candle-stand.jpg"
}

def rename_images():
    """Rename images from Chinese to English filenames"""
    
    images_dir = "images"
    
    print("Renaming sample images...")
    print("=" * 60)
    
    renamed_count = 0
    
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(images_dir, old_name)
        new_path = os.path.join(images_dir, new_name)
        
        if os.path.exists(old_path):
            # Copy to new filename
            shutil.copy2(old_path, new_path)
            print(f"✓ {old_name}")
            print(f"  → {new_name}")
            renamed_count += 1
        else:
            print(f"✗ Not found: {old_name}")
    
    print("\n" + "=" * 60)
    print(f"✓ Renamed {renamed_count} images")
    
    return rename_map

if __name__ == "__main__":
    rename_images()
