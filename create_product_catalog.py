"""
创建MIGAC产品目录册
根据现有产品信息和图片，生成简洁大方的产品目录册
"""

import os
import json
from typing import List, Dict, Any
from pathlib import Path

class ProductCatalogGenerator:
    """产品目录册生成器"""
    
    def __init__(self, base_path: str = "assets"):
        self.base_path = Path(base_path)
        self.products = []
        
    def collect_product_images(self) -> List[Dict[str, str]]:
        """收集产品图片"""
        print("正在收集产品图片...")
        
        product_images = []
        image_extensions = ['.jpg', '.jpeg', '.png']
        
        # 常见的产品图片名称模式
        product_patterns = [
            'candle',
            'crystal',
            'candelabra',
            'decor',
            'holder',
            'chandelier'
        ]
        
        # 遍历assets目录
        for file_path in self.base_path.rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                # 排除临时文件和截图
                if any(skip in str(file_path).lower() for skip in ['wechat', 'temp', 'screenshot', 'qq', '新增']):
                    continue
                
                file_name = file_path.name.lower()
                
                # 检查是否是产品图片
                if any(pattern in file_name for pattern in product_patterns):
                    file_size = file_path.stat().st_size
                    
                    # 只保留大于50KB的图片（避免小图标）
                    if file_size > 50 * 1024:  # 50KB
                        product_images.append({
                            'path': str(file_path),
                            'name': file_path.stem,
                            'size': file_size,
                            'size_mb': round(file_size / (1024 * 1024), 2)
                        })
        
        # 按文件大小排序（大文件优先）
        product_images.sort(key=lambda x: x['size'], reverse=True)
        
        print(f"找到 {len(product_images)} 张产品图片")
        return product_images[:20]  # 限制20张图片
    
    def get_company_info(self) -> Dict[str, str]:
        """获取公司信息"""
        return {
            'company_name': 'Yiwu Bangye Handicraft Factory',
            'brand_name': 'MIGAC',
            'website': 'https://miga.cc',
            'email': 'info@miga.cc',
            'phone': '+86-19879476613',
            'address': 'Yiwu, Zhejiang, China',
            'description': 'Professional Manufacturer of Crystal Candelabras & Home Decor',
            'experience': '10+ Years',
            'customers': '200+',
            'countries': '50+'
        }
    
    def get_product_categories(self) -> List[Dict[str, Any]]:
        """获取产品分类"""
        return [
            {
                'category': 'Crystal Candelabras',
                'description': 'Elegant crystal candelabras for weddings, events, and luxury home decor',
                'features': [
                    'High-quality K9 crystal',
                    'Multiple arm designs',
                    'Candle or LED options',
                    'Customizable heights'
                ],
                'moq': '10 pieces',
                'lead_time': '7-15 days'
            },
            {
                'category': 'Candle Holders',
                'description': 'Beautiful crystal and glass candle holders for table decoration',
                'features': [
                    'Premium materials',
                    'Various styles available',
                    'Perfect for events',
                    'Competitive pricing'
                ],
                'moq': '20 pieces',
                'lead_time': '7-10 days'
            },
            {
                'category': 'Home Decor',
                'description': 'Crystal decorative items for home and commercial spaces',
                'features': [
                    'Modern designs',
                    'Durable quality',
                    'Easy maintenance',
                    'Packaging included'
                ],
                'moq': '30 pieces',
                'lead_time': '10-15 days'
            }
        ]
    
    def generate_catalog_content(self) -> Dict[str, Any]:
        """生成目录册内容"""
        print("正在生成目录册内容...")
        
        company_info = self.get_company_info()
        product_images = self.collect_product_images()
        product_categories = self.get_product_categories()
        
        catalog_content = {
            'company_info': company_info,
            'product_categories': product_categories,
            'product_images': product_images,
            'key_advantages': [
                '10+ Years Manufacturing Experience',
                '200+ Satisfied Customers Worldwide',
                'Export to 50+ Countries',
                '100% Quality Inspection',
                'Competitive Factory Prices',
                'Custom Design Available'
            ],
            'services': [
                'OEM/ODM Services',
                'Free Samples Available',
                'Fast Delivery',
                'Quality Guarantee',
                'After-sales Support'
            ],
            'contact_info': {
                'sales_team': 'sales@miga.cc',
                'website': 'https://miga.cc',
                'whatsapp': '+86-19879476613'
            }
        }
        
        return catalog_content
    
    def save_catalog_data(self, catalog_content: Dict[str, Any], filename: str = "catalog_data.json"):
        """保存目录册数据"""
        output_path = self.base_path / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog_content, f, ensure_ascii=False, indent=2)
        print(f"目录册数据已保存到: {output_path}")
        return str(output_path)


def main():
    """主函数"""
    print("=" * 60)
    print("MIGAC 产品目录册生成器")
    print("=" * 60)
    print()
    
    # 初始化生成器
    generator = ProductCatalogGenerator(base_path="assets")
    
    # 生成目录册内容
    catalog_content = generator.generate_catalog_content()
    
    # 保存数据
    data_file = generator.save_catalog_data(catalog_content)
    
    # 显示摘要
    print()
    print("=" * 60)
    print("目录册生成完成")
    print("=" * 60)
    print(f"公司名称: {catalog_content['company_info']['company_name']}")
    print(f"品牌: {catalog_content['company_info']['brand_name']}")
    print(f"产品分类数: {len(catalog_content['product_categories'])}")
    print(f"产品图片数: {len(catalog_content['product_images'])}")
    print(f"数据文件: {data_file}")
    print()
    
    # 显示产品分类
    print("产品分类:")
    for i, category in enumerate(catalog_content['product_categories'], 1):
        print(f"  {i}. {category['category']}")
        print(f"     - {category['description']}")
        print(f"     - MOQ: {category['moq']}")
        print(f"     - 交期: {category['lead_time']}")
    print()


if __name__ == "__main__":
    main()
