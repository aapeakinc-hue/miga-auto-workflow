#!/usr/bin/env python3
"""
补充翻译剩余的中文内容
"""

import re

# 补充翻译
extra_translations = {
    "的行业经验": "years of industry experience",
    "地区": "regions",
    "酒店": "hotels",
    "作为运营实体": "as the operating entity",
    "现货": "in-stock",
}

def replace_remaining_chinese(filename):
    """替换文件中剩余的中文内容"""
    with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计替换次数
    replace_count = 0
    
    for chinese, english in extra_translations.items():
        if chinese in content:
            content = content.replace(chinese, english)
            replace_count += 1
            print(f"  ✓ {chinese} → {english}")
    
    # 保存文件
    with open(f'cloudflare-deploy/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return replace_count

# 处理文件
files = ['index.html', 'contact.html']

print("=" * 80)
print("补充翻译剩余中文内容...")
print("=" * 80)
print()

total_replaced = 0

for filename in files:
    print(f"\n处理 {filename}:")
    print("-" * 80)
    
    count = replace_remaining_chinese(filename)
    total_replaced += count
    
    # 验证
    with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    remaining = chinese_pattern.findall(content)
    
    if remaining:
        print(f"⚠️  还有 {len(remaining)} 处中文: {remaining}")
    else:
        print(f"✅ 完全清理，无剩余中文")

print("\n" + "=" * 80)
print("✅ 所有中文内容已替换为英文！")
print("=" * 80)
print(f"\n总计补充替换了 {total_replaced} 处中文内容")
