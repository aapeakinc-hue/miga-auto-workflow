#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建MIGAC产品目录PDF
符合国际B2B标准
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# 创建PDF
output_file = '/workspace/projects/cloudflare-deploy/MIGAC_Catalog_2024.pdf'
doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

# 创建样式
styles = getSampleStyleSheet()

# 自定义样式
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1a237e'),
    alignment=TA_CENTER,
    spaceAfter=20
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=colors.HexColor('#0d47a1'),
    spaceAfter=15
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#333333')
)

product_title_style = ParagraphStyle(
    'ProductTitle',
    parent=styles['Heading3'],
    fontSize=14,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=5
)

# 内容容器
content = []

# === 封面 ===
content.append(Spacer(0, 2*cm))

# 标题
content.append(Paragraph("MIGAC", title_style))
content.append(Paragraph("Professional Crystal Candle Holder Manufacturer", ParagraphStyle('Custom', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#666666'), alignment=TA_CENTER, spaceAfter=10)))
content.append(Paragraph("产品目录 | Product Catalogue 2024", ParagraphStyle('Custom', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#ffd700'), alignment=TA_CENTER, spaceAfter=20)))

# 公司信息
company_info = """
<para align=center spaceb=12>
<font size=10>专业水晶工艺品制造商 | 10+年工厂直销</font><br/>
<font size=10>服务182+国际客户 | 产品出口50+国家</font><br/>
<font size=10>支持OEM/ODM定制 | ISO 9001认证</font>
</para>
"""
content.append(Paragraph(company_info, ParagraphStyle('Custom', parent=styles['BodyText'])))

content.append(Spacer(0, 2*cm))

# Logo (如果存在)
logo_path = '/workspace/projects/cloudflare-deploy/images/logo.jpg'
if os.path.exists(logo_path):
    try:
        logo = Image(logo_path, width=4*cm, height=2*cm)
        logo.hAlign = 'CENTER'
        content.append(logo)
    except:
        pass

content.append(Spacer(0, 2*cm))

# 联系信息
contact_table_data = [
    ['Email', 'info@miga.cc'],
    ['Phone', '+86-19879476613'],
    ['WhatsApp', '+86-19879476613'],
    ['Website', 'www.miga.cc'],
    ['Address', 'No.888 Shuijing Road, Pujiang County, Zhejiang, China'],
]

contact_table = Table(contact_table_data, colWidths=[3*cm, 9*cm])
contact_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
]))

contact_table.hAlign = 'CENTER'
content.append(contact_table)

content.append(PageBreak())

# === 关于我们 ===
content.append(Paragraph("关于我们 | About Us", title_style))

about_text = """
<para spaceb=12>
<font size=10><b>MIGAC</b> is a professional crystal craft manufacturer based in Pujiang County, Zhejiang Province - the famous "Crystal Capital of the World". With 10+ years of industry experience, we specialize in manufacturing high-quality crystal candle holders, crystal chandeliers, and crystal decorations.</font>
</para>
<para spaceb=12>
<font size=10>Our factory covers an area of 5,000 square meters, equipped with advanced production facilities and a skilled technical team. From design, development to production and quality inspection, every step is strictly controlled to ensure product quality meets international standards.</font>
</para>
<para spaceb=12>
<font size=10>With premium products and professional services, our products are exported to 50+ countries and regions including the USA, Europe, Middle East, and Southeast Asia. We have served 182+ international clients including wholesalers, retailers, hotels, and wedding companies.</font>
</para>
"""

content.append(Paragraph(about_text, body_style))
content.append(Spacer(0, 1*cm))

# 核心优势
content.append(Paragraph("核心优势 | Core Advantages", subtitle_style))

advantages_data = [
    ['🏭 Factory Direct', 'Manufacturer direct sales, competitive pricing'],
    ['🎨 OEM/ODM', 'Professional design team, custom solutions'],
    ['✅ Quality Assurance', 'ISO 9001 certified, strict quality control'],
    ['📦 Low MOQ', 'Flexible MOQ, small trial orders welcome'],
    ['⚡ Fast Response', '24-hour response, on-time delivery'],
    ['🌍 Global Shipping', 'Worldwide delivery, customs clearance expertise'],
]

advantages_table = Table(advantages_data, colWidths=[4*cm, 8*cm])
advantages_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
]))

content.append(advantages_table)
content.append(PageBreak())

# === 产品展示 ===
content.append(Paragraph("产品目录 | Product Catalogue", title_style))

# 产品列表
products = [
    {
        'name': '5 Arms Candelabra',
        'name_cn': '五臂烛台',
        'image': 'product-1.jpg',
        'category': 'Candelabra',
        'description': 'Elegant 5-arm design, made from premium K9 crystal, exquisite cutting technique, excellent light refraction. Perfect for weddings, home decoration, hotels, and banquets.',
        'description_cn': '优雅的五臂设计，采用优质K9水晶制作，切割工艺精湛，光线折射效果出色。适合婚庆、家居装饰、酒店宴会等多种场景。',
        'material': 'K9 Crystal',
        'size': 'Customizable',
        'moq': '50 PCS',
        'lead_time': '15-20 days'
    },
    {
        'name': '9 Arms Candelabra',
        'name_cn': '九臂烛台',
        'image': 'product-2.jpg',
        'category': 'Candelabra',
        'description': 'Luxurious 9-arm candelabra, multi-layer crystal design, grand and elegant. Ideal for hotel lobbies, banquet halls, and high-end restaurants.',
        'description_cn': '奢华九臂烛台，多层水晶设计，华丽大气。适合酒店大堂、宴会厅、高端餐厅使用。',
        'material': 'K9 Crystal',
        'size': 'Customizable',
        'moq': '10 PCS',
        'lead_time': '20-25 days'
    },
    {
        'name': 'Classic Candlestick',
        'name_cn': '经典烛台',
        'image': 'product-3.jpg',
        'category': 'Candlestick',
        'description': 'Classic single candlestick design, simple and elegant. Hand-polished K9 crystal, smooth finish. Suitable for dining tables, mantels, and living room decoration.',
        'description_cn': '经典单烛台设计，简洁优雅。手工抛光K9水晶，表面光滑。适合餐桌、壁炉架、客厅装饰。',
        'material': 'K9 Crystal',
        'size': 'Multiple sizes',
        'moq': '100 PCS',
        'lead_time': '10-15 days'
    },
    {
        'name': 'Crystal Candle Holders',
        'name_cn': '水晶烛台',
        'image': 'product-4.jpg',
        'category': 'Candle Holder',
        'description': 'Modern crystal candle holder set, premium quality, multiple styles available. Perfect for weddings, parties, and special events.',
        'description_cn': '现代水晶烛台套装，优质品质，多种款式可选。完美适用于婚礼、派对和特殊场合。',
        'material': 'K9 Crystal',
        'size': 'Various',
        'moq': '50 PCS',
        'lead_time': '15-20 days'
    },
    {
        'name': 'Crystal Bubble Stand',
        'name_cn': '水晶气泡台',
        'image': 'product-5.jpg',
        'category': 'Decorative Stand',
        'description': 'Unique crystal bubble stand design, artistic and elegant. Excellent light refraction creates stunning visual effects. Great for display and decoration.',
        'description_cn': '独特的水晶气泡台设计，艺术感强，优雅精致。出色的光线折射创造令人惊叹的视觉效果。适合展示和装饰。',
        'material': 'K9 Crystal',
        'size': 'Customizable',
        'moq': '50 PCS',
        'lead_time': '15-20 days'
    },
    {
        'name': 'Color Candelabra',
        'name_cn': '彩色烛台',
        'image': 'product-6.jpg',
        'category': 'Candelabra',
        'description': 'Colorful crystal candelabra, vibrant colors, eye-catching design. Available in various colors to match different themes.',
        'description_cn': '彩色水晶烛台，色彩鲜艳，设计吸睛。提供多种颜色选择，匹配不同主题。',
        'material': 'K9 Crystal',
        'size': 'Customizable',
        'moq': '50 PCS',
        'lead_time': '15-20 days'
    },
    {
        'name': 'Crystal Stand',
        'name_cn': '水晶台',
        'image': 'product-7.jpg',
        'category': 'Stand',
        'description': 'Simple yet elegant crystal stand, versatile design. Can be used as candle holder, display stand, or decorative piece.',
        'description_cn': '简洁优雅的水晶台，多功能设计。可用作烛台、展示台或装饰品。',
        'material': 'K9 Crystal',
        'size': 'Various',
        'moq': '100 PCS',
        'lead_time': '10-15 days'
    },
    {
        'name': 'Premium Candle Holder',
        'name_cn': '高级烛台',
        'image': 'product-8.jpg',
        'category': 'Candle Holder',
        'description': 'Premium quality candle holder, exquisite craftsmanship. Made from high-grade K9 crystal with superior transparency and sparkle.',
        'description_cn': '高级品质烛台，工艺精湛。采用优质K9水晶，透明度和闪光度极佳。',
        'material': 'K9 Crystal',
        'size': 'Multiple sizes',
        'moq': '50 PCS',
        'lead_time': '15-20 days'
    }
]

# 添加产品
for i, product in enumerate(products):
    # 产品名称
    content.append(Paragraph(f"{product['name']} | {product['name_cn']}", product_title_style))
    content.append(Paragraph(product['category'], ParagraphStyle('Category', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#666666'), spaceAfter=5)))

    # 图片和描述并排布局
    image_path = f"/workspace/projects/cloudflare-deploy/images/{product['image']}"
    if os.path.exists(image_path):
        try:
            product_img = Image(image_path, width=6*cm, height=6*cm)
        except:
            product_img = None
    else:
        product_img = None

    # 产品信息表格
    info_data = [
        ['Description', product['description']],
        ['描述', product['description_cn']],
        ['材质 | Material', product['material']],
        ['尺寸 | Size', product['size']],
        ['起订量 | MOQ', product['moq']],
        ['交期 | Lead Time', product['lead_time']],
    ]

    info_table = Table(info_data, colWidths=[3*cm, 9*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))

    # 如果有图片，添加图片
    if product_img:
        content.append(product_img)
        content.append(Spacer(0, 0.3*cm))

    content.append(info_table)
    content.append(Spacer(0, 0.5*cm))

    # 分页（每2个产品一页）
    if (i + 1) % 2 == 0 and i < len(products) - 1:
        content.append(PageBreak())

content.append(PageBreak())

# === 联系我们 ===
content.append(Paragraph("联系我们 | Contact Us", title_style))

contact_section = """
<para spaceb=15>
<font size=12><b>We are ready to serve you!</b></font>
</para>
<para spaceb=10>
<font size=10>For inquiries, quotes, or custom orders, please contact us. Our professional team will respond within 24 hours.</font>
</para>
"""

content.append(Paragraph(contact_section, body_style))
content.append(Spacer(0, 1*cm))

# 联系信息表格
contact_full_data = [
    ['📧 Email', 'info@miga.cc'],
    ['📞 Phone', '+86-19879476613'],
    ['💬 WhatsApp', '+86-19879476613'],
    ['🌐 Website', 'www.miga.cc'],
    ['📍 Address', 'No.888 Shuijing Road, Pujiang County, Zhejiang Province, China'],
]

contact_full_table = Table(contact_full_data, colWidths=[3*cm, 9*cm])
contact_full_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
]))

content.append(contact_full_table)

content.append(Spacer(0, 1*cm))

# 结尾
footer_text = """
<para align=center spaceb=10>
<font size=9><i>Thank you for choosing MIGAC!</i></font><br/>
<font size=9><i>MIGAC - Professional Crystal Craft Manufacturer</i></font><br/>
<font size=9><i>&copy; 2024 MIGAC. All Rights Reserved.</i></font>
</para>
"""

content.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['BodyText'], fontSize=9, textColor=colors.HexColor('#666666'), alignment=TA_CENTER)))

# 生成PDF
print("正在生成PDF...")
doc.build(content)
print(f"PDF已生成: {output_file}")
print(f"文件大小: {os.path.getsize(output_file) / 1024:.2f} KB")
