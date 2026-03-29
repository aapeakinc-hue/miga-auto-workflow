#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理产品图片 - 调整尺寸并优化
"""

from PIL import Image
import os
import shutil

# 源目录和目标目录
source_dir = 'temp-images'
output_dir = 'processed-images'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 最佳图片尺寸
MAX_WIDTH = 800
MAX_HEIGHT = 800
QUALITY = 85

# 需要处理的目录
categories = {
    '烛台白图': 'candle-holders-white',
    '水晶花台图': 'crystal-flower-stands',
    '水晶工艺品': 'crystal-crafts'
}

print("开始处理图片...\n")

for src_cat, dst_cat in categories.items():
    src_path = os.path.join(source_dir, src_cat)
    dst_path = os.path.join(output_dir, dst_cat)

    if not os.path.exists(src_path):
        print(f"跳过 {src_cat}（目录不存在）")
        continue

    os.makedirs(dst_path, exist_ok=True)

    # 获取所有图片文件
    image_files = [f for f in os.listdir(src_path)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    print(f"处理 {src_cat}: {len(image_files)} 张图片")

    processed = 0
    for i, filename in enumerate(image_files):
        src_file = os.path.join(src_path, filename)
        dst_file = os.path.join(dst_path, filename)

        try:
            # 打开图片
            img = Image.open(src_file)

            # 转换为RGB（如果是RGBA）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # 计算新尺寸（保持宽高比）
            width, height = img.size
            if width > height:
                # 横向图片
                if width > MAX_WIDTH:
                    new_width = MAX_WIDTH
                    new_height = int(height * MAX_WIDTH / width)
                else:
                    new_width, new_height = width, height
            else:
                # 纵向图片
                if height > MAX_HEIGHT:
                    new_height = MAX_HEIGHT
                    new_width = int(width * MAX_HEIGHT / height)
                else:
                    new_width, new_height = width, height

            # 调整大小
            if new_width != width or new_height != height:
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 保存图片
            img.save(dst_file, 'JPEG', quality=QUALITY, optimize=True)
            processed += 1

            if (i + 1) % 10 == 0:
                print(f"  已处理 {i + 1}/{len(image_files)}...")

        except Exception as e:
            print(f"  错误: {filename} - {e}")

    print(f"  完成！成功处理 {processed} 张图片\n")

print("所有图片处理完成！")
print(f"输出目录: {output_dir}")
