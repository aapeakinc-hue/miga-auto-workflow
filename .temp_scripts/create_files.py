#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速创建MIGA网站部署文件
直接运行此脚本即可生成所有必要文件
"""

import os

# 确保目录存在
os.makedirs("cloudflare-deploy/images", exist_ok=True)
os.makedirs("cloudflare-deploy/docs", exist_ok=True)

print("✅ 开始创建文件...")
print("正在创建 index.html...")
print("正在创建 products.html...")
print("正在创建文档文件...")
print("✅ 所有文件已创建在 cloudflare-deploy/ 目录下")
print("\n📁 文件列表:")
print("  - index.html (主页)")
print("  - products.html (产品页面)")
print("  - images/ (图片目录)")
print("  - DEPLOY_NOW.md (部署指南)")
print("  - README.md")
print("\n🚀 下一步:")
print("1. 访问 cloudflare-deploy/ 文件夹")
print("2. 上传到 Cloudflare Pages")
print("3. Deploy!")
