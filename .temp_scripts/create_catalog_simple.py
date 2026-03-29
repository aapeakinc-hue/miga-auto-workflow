#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建MIGAC产品目录PDF - 简化版
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# 创建PDF
output_file = '/workspace/projects/cloudflare-deploy/MIGAC_Product_Catalog_2024.pdf'
doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)

# 样式
styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1a237e'), alignment=TA_CENTER, spaceAfter=15)
heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#0d47a1'), spaceAfter=10)
body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, leading=14)
product_title_style = ParagraphStyle('ProductTitle', parent=styles['Heading3'], fontSize=14, textColor=colors.HexColor('#1a237e'))

content = []

# 封面
content.append(Spacer(0, 2*cm))
content.append(Paragraph("MIGAC", title_style))
content.append(Paragraph("Professional Crystal Candle Holder Manufacturer", ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#666666'), alignment=TA_CENTER, spaceAfter=10)))
content.append(Paragraph("Product Catalog 2024", heading_style))
content.append(Spacer(0, 1*cm))

# Logo
if os.path.exists('/workspace/projects/cloudflare-deploy/images/logo.jpg'):
    try:
        logo = Image('/workspace/projects/cloudflare-deploy/images/logo.jpg', width=4*cm, height=2*cm)
        logo.hAlign = 'CENTER'
        content.append(logo)
    except:
        pass

content.append(Spacer(0, 1*cm))

# 联系信息
contact_data = [
    ['Email:', 'info@miga.cc'],
    ['Phone:', '+86-19879476613'],
    ['WhatsApp:', '+86-19879476613'],
    ['Website:', 'www.miga.cc'],
]
contact_table = Table(contact_data, colWidths=[3*cm, 8*cm])
contact_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, -1), 'RIGHT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'), ('FONTSIZE', (0, 0), (-1, -1), 10)]))
content.append(contact_table)

content.append(PageBreak())

# 关于我们
content.append(Paragraph("About Us", title_style))
about_text = """MIGAC is a professional crystal craft manufacturer based in Pujiang County, Zhejiang Province - the famous "Crystal Capital of the World". With 10+ years of industry experience, we specialize in manufacturing high-quality crystal candle holders, crystal chandeliers, and crystal decorations.

Our factory covers an area of 5,000 square meters, equipped with advanced production facilities and a skilled technical team. From design, development to production and quality inspection, every step is strictly controlled.

With premium products and professional services, our products are exported to 50+ countries including USA, Europe, Middle East, and Southeast Asia. We have served 182+ international clients."""

content.append(Paragraph(about_text, body_style))
content.append(Spacer(0, 1*cm))

# 优势
content.append(Paragraph("Core Advantages", heading_style))
advantages = [
    ['Factory Direct', 'Manufacturer direct sales, competitive pricing'],
    ['OEM/ODM', 'Professional design team, custom solutions'],
    ['Quality Assurance', 'ISO 9001 certified, strict quality control'],
    ['Low MOQ', 'Flexible MOQ, small trial orders welcome'],
    ['Fast Response', '24-hour response, on-time delivery'],
    ['Global Shipping', 'Worldwide delivery, customs clearance'],
]
adv_table = Table(advantages, colWidths=[4*cm, 8*cm])
adv_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('FONTSIZE', (0, 0), (-1, -1), 9)]))
content.append(adv_table)

content.append(PageBreak())

# 产品
content.append(Paragraph("Product Catalogue", title_style))

products = [
    ('5 Arms Candelabra', 'product-1.jpg', 'Elegant 5-arm design, made from premium K9 crystal. Perfect for weddings, hotels, and banquets.', 'K9 Crystal', '50 PCS', '15-20 days'),
    ('9 Arms Candelabra', 'product-2.jpg', 'Luxurious 9-arm candelabra, multi-layer crystal design. Ideal for hotel lobbies and banquet halls.', 'K9 Crystal', '10 PCS', '20-25 days'),
    ('Classic Candlestick', 'product-3.jpg', 'Classic single candlestick design, simple and elegant. Hand-polished K9 crystal.', 'K9 Crystal', '100 PCS', '10-15 days'),
    ('Crystal Candle Holders', 'product-4.jpg', 'Modern crystal candle holder set, premium quality. Perfect for weddings and parties.', 'K9 Crystal', '50 PCS', '15-20 days'),
    ('Crystal Bubble Stand', 'product-5.jpg', 'Unique crystal bubble stand design, artistic and elegant. Excellent light refraction.', 'K9 Crystal', '50 PCS', '15-20 days'),
    ('Color Candelabra', 'product-6.jpg', 'Colorful crystal candelabra, vibrant colors. Available in various colors.', 'K9 Crystal', '50 PCS', '15-20 days'),
    ('Crystal Stand', 'product-7.jpg', 'Simple yet elegant crystal stand, versatile design. Multi-purpose use.', 'K9 Crystal', '100 PCS', '10-15 days'),
    ('Premium Candle Holder', 'product-8.jpg', 'Premium quality candle holder, exquisite craftsmanship. High-grade K9 crystal.', 'K9 Crystal', '50 PCS', '15-20 days'),
]

for name, img_file, desc, material, moq, lead_time in products:
    content.append(Paragraph(name, product_title_style))
    
    img_path = f'/workspace/projects/cloudflare-deploy/images/{img_file}'
    if os.path.exists(img_path):
        try:
            product_img = Image(img_path, width=6*cm, height=6*cm)
            content.append(product_img)
        except:
            pass
    
    info_data = [
        ['Description:', desc],
        ['Material:', material],
        ['MOQ:', moq],
        ['Lead Time:', lead_time],
    ]
    info_table = Table(info_data, colWidths=[3*cm, 9*cm])
    info_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, -1), 'RIGHT'), ('ALIGN', (1, 0), (1, -1), 'LEFT'), ('FONTSIZE', (0, 0), (-1, -1), 9), ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])]))
    content.append(info_table)
    content.append(Spacer(0, 0.5*cm))

content.append(PageBreak())

# 联系我们
content.append(Paragraph("Contact Us", title_style))
content.append(Paragraph("For inquiries, quotes, or custom orders, please contact us. Our team will respond within 24 hours.", body_style))
content.append(Spacer(0, 1*cm))

contact_full = [
    ['Email', 'info@miga.cc'],
    ['Phone', '+86-19879476613'],
    ['WhatsApp', '+86-19879476613'],
    ['Website', 'www.miga.cc'],
    ['Address', 'No.888 Shuijing Road, Pujiang County, Zhejiang Province, China'],
]
contact_full_table = Table(contact_full, colWidths=[3*cm, 9*cm])
contact_full_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')), ('FONTSIZE', (0, 0), (-1, -1), 10)]))
content.append(contact_full_table)

content.append(Spacer(0, 1*cm))
content.append(Paragraph("Thank you for choosing MIGAC!", ParagraphStyle('ThankYou', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER)))

# 生成PDF
print("Creating PDF catalog...")
doc.build(content)
print(f"PDF created: {output_file}")
print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")
