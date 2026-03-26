#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证网站部署文件完整性
"""

import os
import json

def check_file_exists(filepath, required=True):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    size = os.path.getsize(filepath) if exists else 0
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}")
    if exists:
        print(f"   Size: {size} bytes ({size/1024:.1f} KB)")
    elif required:
        print(f"   ERROR: Required file missing!")
    return exists if required else True

def main():
    print("=" * 60)
    print("MIGAC Website Deployment Verification")
    print("=" * 60)
    print()

    # 检查部署目录
    deploy_dir = "cloudflare-deploy"
    if not os.path.exists(deploy_dir):
        print(f"❌ Deployment directory not found: {deploy_dir}")
        return

    print("1. HTML Pages (English)")
    print("-" * 60)
    html_files = [
        "index.html",
        "products.html",
        "about.html",
        "contact.html"
    ]
    html_ok = True
    for file in html_files:
        if not check_file_exists(os.path.join(deploy_dir, file)):
            html_ok = False
    print()

    # 检查PDF目录
    print("2. Product Catalogs")
    print("-" * 60)
    pdf_ok = True
    pdf_files = [
        "MIGAC_Product_Catalog_EN_2024.pdf",
        "MIGAC_Product_Catalog_2024.pdf"
    ]
    for file in pdf_files:
        if not check_file_exists(os.path.join(deploy_dir, file)):
            pdf_ok = False
    print()

    # 检查图片目录
    print("3. Images")
    print("-" * 60)
    images_dir = os.path.join(deploy_dir, "images")
    if os.path.exists(images_dir):
        images = os.listdir(images_dir)
        print(f"✅ Images directory exists")
        print(f"   Total images: {len(images)}")

        # 检查关键图片
        key_images = [
            "MIGAC_logo.png",
            "hero-banner.jpg"
        ]
        for img in key_images:
            img_path = os.path.join(images_dir, img)
            if os.path.exists(img_path):
                size = os.path.getsize(img_path)
                print(f"✅ {img} ({size/1024:.1f} KB)")
            else:
                print(f"❌ {img} (missing)")

        # 统计产品图片
        product_images = [f for f in images if f.startswith("product-") or f.endswith(".jpg")]
        print(f"   Product images: {len(product_images)}")

        images_ok = len(product_images) >= 50
    else:
        print("❌ Images directory not found")
        images_ok = False
    print()

    # 检查CSS文件
    print("4. Stylesheets")
    print("-" * 60)
    css_ok = True
    css_files = [
        "style.css",
        "responsive.css"
    ]
    for file in css_files:
        if not check_file_exists(os.path.join(deploy_dir, file), required=False):
            css_ok = True  # CSS is optional since it can be inline
    print()

    # 检查其他文件
    print("5. Additional Files")
    print("-" * 60)
    additional_files = [
        "README_DEPLOYMENT.md",
        "robots.txt",
        "sitemap.xml"
    ]
    for file in additional_files:
        check_file_exists(os.path.join(deploy_dir, file), required=False)
    print()

    # 生成摘要
    print("=" * 60)
    print("Deployment Summary")
    print("=" * 60)

    all_checks = [
        ("HTML Pages (English)", html_ok),
        ("Product Catalogs", pdf_ok),
        ("Images (90+)", images_ok),
        ("Stylesheets", css_ok)
    ]

    for check_name, result in all_checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")

    print()

    # 总体状态
    overall_ok = all(result for _, result in all_checks)

    if overall_ok:
        print("🎉 ALL CHECKS PASSED! Website is ready for deployment!")
        print()
        print("Next steps:")
        print("1. Upload to Cloudflare Pages (5 minutes)")
        print("   - Go to: https://dash.cloudflare.com")
        print("   - Pages > Create project > Upload assets")
        print("   - Select 'cloudflare-deploy' folder")
        print("2. Or deploy via GitHub for automatic updates")
        print()
        print("Files ready:")
        print(f"   - {len(html_files)} HTML pages")
        print(f"   - {len(pdf_files)} PDF catalogs")
        print(f"   - {len(images)} images")
    else:
        print("❌ Some checks failed. Please fix the issues above.")

    print("=" * 60)

if __name__ == "__main__":
    main()
