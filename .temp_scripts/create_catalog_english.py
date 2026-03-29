#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成英文版产品目录
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册字体
try:
    pdfmetrics.registerFont(TTFont('Arial', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    font_name = 'Arial'
except:
    font_name = 'Helvetica'

# 创建PDF
pdf_path = 'cloudflare-deploy/MIGAC_Product_Catalog_EN_2024.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=2*cm, bottomMargin=2*cm)

# 创建样式
styles = getSampleStyleSheet()

# 自定义样式
styles.add(ParagraphStyle(
    name='TitleStyle',
    parent=styles['Title'],
    fontName=font_name,
    fontSize=28,
    textColor=colors.HexColor('#0d47a1'),
    spaceAfter=12,
    alignment=TA_CENTER,
))

styles['Heading1'].fontName = font_name
styles['Heading1'].fontSize = 18
styles['Heading1'].textColor = colors.HexColor('#1a237e')
styles['Heading1'].spaceAfter = 12

styles['Heading2'].fontName = font_name
styles['Heading2'].fontSize = 14
styles['Heading2'].textColor = colors.HexColor('#0d47a1')
styles['Heading2'].spaceAfter = 10

styles['Normal'].fontName = font_name
styles['Normal'].fontSize = 10
styles['Normal'].spaceAfter = 6

styles.add(ParagraphStyle(
    name='Highlight',
    parent=styles['Normal'],
    fontName=font_name,
    fontSize=10,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=6,
))

# 构建文档内容
story = []

# 封面
story.append(Spacer(1, 2*cm))
story.append(Paragraph("MIGAC Crystal Crafts", styles['TitleStyle']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Product Catalog 2024", styles['Heading1']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Crystal Candle Holders & Crafts", styles['Normal']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Professional Crystal Craft Manufacturer Since 2013", styles['Highlight']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Factory Direct | OEM/ODM Supported", styles['Normal']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Contact Us:", styles['Heading2']))
story.append(Paragraph("Email: info@miga.cc", styles['Normal']))
story.append(Paragraph("WhatsApp: +86 138 8888 8888", styles['Normal']))
story.append(Paragraph("Website: https://miga.cc", styles['Normal']))

story.append(PageBreak())

# 第2页：公司简介
story.append(Paragraph("About MIGAC", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("MIGAC is a professional crystal craft manufacturer specializing in crystal candle holders and decorative crafts. With over 10 years of experience, we serve 182+ international clients worldwide.", styles['Normal']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Our Advantages:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))

advantages = [
    ["✓", "Factory Direct - Competitive Pricing"],
    ["✓", "10+ Years Manufacturing Experience"],
    ["✓", "OEM/ODM Customization Service"],
    ["✓", "ISO Quality Management System"],
    ["✓", "Low MOQ - Flexible Cooperation"],
    ["✓", "Fast Response & On-Time Delivery"],
]

data = [["", ""]]
for advantage in advantages:
    data.append(advantage)

table = Table(data, colWidths=[0.8*cm, 12*cm])
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
]))
story.append(table)

story.append(PageBreak())

# 第3-4页：产品列表
story.append(Paragraph("Product Categories", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))

categories = [
    "Crystal Candle Holders",
    "Crystal Candelabras",
    "Crystal Candlesticks",
    "Crystal Tea Light Holders",
    "Crystal Votive Holders",
    "Crystal Pillar Holders",
    "Crystal Decorative Crafts",
    "Custom Crystal Products",
]

for category in categories:
    story.append(Paragraph(f"• {category}", styles['Normal']))
    story.append(Spacer(1, 0.1*cm))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Product Features:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))
story.append(Paragraph("• High quality K9 crystal material", styles['Normal']))
story.append(Paragraph("• Various sizes and designs available", styles['Normal']))
story.append(Paragraph("• OEM/ODM customization supported", styles['Normal']))
story.append(Paragraph("• Suitable for home decoration, hotels, events", styles['Normal']))
story.append(Paragraph("• Lead-free and environmentally friendly", styles['Normal']))

story.append(PageBreak())

# 第5页：定制服务
story.append(Paragraph("Custom Services", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("We offer comprehensive OEM/ODM customization services to meet your specific requirements.", styles['Normal']))
story.append(Spacer(1, 0.3*cm))

services = [
    ["Custom Design", "Provide your design, we create the mold and produce"],
    ["Logo Engraving", "Laser engraving or sandblasting your logo on crystal"],
    ["Custom Size", "Adjust dimensions according to your specifications"],
    ["Custom Packaging", "Design custom packaging to match your brand"],
    ["Color Options", "Clear crystal, colored crystal, or mixed colors"],
]

data = [[b[0] for b in services], [b[1] for b in services]]
table = Table(data, colWidths=[5*cm, 8*cm])
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#0d47a1')),
    ('BACKGROUND', (0, 1), (0, 5), colors.HexColor('#1976d2')),
    ('TEXTCOLOR', (0, 0), (0, 5), colors.white),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(table)

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Order Process:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))
story.append(Paragraph("1. Send inquiry with requirements", styles['Normal']))
story.append(Paragraph("2. We provide quotation and samples", styles['Normal']))
story.append(Paragraph("3. Confirm design and specifications", styles['Normal']))
story.append(Paragraph("4. Production and quality inspection", styles['Normal']))
story.append(Paragraph("5. Packaging and shipping", styles['Normal']))
story.append(Paragraph("6. After-sales support", styles['Normal']))

story.append(PageBreak())

# 第6页：联系我们
story.append(Paragraph("Contact Us", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))

contact_info = [
    ["Company Name", "MIGAC Crystal Crafts Co., Ltd."],
    ["Business Type", "Manufacturer & Exporter"],
    ["Established", "2013"],
    ["Products", "Crystal Candle Holders, Crystal Crafts"],
    ["Export Markets", "182+ Countries Worldwide"],
]

table = Table(contact_info, colWidths=[5*cm, 8*cm])
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ('BACKGROUND', (0, 0), (0, 4), colors.HexColor('#0d47a1')),
    ('TEXTCOLOR', (0, 0), (0, 4), colors.white),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(table)

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("How to Contact Us:", styles['Heading2']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("📧 Email: info@miga.cc", styles['Normal']))
story.append(Paragraph("📱 WhatsApp: +86 138 8888 8888", styles['Normal']))
story.append(Paragraph("🌐 Website: https://miga.cc", styles['Normal']))
story.append(Paragraph("📍 Address: Yiwu City, Zhejiang Province, China", styles['Normal']))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Business Hours:", styles['Heading2']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Monday - Friday: 9:00 AM - 6:00 PM (GMT+8)", styles['Normal']))
story.append(Paragraph("Saturday - Sunday: Closed", styles['Normal']))

story.append(Spacer(1, 1*cm))
story.append(Paragraph("Thank you for choosing MIGAC Crystal Crafts!", styles['Highlight']))
story.append(Paragraph("We look forward to working with you.", styles['Normal']))

# 生成PDF
doc.build(story)
print(f"✅ English product catalog created: {pdf_path}")
print(f"   File size: {os.path.getsize(pdf_path)/1024:.1f} KB")
