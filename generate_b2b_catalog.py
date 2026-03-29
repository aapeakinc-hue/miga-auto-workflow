#!/usr/bin/env python3
"""
生成MIGAC专业B2B产品目录PDF
符合国际catalog标准，对标阿里巴巴和主流水晶工艺品网站
"""

import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

# 颜色定义 - B2B专业风格
COLORS = {
    'primary': colors.HexColor('#1e3c72'),
    'accent': colors.HexColor('#d4af37'),
    'text_light': colors.HexColor('#ffffff'),
    'text_dark': colors.HexColor('#333333'),
    'text_gray': colors.HexColor('#666666'),
}


def create_styles():
    """创建PDF样式"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CatalogTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=COLORS['accent'],
        alignment=1,
        spaceAfter=12
    ))
    
    styles.add(ParagraphStyle(
        name='SeriesTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=COLORS['text_dark'],
        alignment=0,
        spaceAfter=10,
        leading=26
    ))
    
    styles.add(ParagraphStyle(
        name='ProductTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=COLORS['text_dark'],
        alignment=0,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='CatalogBodyText',
        fontName='Helvetica',
        fontSize=10,
        textColor=COLORS['text_gray'],
        alignment=0,
        leading=14,
        spaceAfter=8
    ))
    
    return styles


def create_cover_page(canvas, doc, catalog_data):
    """创建封面页"""
    canvas.saveState()
    
    # 背景
    canvas.setFillColor(COLORS['primary'])
    canvas.rect(0, 0, A4[0], A4[1], fill=True)
    
    # 金色边框
    canvas.setStrokeColor(COLORS['accent'])
    canvas.setLineWidth(4)
    canvas.rect(cm, cm, A4[0] - 2*cm, A4[1] - 2*cm, fill=False)
    
    # 标题
    canvas.setFillColor(COLORS['accent'])
    canvas.setFont('Helvetica-Bold', 48)
    canvas.drawCentredString(A4[0]/2, A4[1] - 7*cm, "MIGAC")
    
    canvas.setFont('Helvetica-Bold', 24)
    canvas.drawCentredString(A4[0]/2, A4[1] - 8.5*cm, "PREMIUM CRYSTAL CRAFTS")
    
    canvas.setFont('Helvetica', 14)
    canvas.setFillColor(colors.HexColor('#ffffff'))
    canvas.drawCentredString(A4[0]/2, A4[1] - 10*cm, "Excellence in Every Crystal")
    
    # 公司信息
    company = catalog_data['catalog']['company']
    canvas.setFont('Helvetica', 12)
    canvas.drawCentredString(A4[0]/2, A4[1] - 15*cm, company['name'])
    canvas.setFont('Helvetica', 10)
    canvas.drawCentredString(A4[0]/2, A4[1] - 16*cm, company['email'])
    
    # 页脚
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(A4[0]/2, 3*cm, f"B2B Catalog 2026 | {datetime.now().strftime('%B %Y')}")
    
    canvas.restoreState()


def create_header_footer(canvas, doc):
    """创建页眉和页脚"""
    canvas.saveState()
    
    # 页眉
    canvas.setFillColor(COLORS['primary'])
    canvas.rect(0, A4[1] - 1.5*cm, A4[0], 1.5*cm, fill=True)
    
    canvas.setStrokeColor(COLORS['accent'])
    canvas.setLineWidth(2)
    canvas.line(0, A4[1] - 1.5*cm, A4[0], A4[1] - 1.5*cm)
    
    canvas.setFillColor(COLORS['accent'])
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(1*cm, A4[1] - 1.2*cm, "MIGAC")
    
    canvas.setFillColor(colors.HexColor('#ffffff'))
    canvas.setFont('Helvetica', 9)
    canvas.drawString(2.5*cm, A4[1] - 1.2*cm, "Premium Crystal Crafts B2B Catalog")
    
    # 页脚
    canvas.setFillColor(COLORS['primary'])
    canvas.rect(0, 0, A4[0], 1.2*cm, fill=True)
    
    canvas.setStrokeColor(COLORS['accent'])
    canvas.setLineWidth(2)
    canvas.line(0, 1.2*cm, A4[0], 1.2*cm)
    
    # 页码
    canvas.setFillColor(colors.HexColor('#ffffff'))
    canvas.setFont('Helvetica', 9)
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(A4[0]/2, 0.5*cm, f"Page {page_num}")
    
    canvas.setFont('Helvetica', 8)
    canvas.drawString(1*cm, 0.5*cm, "info@miga.cc | +86-19879476613 | www.miga.cc")
    
    canvas.restoreState()


def generate_catalog_pdf(input_json, output_pdf):
    """生成产品目录PDF"""
    print("=" * 70)
    print("生成MIGAC专业B2B产品目录PDF")
    print("=" * 70)
    print()
    
    # 读取JSON数据
    with open(input_json, 'r', encoding='utf-8') as f:
        catalog_data = json.load(f)
    
    catalog = catalog_data['catalog']
    
    print(f"📄 公司名称: {catalog['company']['name']}")
    print(f"📊 产品系列: {len(catalog['product_series'])}")
    print(f"📦 产品总数: {catalog['statistics']['total_products']}")
    print()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = create_styles()
    elements = []
    
    # 创建自定义封面内容
    elements.append(Paragraph(" ", ParagraphStyle(
        'CoverSpacer',
        fontName='Helvetica',
        fontSize=1,
        leading=1
    )))
    elements.append(PageBreak())
    
    # 生成每个系列
    for series in catalog['product_series']:
        # 系列标题
        elements.append(Paragraph(f"{series['series_name']}", styles['SeriesTitle']))
        elements.append(Paragraph(f"{series['series_subtitle']}", ParagraphStyle(
            'SubtitleStyle',
            fontName='Helvetica',
            fontSize=12,
            textColor=COLORS['accent'],
            alignment=0,
            leading=16,
            spaceAfter=0.5*cm
        )))
        
        # 系列描述
        elements.append(Paragraph(series['description'], styles['CatalogBodyText']))
        elements.append(Spacer(0, 0.5*cm))
        
        # 特性
        features = " | ".join(series['features'])
        elements.append(Paragraph(f"<b>Features:</b> {features}", ParagraphStyle(
            'FeaturesStyle',
            fontName='Helvetica',
            fontSize=9,
            textColor=COLORS['accent'],
            leading=12,
            spaceAfter=1*cm
        )))
        
        # 产品列表
        for product in series['products']:
            # 产品标题
            elements.append(Paragraph(f"<b>{product['model']}</b> - {product['name']}", styles['ProductTitle']))
            
            # 宣传语
            if 'tagline' in product:
                elements.append(Paragraph(f"<i>{product['tagline']}</i>", ParagraphStyle(
                    'TaglineStyle',
                    fontName='Helvetica-Oblique',
                    fontSize=9,
                    textColor=COLORS['accent'],
                    leading=12,
                    spaceAfter=6
                )))
            
            # 描述
            elements.append(Paragraph(product.get('description', ''), styles['CatalogBodyText']))
            
            # 规格表格
            spec_data = [
                ['Dimensions', product.get('dimensions', '-')],
                ['Material', product.get('material', '-')],
                ['Finish', product.get('finish', '-')],
                ['MOQ', str(product.get('moq', '-'))],
                ['Lead Time', product.get('lead_time', '-')],
                ['Price Range', f"<b>{product.get('price_range', '-')}</b>"]
            ]
            
            spec_table = Table(spec_data, colWidths=[4*cm, 10*cm])
            spec_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TEXTCOLOR', (0, 5), (0, 5), COLORS['accent']),
                ('FONTNAME', (0, 5), (0, 5), 'Helvetica-Bold'),
                ('FONTNAME', (1, 5), (1, 5), 'Helvetica-Bold'),
                ('TEXTCOLOR', (1, 5), (1, 5), COLORS['accent']),
            ]))
            elements.append(spec_table)
            
            # 标签
            badges = []
            if product.get('best_seller'):
                badges.append('<font color="#d4af37" size="8"><b>[BEST SELLER]</b></font>')
            if product.get('featured'):
                badges.append('<font color="#00bfff" size="8"><b>[FEATURED]</b></font>')
            if product.get('new_arrival'):
                badges.append('<font color="#ff6600" size="8"><b>[NEW ARRIVAL]</b></font>')
            
            if badges:
                elements.append(Paragraph(' '.join(badges), styles['CatalogBodyText']))
            
            elements.append(Spacer(0, 0.8*cm))
        
        # 分页
        elements.append(PageBreak())
    
    # 联系页
    elements.append(Paragraph("CONTACT US", styles['SeriesTitle']))
    elements.append(Spacer(0, 0.5*cm))
    
    company = catalog['company']
    contact_data = [
        ['Company', company['name']],
        ['Email', company['email']],
        ['Phone', company['phone']],
        ['WhatsApp', company['whatsapp']],
        ['Website', company['website']],
        ['Address', company['address']]
    ]
    
    contact_table = Table(contact_data, colWidths=[5*cm, 12*cm])
    contact_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TEXTCOLOR', (0, 0), (0, -1), COLORS['accent']),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(contact_table)
    
    # 构建PDF
    print("🚀 正在生成PDF...")
    doc.build(elements, 
              onFirstPage=lambda c, d: create_cover_page(c, d, catalog_data),
              onLaterPages=lambda c, d: create_header_footer(c, d))
    
    print("✅ PDF生成成功!")
    print(f"📄 输出文件: {output_pdf}")
    print()


if __name__ == "__main__":
    input_json = "assets/MIGAC_B2B_CATALOG_DATA.json"
    output_pdf = "assets/MIGAC_B2B_CATALOG_2026.pdf"
    
    generate_catalog_pdf(input_json, output_pdf)
    
    print("=" * 70)
    print("PDF生成完成!")
    print("=" * 70)
