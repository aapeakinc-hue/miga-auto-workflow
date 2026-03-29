#!/usr/bin/env python3
"""
Download new Crystal Pillar Holders images
"""

import requests
from pathlib import Path

# New image URLs provided by user
new_pillar_images = [
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162548_18_2.jpg&nonce=230f64ee-9dd9-435d-b2d3-40c3a2147f37&project_id=7620116912135094306&sign=0a4d4d8e220b97cf30da85a0ea1ad8304e3bd780cde709e2e7e2b074dc9623f3",
        "filename": "pillar-holder-01.jpg",
        "title": "Crystal Pillar Holder 1"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321163151_67_2.jpg&nonce=572dcda9-7a63-4d55-bf0d-0ca33aef62e2&project_id=7620116912135094306&sign=0175448337ae09c7126679fda156e4481ef15b3b44946f7d3c20c01aa08fdd95",
        "filename": "pillar-holder-02.jpg",
        "title": "Crystal Pillar Holder 2"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321163456_101_2.jpg&nonce=d2948b10-965f-44be-bd03-bc77a37d7c30&project_id=7620116912135094306&sign=147d3948910b8dd43972de902837ad2dbfda762b0739ee3dd4b4fb8a1543990d",
        "filename": "pillar-holder-03.jpg",
        "title": "Crystal Pillar Holder 3"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165132_495_2.jpg&nonce=b48dbbd0-e1be-439c-8e5f-8fd4b6b76fd2&project_id=7620116912135094306&sign=d3f33a588841c35e295befa9ea558b3cce1b6dc5e5c27448b700c0f9fc3cdef6",
        "filename": "pillar-holder-04.jpg",
        "title": "Crystal Pillar Holder 4"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165235_559_2.jpg&nonce=94f8abed-ae61-410b-97d4-6305f8e560d9&project_id=7620116912135094306&sign=e17cefa2c8785cad47f5c90b23ffaa9806033eed2aa776401911216aa5e31b46",
        "filename": "pillar-holder-05.jpg",
        "title": "Crystal Pillar Holder 5"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165242_567_2.jpg&nonce=3d03e7e8-5963-4fb5-8cd2-3fa8a2782ebd&project_id=7620116912135094306&sign=9b3de5671ab0bd78ef9a0004f53dc806dd62e426f14693cd0049706f6bc6e30b",
        "filename": "pillar-holder-06.jpg",
        "title": "Crystal Pillar Holder 6"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165254_579_2.jpg&nonce=5397b66d-2faf-4909-bc51-b9e566c256b2&project_id=7620116912135094306&sign=2776af8f29af00acdf650b991c230dd3b402c48071dcc63071154ee76633de12",
        "filename": "pillar-holder-07.jpg",
        "title": "Crystal Pillar Holder 7"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165257_582_2.jpg&nonce=c02c73f5-560e-4ca1-89d5-28a2b92a188b&project_id=7620116912135094306&sign=70d7d941c45084b549225048ccbea22dd42c892a0a8709d6cd11bdbc66fd04ef",
        "filename": "pillar-holder-08.jpg",
        "title": "Crystal Pillar Holder 8"
    }
]

def download_pillar_images():
    """Download new pillar holder images"""
    
    # Create images directory if it doesn't exist
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Downloading {len(new_pillar_images)} pillar holder images to {images_dir}/")
    print("=" * 60)
    
    downloaded_files = []
    
    for i, image in enumerate(new_pillar_images, 1):
        print(f"\n[{i}/{len(new_pillar_images)}] Downloading {image['filename']}...")
        
        try:
            response = requests.get(image['url'], timeout=30)
            response.raise_for_status()
            
            # Save image
            filepath = images_dir / image['filename']
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✓ Saved to {filepath}")
            print(f"  ✓ Size: {len(response.content)} bytes")
            
            downloaded_files.append(image['filename'])
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✓ Downloaded {len(downloaded_files)}/{len(new_pillar_images)} images")
    
    return downloaded_files

if __name__ == "__main__":
    download_pillar_images()
