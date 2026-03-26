#!/usr/bin/env python3
"""
检查并生成中文内容替换方案
"""

import re
import json

# 定义中文到英文的翻译映射
translation_map = {
    # Meta 标签中的
    "义乌市邦邺工艺品厂": "Yiwu Bangye Handicraft Factory",
    "义乌市后宅街道城北路L38": "Chengbei Road L38, Houzhai Street, Yiwu City",
    
    # 通用词汇
    "浏览": "Browse",
    "目录": "Catalog",
    "款式": "Styles",
    "精选": "Featured",
    "展示": "Showcase",
    "卡片": "Card",
    "替换为真实": "Replace with real",
    "图片": "image",
    "产品": "products",
    "立即": "Send",
    "和": "and",
    "联系方式": "Contact Information",
    "我们的专业团队将在": "Our professional team will respond to your inquiry within",
    "小时内回复您的询盘": "hours",
    "中国浙江省浦江县水晶路": "Crystal Road, Pujiang County, Zhejiang Province, China",
    "号": "No.",
    "北京时间": "Beijing Time",
    "请输入您的": "Please enter your",
    "公司名称": "company name",
    "请输入您的公司名称": "Please enter your company name",
    "号码": "number",
    "请输入您的号码": "Please enter your number",
    "咨询": "Inquiry",
    "索要": "Request",
    "请详细描述您的需求": "Please describe your requirements in detail",
    "包括": "including",
    "类型": "type",
    "数量": "quantity",
    "规格": "specifications",
    "等信息": "and other information",
    "常见问题": "FAQ",
    "最小起订量是多少": "What is the Minimum Order Quantity (MOQ)?",
    "大部分": "Most",
    "的最小起订量是": "products have a minimum order quantity of",
    "件": "pieces",
    
    # 产品描述
    "经典水晶烛台": "Classic Crystal Candelabra",
    "优雅设计": "Elegant Design",
    "适合婚庆": "Perfect for Weddings",
    "装饰": "Decorations",
    "礼品等多种场景": "and Gifts",
    "热销": "Best Seller",
    
    # 其他
    "联系": "Contact",
    "关于": "About",
    "下载": "Download",
    "更多": "More",
    "查看": "View",
    "详情": "Details",
    "提交": "Submit",
    "重置": "Reset",
    "姓名": "Name",
    "邮箱": "Email",
    "电话": "Phone",
    "消息": "Message",
    "发送": "Send",
    "收到": "Received",
    "谢谢": "Thank you",
    "我们会尽快回复": "We will reply as soon as possible",
}

def find_chinese_in_file(filename):
    """查找文件中的中文内容"""
    with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找中文字符及其上下文
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    matches = []
    
    for match in chinese_pattern.finditer(content):
        chinese_text = match.group()
        start = max(0, match.start() - 50)
        end = min(len(content), match.end() + 50)
        context = content[start:end]
        
        matches.append({
            'text': chinese_text,
            'context': context,
            'position': match.start()
        })
    
    return matches

# 检查所有文件
files = ['index.html', 'about.html', 'products.html', 'contact.html', 'download.html']

all_matches = {}

print("=" * 80)
print("中文内容检查报告")
print("=" * 80)
print()

for filename in files:
    matches = find_chinese_in_file(filename)
    all_matches[filename] = matches
    
    if matches:
        print(f"\n{filename} - 发现 {len(matches)} 处中文内容:")
        print("-" * 80)
        
        # 去重
        unique_texts = list(set([m['text'] for m in matches]))
        for i, text in enumerate(unique_texts, 1):
            print(f"  {i}. {text}")
    else:
        print(f"\n{filename} - ✅ 无中文内容")

print("\n" + "=" * 80)
print("翻译映射表")
print("=" * 80)
print()

for chinese, english in translation_map.items():
    print(f"{chinese} → {english}")

print("\n" + "=" * 80)
print("总计")
print("=" * 80)

total = sum([len(matches) for matches in all_matches.values()])
print(f"所有文件中文内容总计: {total} 处")
