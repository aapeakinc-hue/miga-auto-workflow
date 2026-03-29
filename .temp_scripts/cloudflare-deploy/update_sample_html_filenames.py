#!/usr/bin/env python3
"""
Update request-sample.html to use English image filenames
"""

import re

# Mapping of old filenames to new filenames
filename_map = {
    "images/sample_微信圖片_20260321162810_44_2.jpg": "images/sample-classic-candelabra.jpg",
    "images/sample_微信圖片_20260321165154_518_2.jpg": "images/sample-tea-light-holder.jpg",
    "images/sample_微信圖片_20260321165225_547_2.jpg": "images/sample-chandelier.jpg",
    "images/sample_微信圖片_20260321165229_552_2.jpg": "images/sample-wall-sconce.jpg",
    "images/sample_微信圖片_20260321162605_25_2.jpg": "images/sample-ornament.jpg",
    "images/sample_微信圖片_20260321163151_67_2.jpg": "images/sample-votive-set.jpg",
    "images/sample_微信圖片_20260321165244_569_2.jpg": "images/sample-premium-candelabra.jpg",
    "images/sample_微信圖片_20260321165337_622_2.jpg": "images/sample-elegant-holder.jpg",
    "images/sample_微信圖片_20260321165358_643_2.jpg": "images/sample-candle-stand.jpg"
}

def update_html_filenames():
    """Update HTML to use new filenames"""
    
    # Read the file
    with open('request-sample.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all Chinese filenames with English filenames
    for old_filename, new_filename in filename_map.items():
        content = content.replace(old_filename, new_filename)
    
    # Write back
    with open('request-sample.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Updated request-sample.html:")
    print(f"  - Replaced {len(filename_map)} Chinese filenames with English filenames")
    print("  - Images should now display correctly")

if __name__ == "__main__":
    print("Updating request-sample.html...")
    print("=" * 60)
    update_html_filenames()
    print("\n" + "=" * 60)
    print("✓ Done!")
