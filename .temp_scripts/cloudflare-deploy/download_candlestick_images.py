#!/usr/bin/env python3
"""
Download new Crystal Candlesticks images
"""

import requests
from pathlib import Path

# New image URLs provided by user
new_candlestick_images = [
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2Fcandlestick.jpg&nonce=84ffb395-108b-46a8-9bb5-d792d843fe76&project_id=7620116912135094306&sign=c86caccc35710dde2cc4af3f7aeeeffd98fd14ae20ca7d8918be0eaa3798aad9",
        "filename": "candlestick-01.jpg",
        "title": "Crystal Candlestick 1"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162605_25_2.jpg&nonce=bdbe94c2-bf54-4534-97bf-718cfa2f4a86&project_id=7620116912135094306&sign=dc982a1df1bb9f9fe7e05a3133740f436d11a1f827d1b204ad69bc932b811923",
        "filename": "candlestick-02.jpg",
        "title": "Crystal Candlestick 2"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162614_29_2.jpg&nonce=261fa998-cbc7-4672-a734-fc50305c25d0&project_id=7620116912135094306&sign=b4a6d64d140d53c8d6b3bc6d5378ad6d960c765238464113f66e56b22bec2f7c",
        "filename": "candlestick-03.jpg",
        "title": "Crystal Candlestick 3"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321162623_30_2.jpg&nonce=b2ca9e79-71b2-48e3-9654-1470d36ebaf2&project_id=7620116912135094306&sign=60d4506732cb00fbca638b142066c1c6eeeb11823806ed2f7814eaf2b5027033",
        "filename": "candlestick-04.jpg",
        "title": "Crystal Candlestick 4"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165232_556_2.jpg&nonce=6e21af69-0ca1-4023-9100-1db8e9c38345&project_id=7620116912135094306&sign=a8dc678b3a15ca5e6d3b5a17c5897457e281eeed7b05706d09939b7d1c43d876",
        "filename": "candlestick-05.jpg",
        "title": "Crystal Candlestick 5"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165238_562_2.jpg&nonce=80544f6c-23cf-4cb0-97ce-0afbed02b60a&project_id=7620116912135094306&sign=57e00d48f8b778dc97331f27dfc9154f5c61e79e4bee85b1c864a368140876e4",
        "filename": "candlestick-06.jpg",
        "title": "Crystal Candlestick 6"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165239_564_2.jpg&nonce=c888ee8e-cc9e-4e6e-a1eb-52de3903ade8&project_id=7620116912135094306&sign=be31b9b5614065fced62459eb65beb5ac32a0c8c101e69c9d1e0e047927eb31c",
        "filename": "candlestick-07.jpg",
        "title": "Crystal Candlestick 7"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165245_570_2.jpg&nonce=42d2c491-9060-4073-a891-8bcb6bbefb15&project_id=7620116912135094306&sign=901dc75ebe202ee78546ced504a629c395ba1c00563ab3d0dca93d9208f8934a",
        "filename": "candlestick-08.jpg",
        "title": "Crystal Candlestick 8"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165246_571_2.jpg&nonce=56b308e9-50c6-4483-8404-f125269f3723&project_id=7620116912135094306&sign=56fe7447636d9229e81b17558f93217b40132f1f3552fbd1d9e0877ba41319cf",
        "filename": "candlestick-09.jpg",
        "title": "Crystal Candlestick 9"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165250_575_2.jpg&nonce=d62cd0c2-2a9d-4ef3-9339-3e1136e5d5a8&project_id=7620116912135094306&sign=217f958c3934249ef0e1f18d725d823330e1cfe71d0c04cb8a117db66d3c37f2",
        "filename": "candlestick-10.jpg",
        "title": "Crystal Candlestick 10"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165253_578_2.jpg&nonce=00a387fc-41f3-4c7a-9272-147de8d75a11&project_id=7620116912135094306&sign=512488761ef9bdba87aaff38d440384ec526f61c5e25c0eb53a8924d41c894ee",
        "filename": "candlestick-11.jpg",
        "title": "Crystal Candlestick 11"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165255_580_2.jpg&nonce=376eed93-2184-4a7e-8f34-1138ce35fcb7&project_id=7620116912135094306&sign=6a1caaed79fd4c686607648b6e345fb6a1e63b98da0a0badb3e5c7f6033c155e",
        "filename": "candlestick-12.jpg",
        "title": "Crystal Candlestick 12"
    },
    {
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F%E5%BE%AE%E4%BF%A1%E5%9C%96%E7%89%87_20260321165256_581_2.jpg&nonce=d306f8da-c500-4062-89e0-3e50c94288bc&project_id=7620116912135094306&sign=70e20912feb82f2340bd5dba3b4f20e5f712749fb415614f7bc2eda372902b3a",
        "filename": "candlestick-13.jpg",
        "title": "Crystal Candlestick 13"
    }
]

def download_candlestick_images():
    """Download new candlestick images"""
    
    # Create images directory if it doesn't exist
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Downloading {len(new_candlestick_images)} crystal candlestick images to {images_dir}/")
    print("=" * 60)
    
    downloaded_files = []
    
    for i, image in enumerate(new_candlestick_images, 1):
        print(f"\n[{i}/{len(new_candlestick_images)}] Downloading {image['filename']}...")
        
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
    print(f"✓ Downloaded {len(downloaded_files)}/{len(new_candlestick_images)} images")
    
    return downloaded_files

if __name__ == "__main__":
    download_candlestick_images()
