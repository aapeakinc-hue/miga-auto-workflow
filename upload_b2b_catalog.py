#!/usr/bin/env python3
"""
上传MIGAC B2B产品目录PDF到对象存储
"""

import os
from pathlib import Path
from coze_coding_dev_sdk.s3 import S3SyncStorage


def upload_b2b_catalog():
    """上传B2B目录PDF到对象存储"""
    print("=" * 70)
    print("MIGAC B2B 产品目录 PDF 上传")
    print("=" * 70)
    print()
    
    # 初始化S3存储客户端
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    
    # PDF文件路径
    pdf_file = "assets/MIGAC_B2B_CATALOG_2026.pdf"
    
    # 检查文件是否存在
    if not os.path.exists(pdf_file):
        print(f"❌ 错误: PDF文件不存在 - {pdf_file}")
        return None
    
    file_path = Path(pdf_file)
    file_size = file_path.stat().st_size / 1024  # KB
    
    print(f"📄 PDF文件: {pdf_file}")
    print(f"📊 文件大小: {file_size:.2f} KB")
    print()
    
    try:
        # 上传文件
        with open(pdf_file, "rb") as f:
            print("🚀 正在上传到对象存储...")
            print(f"   文件: MIGAC_B2B_CATALOG_2026.pdf")
            print()
            
            # 上传文件
            file_key = storage.stream_upload_file(
                fileobj=f,
                file_name="MIGAC_B2B_CATALOG_2026.pdf",
                content_type="application/pdf",
                bucket=None,
                multipart_chunksize=5 * 1024 * 1024,
                multipart_threshold=5 * 1024 * 1024,
                max_concurrency=1,
                use_threads=False,
            )
            
            print("✅ 上传成功!")
            print(f"📦 对象Key: {file_key}")
            print()
        
        # 生成7天有效期的访问链接
        print("🔗 生成下载链接...")
        access_url = storage.generate_presigned_url(
            key=file_key,
            expire_time=604800  # 7天 = 7 * 24 * 3600秒
        )
        
        print("✅ 下载链接生成成功!")
        print()
        print("=" * 70)
        print("📋 下载信息")
        print("=" * 70)
        print(f"🔗 下载链接:")
        print(f"{access_url}")
        print()
        print(f"⏰ 有效期: 7天")
        print(f"📄 文件名: MIGAC_B2B_CATALOG_2026.pdf")
        print(f"📊 文件大小: {file_size:.2f} KB")
        print()
        print("💡 提示:")
        print("  • 点击链接即可下载PDF")
        print("  • 链接7天内有效")
        print("  • 请及时下载保存")
        print("  • 专业B2B风格，符合国际标准")
        print("=" * 70)
        
        return access_url
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    upload_b2b_catalog()
