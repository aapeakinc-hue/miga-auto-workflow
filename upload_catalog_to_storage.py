"""
上传PDF目录册到对象存储
使用storage技能将PDF上传到S3对象存储
"""

import os
from pathlib import Path
from coze_coding_dev_sdk.s3 import S3SyncStorage


class CatalogUploader:
    """目录册上传器"""
    
    def __init__(self):
        # 初始化S3存储客户端
        self.storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
    
    def upload_catalog(self, local_file_path: str = "assets/MIGAC_Catalog_2026.pdf") -> dict:
        """
        上传目录册到对象存储
        
        Args:
            local_file_path: 本地PDF文件路径
            
        Returns:
            包含key和url的字典
        """
        print("=" * 60)
        print("上传PDF目录册到对象存储")
        print("=" * 60)
        print()
        
        # 检查本地文件是否存在
        file_path = Path(local_file_path)
        if not file_path.exists():
            print(f"❌ 错误: 文件不存在 - {local_file_path}")
            return None
        
        print(f"📄 本地文件: {local_file_path}")
        print(f"📊 文件大小: {file_path.stat().st_size / 1024:.2f} KB")
        print()
        
        try:
            # 使用流式上传
            with open(local_file_path, "rb") as f:
                print("🚀 正在上传到对象存储...")
                
                # 上传文件
                file_key = self.storage.stream_upload_file(
                    fileobj=f,
                    file_name="MIGAC_Catalog_2026.pdf",
                    content_type="application/pdf",
                    bucket=None,
                    multipart_chunksize=5 * 1024 * 1024,
                    multipart_threshold=5 * 1024 * 1024,
                    max_concurrency=1,
                    use_threads=False,
                )
                
                print(f"✅ 上传成功!")
                print(f"📦 对象Key: {file_key}")
                print()
                
                # 生成永久访问URL（7天有效期）
                print("🔗 生成访问链接...")
                access_url = self.storage.generate_presigned_url(
                    key=file_key,
                    expire_time=604800  # 7天 = 7 * 24 * 3600秒
                )
                
                print(f"✅ 访问链接生成成功!")
                print(f"🔗 下载链接: {access_url}")
                print(f"⏰ 有效期: 7天")
                print()
                
                return {
                    "file_key": file_key,
                    "access_url": access_url,
                    "local_file": str(file_path),
                    "status": "success"
                }
                
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }
    
    def save_upload_info(self, upload_result: dict):
        """保存上传信息到文件"""
        if upload_result and upload_result.get("status") == "success":
            info_file = Path("assets/catalog_upload_info.json")
            
            upload_info = {
                "file_key": upload_result["file_key"],
                "access_url": upload_result["access_url"],
                "upload_time": "2026-03-30",
                "expire_days": 7,
                "status": "success"
            }
            
            import json
            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(upload_info, f, ensure_ascii=False, indent=2)
            
            print(f"📄 上传信息已保存到: {info_file}")
            
            # 同时保存URL到文本文件
            url_file = Path("assets/catalog_permanent_url.txt")
            with open(url_file, "w") as f:
                f.write(upload_result["access_url"])
            
            print(f"📄 URL链接已保存到: {url_file}")


def main():
    """主函数"""
    # 初始化上传器
    uploader = CatalogUploader()
    
    # 上传目录册
    result = uploader.upload_catalog()
    
    if result and result.get("status") == "success":
        print()
        print("=" * 60)
        print("上传完成")
        print("=" * 60)
        print(f"📦 对象Key: {result['file_key']}")
        print(f"🔗 下载链接: {result['access_url']}")
        print(f"⏰ 有效期: 7天")
        print()
        
        # 保存上传信息
        uploader.save_upload_info(result)
        
        print()
        print("提示:")
        print("1. 点击链接下载PDF文件")
        print("2. 链接7天内有效")
        print("3. 可以下载后保存到本地")
        print("4. 可以发送给客户使用")
        print()
    else:
        print()
        print("=" * 60)
        print("上传失败")
        print("=" * 60)
        print(f"错误: {result.get('error', 'Unknown error')}")
        print()


if __name__ == "__main__":
    main()
