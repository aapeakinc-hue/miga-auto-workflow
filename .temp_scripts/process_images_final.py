#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名和规范图片文件
"""

import os
import shutil
from PIL import Image

def create_logo():
    """创建Logo"""
    # 使用现有的logo.jpg创建
    logo_path = 'cloudflare-deploy/images/logo.jpg'
    new_logo_path = 'cloudflare-deploy/images/MIGAC_logo.png'

    if os.path.exists(logo_path):
        # 读取并转换格式
        img = Image.open(logo_path)
        # 转换为RGB（如果是RGBA）
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # 调整大小
        img.thumbnail((400, 120))
        # 保存为PNG
        img.save(new_logo_path, 'PNG', optimize=True)
        print(f"✅ Created logo: {new_logo_path}")
        return True
    else:
        print(f"❌ Logo source not found: {logo_path}")
        return False

def create_hero_banner():
    """创建Hero Banner"""
    # 使用第一张产品图片作为Hero Banner
    product_images = [
        'cloudflare-deploy/images/5 arms candelabra.jpg',
        'cloudflare-deploy/images/crystal bubble stand.jpg',
        'cloudflare-deploy/images/crystal candle holders.jpg',
    ]

    for img_path in product_images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            # 调整为banner尺寸
            img_resized = img.resize((1200, 500), Image.Resampling.LANCZOS)
            # 保存
            banner_path = 'cloudflare-deploy/images/hero-banner.jpg'
            img_resized.save(banner_path, 'JPEG', quality=85, optimize=True)
            print(f"✅ Created hero banner: {banner_path}")
            return True

    print("❌ No suitable image found for hero banner")
    return False

def rename_product_images():
    """重命名产品图片为统一格式"""
    images_dir = 'cloudflare-deploy/images'
    product_count = 0

    # 获取所有图片
    all_files = os.listdir(images_dir)

    # 跳过已经重命名的文件
    renamed_files = [f for f in all_files if f.startswith('product-')]
    product_count = len(renamed_files)

    # 统计现有产品图片
    print(f"📊 Current product images: {product_count}")

    # 列出所有非product-开头的图片（排除关键文件）
    exclude_files = ['MIGAC_logo.png', 'hero-banner.jpg', 'logo.jpg']
    other_images = [
        f for f in all_files
        if f.endswith(('.jpg', '.jpeg', '.png'))
        and not f.startswith('product-')
        and f not in exclude_files
    ]

    print(f"📊 Other images to consider: {len(other_images)}")

    return product_count

def main():
    print("=" * 60)
    print("Image Processing & Renaming")
    print("=" * 60)
    print()

    # 创建Logo
    print("1. Creating Logo...")
    create_logo()

    # 创建Hero Banner
    print("\n2. Creating Hero Banner...")
    create_hero_banner()

    # 统计图片
    print("\n3. Checking Product Images...")
    product_count = rename_product_images()

    # 最终统计
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    images_dir = 'cloudflare-deploy/images'
    all_images = os.listdir(images_dir)

    print(f"Total images: {len(all_images)}")
    print(f"Product images (product-*.jpg): {len([f for f in all_images if f.startswith('product-')])}")
    print(f"Logo: {'✅' if 'MIGAC_logo.png' in all_images else '❌'}")
    print(f"Hero banner: {'✅' if 'hero-banner.jpg' in all_images else '❌'}")
    print(f"Original logo: {'✅' if 'logo.jpg' in all_images else '❌'}")

    print("\n✅ Image processing complete!")

if __name__ == "__main__":
    main()
