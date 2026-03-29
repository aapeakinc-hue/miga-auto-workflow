#!/usr/bin/env python3
"""
为MIGAC B2B产品目录添加图片占位符
"""

import re
from pathlib import Path

# 根据产品系列确定图标
series_icons = {
    'MG-CA': '🕯️',
    'MG-FS': '🌸',
    'MG-CH': '🕯️',
    'MG-CS': '🎂'
}

def add_product_image(html_content):
    """为所有产品卡片添加图片占位符"""
    
    # 匹配产品卡片中的product-badges和product-model之间的部分
    pattern = r'(<div class="product-badges">.*?</div>\s*)(<div class="product-model">MG-[A-Z]{2}-\d+</div>)'
    
    def replace_func(match):
        badges = match.group(1)
        model_div = match.group(2)
        
        # 提取型号
        model_match = re.search(r'MG-[A-Z]{2}-\d+', model_div)
        if not model_match:
            return match.group(0)
        
        model = model_match.group(0)
        # 获取系列代码
        series_code = model[:5]
        icon = series_icons.get(series_code, '✨')
        
        # 创建图片占位符HTML
        image_html = f'''                    <div class="product-image">
                        <span class="product-image-icon">{icon}</span>
                        <div class="product-image-text">{model}</div>
                    </div>
'''
        
        return badges + image_html + model_div
    
    # 执行替换
    new_content = re.sub(pattern, replace_func, html_content, flags=re.DOTALL)
    
    return new_content

def main():
    """主函数"""
    print("=" * 70)
    print("为MIGAC B2B产品目录添加图片占位符")
    print("=" * 70)
    print()
    
    input_file = "assets/MIGAC_B2B_CATALOG.html"
    output_file = "assets/MIGAC_B2B_CATALOG.html"
    
    # 读取HTML文件
    print(f"📖 读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 添加图片占位符
    print("🖼️ 添加图片占位符...")
    new_content = add_product_image(html_content)
    
    # 保存文件
    print(f"💾 保存文件: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print()
    print("✅ 完成!")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
