"""
生成MIGAC产品目录册PDF
使用document-generation技能从Markdown生成PDF
"""

import os
import json
from pathlib import Path
from coze_coding_dev_sdk import DocumentGenerationClient, PDFConfig


class CatalogPDFGenerator:
    """目录册PDF生成器"""
    
    def __init__(self):
        # 配置PDF参数
        pdf_config = PDFConfig(
            page_size="A4",
            left_margin=72,
            right_margin=72,
            top_margin=72,
            bottom_margin=36
        )
        
        self.client = DocumentGenerationClient(pdf_config=pdf_config)
        self.catalog_data = self.load_catalog_data()
    
    def load_catalog_data(self):
        """加载目录册数据"""
        data_file = Path("assets/catalog_data.json")
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_markdown_content(self) -> str:
        """生成Markdown内容"""
        company = self.catalog_data.get('company_info', {})
        categories = self.catalog_data.get('product_categories', [])
        images = self.catalog_data.get('product_images', [])
        advantages = self.catalog_data.get('key_advantages', [])
        services = self.catalog_data.get('services', [])
        contact = self.catalog_data.get('contact_info', {})
        
        # 构建Markdown内容
        markdown = f"""# MIGAC
## Luxury Crystal Candelabras & Home Decor

---

## Welcome to MIGAC

**{company.get('company_name', '')}**

{company.get('description', '')}

### Why Choose MIGAC?

{''.join([f"- {adv}\n" for adv in advantages])}

---

## Our Products

"""

        # 添加产品分类
        for i, category in enumerate(categories, 1):
            markdown += f"""### {i}. {category.get('category', '')}

{category.get('description', '')}

**Features:**
{''.join([f"- {feature}\n" for feature in category.get('features', [])])}

**Specifications:**
- MOQ: {category.get('moq', '')}
- Lead Time: {category.get('lead_time', '')}

---

"""

        # 添加产品展示
        markdown += "## Product Showcase\n\n"
        
        for i, img in enumerate(images[:12], 1):  # 限制12张图片
            img_name = img.get('name', f'Product {i}')
            img_path = img.get('path', '')
            # 注意：本地图片无法在PDF中直接显示，这里只显示产品名称
            markdown += f"### Product {i}: {img_name}\n\n"
            markdown += f"Size: {img.get('size_mb', 0)}MB\n\n"
            markdown += "---\n\n"
        
        # 添加服务
        markdown += "## Our Services\n\n"
        markdown += ''.join([f"- {service}\n" for service in services])
        markdown += "\n\n"
        
        # 添加联系方式
        markdown += "---\n\n"
        markdown += "## Contact Us\n\n"
        markdown += f"""**Company:** {company.get('company_name', '')}

**Email:** {contact.get('sales_team', '')}

**Website:** {company.get('website', '')}

**Phone:** {company.get('phone', '')}

**Address:** {company.get('address', '')}

---

### Get Your Free Quote Today!

We offer free samples and competitive pricing. Contact our sales team for more information.

**MIGAC - Your Trusted Crystal Decor Partner**

© 2026 Yiwu Bangye Handicraft Factory. All Rights Reserved.
"""
        
        return markdown
    
    def generate_pdf(self) -> str:
        """生成PDF"""
        print("正在生成PDF目录册...")
        
        markdown_content = self.generate_markdown_content()
        
        try:
            # 生成PDF
            pdf_url = self.client.create_pdf_from_markdown(
                markdown_content,
                "MIGAC_Catalog_2026"
            )
            
            print(f"✅ PDF目录册生成成功!")
            print(f"📄 下载链接: {pdf_url}")
            print(f"⏰ 有效期: 24小时")
            
            return pdf_url
            
        except Exception as e:
            print(f"❌ 生成PDF失败: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """主函数"""
    print("=" * 60)
    print("MIGAC 产品目录册 PDF 生成器")
    print("=" * 60)
    print()
    
    # 初始化生成器
    generator = CatalogPDFGenerator()
    
    # 生成PDF
    pdf_url = generator.generate_pdf()
    
    if pdf_url:
        print()
        print("=" * 60)
        print("目录册已生成")
        print("=" * 60)
        print(f"下载链接: {pdf_url}")
        print()
        print("提示:")
        print("1. 点击链接下载PDF文件")
        print("2. 24小时内有效，请及时下载")
        print("3. 可以发送给客户或打印使用")
        print()
        
        # 保存链接到文件
        with open("assets/catalog_pdf_url.txt", "w") as f:
            f.write(pdf_url)
        print(f"链接已保存到: assets/catalog_pdf_url.txt")


if __name__ == "__main__":
    main()
