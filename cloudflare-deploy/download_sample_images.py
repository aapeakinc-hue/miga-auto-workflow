#!/usr/bin/env python3
"""
Download new sample images and update request-sample.html
"""

import os
import requests
from pathlib import Path

# New image URLs provided by user
new_images = [
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162810_44_2.jpg&nonce=40141a7a-7f66-4f81-a864-519cf3660f57&project_id=7620116912135094306&sign=06f1dbad22e23d3f5ffc0859a7797498d4a1b1f81181265ecca6af855ba8c705",
        "filename": "sample-01.jpg",
        "title": "Classic Crystal Candelabra"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165154_518_2.jpg&nonce=243339a1-b080-4cdf-be2a-788699c031e4&project_id=7620116912135094306&sign=6965dea8ba2e3eb2dbe3b928aa107667c62696ecb92160a02954a6092538f4fb",
        "filename": "sample-02.jpg",
        "title": "Crystal Tea Light Holder"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165225_547_2.jpg&nonce=8c5a4b76-5bfa-495b-b137-d775e70d9915&project_id=7620116912135094306&sign=5e8bcda979c59d27db964e9144b62241b4b3790ff31c5e56df503665e778fb6e",
        "filename": "sample-03.jpg",
        "title": "Luxury Crystal Chandelier"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165229_552_2.jpg&nonce=ec39e0eb-7197-4f71-a43b-395cb11844df&project_id=7620116912135094306&sign=ef8e23877257f56dd79cbdccb7bd7a16deea7d42ebf692949aea038b0bcd7a51",
        "filename": "sample-04.jpg",
        "title": "Crystal Wall Sconce"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162605_25_2.jpg&nonce=90eabffe-2d1b-4e6b-a478-b3e0965d85dc&project_id=7620116912135094306&sign=5ee76d99a51604a633493161c1d2c93c0b1ccbcde2f4aea5329da38406456b91",
        "filename": "sample-05.jpg",
        "title": "Crystal Decorative Ornament"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321163151_67_2.jpg&nonce=d628b510-3155-4cfb-b590-23d7ff2d6cec&project_id=7620116912135094306&sign=6b7fc44ce820e4dca6c389f7c0bddaa09f7fc959b00af42c686c9b9280884844",
        "filename": "sample-06.jpg",
        "title": "Crystal Votive Set"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165244_569_2.jpg&nonce=f478d0dc-fe10-4c72-8ff4-48f17059bf28&project_id=7620116912135094306&sign=ed6f3bf5c9b36e7c6431dc07f6be5a0f7ba3f1ba1aaf0dc9594dda5444095462",
        "filename": "sample-07.jpg",
        "title": "Premium Crystal Candelabra"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165337_622_2.jpg&nonce=9f89540a-5a7e-4221-b6cc-5c66f2bb86a6&project_id=7620116912135094306&sign=2b40f2f787fe9fc96ace3b471cf81ad7739f8968f003923eaaae7cb916193f50",
        "filename": "sample-08.jpg",
        "title": "Elegant Crystal Holder"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165358_643_2.jpg&nonce=1f0cab0e-80c3-4410-8b64-0daceee72aba&project_id=7620116912135094306&sign=011dedb58aa8bf9b9cceb950d727573d9d2f973b7a8278ec56ee695f70102d88",
        "filename": "sample-09.jpg",
        "title": "Crystal Candle Stand"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F5+arms+candelabras.jpg&nonce=28ef33d2-c389-40af-be25-05b4c49c2735&project_id=7620116912135094306&sign=131459696c69a33236a525720498daa82ea2ba71c5f9e7ed7a640395eef974b0",
        "filename": "sample-10.jpg",
        "title": "5-Arm Crystal Candelabra"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F9+arms+candelabra.jpg&nonce=98727ac0-de5b-49e8-92c7-b21677bf8cd2&project_id=7620116912135094306&sign=cd0c4d618f3d74be45b48f14f5296b6a2bbd017cb7af11bed31c3e7ab87f95fa",
        "filename": "sample-11.jpg",
        "title": "9-Arm Crystal Candelabra"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F9+candlesticks+candelabra.jpg&nonce=25fc93fd-ec2e-4be0-9c20-34ce0cde6cb6&project_id=7620116912135094306&sign=863bc3526a75a71d099ad0e462b82aa3d69ca3b188ea534f0d944020f27b0e33",
        "filename": "sample-12.jpg",
        "title": "9-Candlesticks Candelabra"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2Fcandle+holder.jpg&nonce=a16beb10-188a-4715-bd0d-c74556f18798&project_id=7620116912135094306&sign=4d1c7e5664c3778be74df19f9f622de1ab1b7bb2498fc0d1d7321511a1621107",
        "filename": "sample-13.jpg",
        "title": "Crystal Candle Holder"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2Fcandlestick.jpg&nonce=65c58f86-3719-4e93-b99a-f73e7b79f4a6&project_id=7620116912135094306&sign=c4c26c0af92b8252825fe36bf8c495063506a58aa42bfb2b792dee15af7b3182",
        "filename": "sample-14.jpg",
        "title": "Elegant Candlestick"
    }
]

def download_images():
    """Download all new images"""
    
    # Create products directory if it doesn't exist
    products_dir = Path("products")
    products_dir.mkdir(exist_ok=True)
    
    print(f"Downloading {len(new_images)} images to {products_dir}/")
    print("=" * 60)
    
    downloaded_files = []
    
    for i, image in enumerate(new_images, 1):
        print(f"\n[{i}/{len(new_images)}] Downloading {image['filename']}...")
        
        try:
            response = requests.get(image['url'], timeout=30)
            response.raise_for_status()
            
            # Save image
            filepath = products_dir / image['filename']
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✓ Saved to {filepath}")
            print(f"  ✓ Size: {len(response.content)} bytes")
            
            downloaded_files.append(image['filename'])
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✓ Downloaded {len(downloaded_files)}/{len(new_images)} images")
    
    return downloaded_files

if __name__ == "__main__":
    download_images()
