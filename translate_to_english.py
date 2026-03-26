#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译HTML页面为英文
"""

import os
import re

# 翻译映射
translations = {
    # 通用词汇
    "首页": "Home",
    "产品": "Products",
    "关于我们": "About Us",
    "联系我们": "Contact Us",
    "获取免费报价": "Get Free Quote",
    "浏览产品目录": "Browse Products",
    "年行业经验": "Years Experience",
    "国际客户": "International Clients",
    "产品款式": "Product Styles",
    "出口国家": "Export Countries",
    "精选产品展示": "Featured Products",
    "我们提供各类水晶烛台、水晶工艺品，满足不同客户需求": "We provide a wide range of crystal candle holders and crafts to meet diverse customer needs",
    "为什么选择 MIGAC？": "Why Choose MIGAC?",
    "联系我们": "Contact Us",
    "如果您有任何需求或问题，欢迎随时与我们联系": "If you have any requirements or questions, please feel free to contact us",
    "邮箱": "Email",
    "电话": "Phone",
    "WhatsApp": "WhatsApp",
    "网站": "Website",
    "地址": "Address",
    "发送询盘": "Send Inquiry",
    "填写下方表单，我们会尽快与您联系": "Fill in the form below and we will contact you as soon as possible",
    "姓名": "Name",
    "请输入您的姓名": "Please enter your name",
    "邮箱": "Email",
    "请输入您的邮箱": "Please enter your email",
    "国家": "Country",
    "请输入您的国家": "Please enter your country",
    "询盘类型": "Inquiry Type",
    "产品咨询": "Product Inquiry",
    "价格咨询": "Price Inquiry",
    "定制订单": "Custom Order",
    "批发咨询": "Wholesale Inquiry",
    "索要产品目录": "Request Product Catalog",
    "其他": "Other",
    "留言": "Message",
    "请详细描述您的需求，包括产品类型、数量、规格等信息": "Please describe your requirements in detail, including product type, quantity, specifications, etc.",
    "提交询盘": "Submit Inquiry",
    "专业水晶烛台制造商": "Professional Crystal Candle Holder Manufacturer",
    "10+年工厂直销": "10+ Years Factory Direct",
    "服务182+国际客户，支持OEM/ODM定制，为您提供高品质水晶工艺品": "Serving 182+ international clients, supporting OEM/ODM customization, providing you with high-quality crystal crafts",
    "产品展示": "Products",
    "产品": "Product",
    "产品名称": "Product Name",
    "产品描述": "Product Description",
    "产品展示": "Product Display",
    "产品中心": "Products Center",
    "产品目录": "Product Catalog",
    "热销产品": "Best Sellers",
    "定制服务": "Custom Services",
    "关于我们": "About Us",
    "公司简介": "Company Profile",
    "发展历程": "Company History",
    "企业文化": "Company Culture",
    "服务时间": "Business Hours",
    "周一至周五": "Monday to Friday",
    "隐私政策": "Privacy Policy",
    "服务条款": "Terms of Service",
    "下载产品目录": "Download Product Catalog",
    "工厂直销，价格优势": "Factory Direct, Competitive Pricing",
    "OEM/ODM定制服务": "OEM/ODM Customization Service",
    "质量保证，符合ISO标准": "Quality Assurance, ISO Certified",
    "小批量起订，灵活合作": "Low MOQ, Flexible Cooperation",
    "快速响应，准时交付": "Fast Response, On-Time Delivery",
    "专业团队，全程服务": "Professional Team, Full-Service Support",
}

def translate_html_file(input_file, output_file):
    """翻译HTML文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 翻译关键词
    for zh, en in translations.items():
        content = content.replace(zh, en)
    
    # 更改HTML语言标签
    content = content.replace('lang="zh-CN"', 'lang="en"')
    
    # 更改meta描述
    content = re.sub(
        r'meta name="description" content="[^"]*"',
        'meta name="description" content="MIGAC - Professional crystal candle holder manufacturer with 10+ years experience. Serving 182+ international clients, factory direct, supporting OEM/ODM customization. Get free quote and product catalog."',
        content
    )
    
    # 更改标题
    content = re.sub(
        r'<title>[^<]*</title>',
        '<title>Professional Crystal Candle Holder Manufacturer - MIGAC | Factory Direct | Free Quote</title>',
        content
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Translated: {input_file} -> {output_file}")

# 翻译所有HTML文件
html_files = [
    'cloudflare-deploy/index.html',
    'cloudflare-deploy/products.html',
    'cloudflare-deploy/about.html',
    'cloudflare-deploy/contact.html',
]

for html_file in html_files:
    if os.path.exists(html_file):
        translate_html_file(html_file, html_file)
        print(f"  ✓ {html_file} translated to English")
    else:
        print(f"  ✗ {html_file} not found")

print("\n✅ All HTML files translated to English!")
