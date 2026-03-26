#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新PDF目录 - 真实公司历史和定制能力
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
story.append(Paragraph("Exquisite Craftsmanship Since 2009", styles['Highlight']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Expert Customization & Production", styles['Normal']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Contact Us:", styles['Heading2']))
story.append(Paragraph("Email: info@miga.cc", styles['Normal']))
story.append(Paragraph("WhatsApp: +86 19879476613", styles['Normal']))
story.append(Paragraph("Website: https://miga.cc", styles['Normal']))

story.append(PageBreak())

# 第2页：公司简介 - 真实历史
story.append(Paragraph("Our Legacy", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("<b>Founded in 2009 as Kamong Crystal Arts and Crafts Co., Ltd. in Hong Kong</b>", styles['Normal']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("With 15+ years of crystal craftsmanship heritage, MIGAC has evolved into a leading crystal manufacturer. Since 2015, our operations are managed by Yiwu Bangye Handicraft Factory, ensuring compliant and efficient production.", styles['Normal']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Our Core Strengths:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))

strengths = [
    ["Production Excellence", "Factories across Pujiang Crystal Industrial Parks"],
    ["Detail-Oriented", "Uncompromising attention to product details"],
    ["Customization Expert", "Specialized in bespoke crystal products"],
    ["Legacy & Compliance", "15+ years heritage, modern operations since 2015"],
    ["Scalability", "Mass production with precision craftsmanship"],
    ["Quality Control", "Strict QC at every production stage"],
]

data = [[b[0] for b in strengths], [b[1] for b in strengths]]
table = Table(data, colWidths=[5*cm, 10*cm])
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
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

story.append(PageBreak())

# 第3页：产品列表
story.append(Paragraph("Product Portfolio", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))

categories = [
    "Crystal Candle Holders",
    "Crystal Candelabras (5-arm, 7-arm, 9-arm, 12-arm)",
    "Crystal Candlesticks & Pillar Holders",
    "Crystal Tea Light & Votive Holders",
    "Crystal Chandeliers & Ceiling Lights",
    "Crystal Decorative Arts & Sculptures",
    "Custom Crystal Products",
    "Hotel & Wedding Collection",
]

for category in categories:
    story.append(Paragraph(f"• {category}", styles['Normal']))
    story.append(Spacer(1, 0.1*cm))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Production Capabilities:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))
story.append(Paragraph("• K9 Crystal & Premium Materials", styles['Normal']))
story.append(Paragraph("• Custom Designs & Branding", styles['Normal']))
story.append(Paragraph("• Mass Production (50,000+ pieces/month)", styles['Normal']))
story.append(Paragraph("• Precision Cutting & Polishing", styles['Normal']))
story.append(Paragraph("• OEM/ODM Services Available", styles['Normal']))

story.append(PageBreak())

# 第4页：定制服务 - 突出定制能力
story.append(Paragraph("Customization Excellence", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("We specialize in creating bespoke crystal products that match your exact specifications. Our 15+ years of expertise ensures exceptional results.", styles['Normal']))
story.append(Spacer(1, 0.3*cm))

services = [
    ["Custom Design", "Your vision, our expertise. From concept to production"],
    ["Logo & Branding", "Laser engraving, sandblasting, or etching your brand"],
    ["Custom Dimensions", "Any size, any shape, crystal expertise applied"],
    ["Material Selection", "K9, K5, or premium crystal options"],
    ["Color & Finish", "Clear, colored, or specialized crystal finishes"],
    ["Packaging Design", "Custom packaging to elevate your brand"],
]

data = [[b[0] for b in services], [b[1] for b in services]]
table = Table(data, colWidths=[5*cm, 10*cm])
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), font_name),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
    ('BACKGROUND', (0, 0), (0, 5), colors.HexColor('#0d47a1')),
    ('TEXTCOLOR', (0, 0), (0, 5), colors.white),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(table)

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Our Process:", styles['Heading2']))
story.append(Spacer(1, 0.1*cm))
story.append(Paragraph("1. Consultation - Understand your requirements", styles['Normal']))
story.append(Paragraph("2. Design - Create detailed drawings and specifications", styles['Normal']))
story.append(Paragraph("3. Sampling - Produce samples for your approval", styles['Normal']))
story.append(Paragraph("4. Production - Mass production with strict QC", styles['Normal']))
story.append(Paragraph("5. Delivery - Packaging and global shipping", styles['Normal']))
story.append(Paragraph("6. Support - Ongoing after-sales service", styles['Normal']))

story.append(PageBreak())

# 第5页：联系我们
story.append(Paragraph("Contact Us", styles['Heading1']))
story.append(Spacer(1, 0.3*cm))

contact_info = [
    ["Brand Name", "MIGAC Crystal Crafts"],
    ["Operating Company", "Yiwu Bangye Handicraft Factory (since 2015)"],
    ["Heritage", "Kamong Crystal Arts and Crafts Co., Ltd. (since 2009)"],
    ["Production Base", "Pujiang Crystal Industrial Parks, Zhejiang"],
    ["Export Markets", "50+ Countries Worldwide"],
]

table = Table(contact_info, colWidths=[5*cm, 10*cm])
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
story.append(Paragraph("Get in Touch:", styles['Heading2']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Email: info@miga.cc", styles['Normal']))
story.append(Paragraph("WhatsApp: +86 19879476613", styles['Normal']))
story.append(Paragraph("Website: https://miga.cc", styles['Normal']))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Business Hours:", styles['Heading2']))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Monday - Friday: 9:00 AM - 6:00 PM (GMT+8)", styles['Normal']))
story.append(Paragraph("Saturday - Sunday: Available by appointment", styles['Normal']))

story.append(Spacer(1, 1*cm))
story.append(Paragraph("Trusted by 182+ international clients since 2009", styles['Highlight']))
story.append(Paragraph("Let's create something beautiful together.", styles['Normal']))

# 生成PDF
doc.build(story)
print(f"Updated PDF catalog with true company history: {pdf_path}")
print(f"   File size: {os.path.getsize(pdf_path)/1024:.1f} KB")
print(f"   Heritage: Kamong Crystal Arts and Crafts Co., Ltd. (2009)")
print(f"   Operating: Yiwu Bangye Handicraft Factory (2015)")
print(f"   Production: Pujiang Crystal Industrial Parks")
