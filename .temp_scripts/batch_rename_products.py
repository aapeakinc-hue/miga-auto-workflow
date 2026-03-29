#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名产品图片为标准格式
"""

import os
import shutil

def rename_product_images():
    """重命名所有产品图片为 product-*.jpg 格式"""
    images_dir = 'cloudflare-deploy/images'

    # 获取所有图片
    all_files = os.listdir(images_dir)

    # 排除已经重命名的文件和关键文件
    exclude_files = [
        'MIGAC_logo.png',
        'hero-banner.jpg',
        'logo.jpg',
        'product-1.jpg',
        'product-2.jpg',
        'product-3.jpg',
        'product-4.jpg',
        'product-5.jpg',
        'product-6.jpg',
        'product-7.jpg',
        'product-8.jpg'
    ]

    # 找到需要重命名的图片
    to_rename = [
        f for f in all_files
        if f.endswith(('.jpg', '.jpeg'))
        and not f.startswith('product-')
        and f not in exclude_files
    ]

    print(f"找到 {len(to_rename)} 张需要重命名的产品图片")

    # 按文件大小排序（大的通常更好）
    to_rename_with_size = []
    for f in to_rename:
        size = os.path.getsize(os.path.join(images_dir, f))
        to_rename_with_size.append((f, size))

    # 按大小降序排序
    to_rename_with_size.sort(key=lambda x: x[1], reverse=True)

    # 重命名（从 product-9 开始）
    counter = 9
    renamed_count = 0

    for old_name, size in to_rename_with_size:
        if counter > 50:  # 最多重命名50张
            break

        new_name = f"product-{counter}.jpg"
        old_path = os.path.join(images_dir, old_name)
        new_path = os.path.join(images_dir, new_name)

        try:
            shutil.copy2(old_path, new_path)
            renamed_count += 1
            counter += 1
            print(f"✓ {old_name} ({size/1024:.1f} KB) -> {new_name}")
        except Exception as e:
            print(f"✗ {old_name} 失败: {e}")

    print(f"\n总共重命名: {renamed_count} 张图片")

    # 统计
    product_images = [f for f in os.listdir(images_dir) if f.startswith('product-')]
    print(f"当前 product-*.jpg 文件: {len(product_images)} 个")

    return renamed_count

if __name__ == "__main__":
    rename_product_images()
