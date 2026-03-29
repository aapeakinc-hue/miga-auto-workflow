"""
读取MIGAC产品目录PDF内容
"""
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.file.file import File, FileOps

# 创建File对象
pdf_file = File(
    url="assets/MIGAC_CATALOGUE.pdf",
    file_type="document"
)

# 读取PDF内容
print("正在读取PDF内容...")
try:
    content = FileOps.extract_text(pdf_file)
    
    # 保存内容到文件
    with open("assets/catalog_text_content.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ PDF内容读取成功！")
    print(f"📄 内容长度: {len(content)} 字符")
    print(f"💾 已保存到: assets/catalog_text_content.txt")
    
    # 显示前2000个字符作为预览
    print("\n" + "="*60)
    print("内容预览（前2000字符）:")
    print("="*60)
    print(content[:2000])
    print("="*60)
    
except Exception as e:
    print(f"❌ 读取失败: {e}")
    import traceback
    traceback.print_exc()
