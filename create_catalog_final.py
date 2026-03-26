#!/usr/bin/env python3
"""
Generate MIGAC Crystal Candelabra Catalog
- Remove prices
- Reorganize product codes
- Use real product images
- Clean and professional international format
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Flowable, PageBreak
from reportlab.lib.colors import HexColor, white, black
from PIL import Image as PILImage

# Company Information
COMPANY_NAME = "Yiwu Bangye Crystal Crafts Factory"
COMPANY_ADDRESS = "Chengbei Road L38, Houzhai Street, Yiwu City, Zhejiang Province, China"
COMPANY_EMAIL = "sales@migac.com"
COMPANY_WEBSITE = "www.migac.com"

# Product Catalog Data - Reorganized with prices removed
PRODUCTS = [
    # 5 Arms Candelabras
    {
        "category": "5 Arms Candelabras",
        "code": "MG-5A-001",
        "name": "5 Arms Crystal Candelabra - Classic Design",
        "description": "Elegant 5-arm crystal candelabra with traditional design",
        "height": "45cm",
        "image": "微信圖片_20260321164310_212_2.jpg"
    },
    {
        "category": "5 Arms Candelabras",
        "code": "MG-5A-002",
        "name": "5 Arms Crystal Candelabra - Modern Style",
        "description": "Contemporary 5-arm crystal candelabra with sleek lines",
        "height": "50cm",
        "image": "微信圖片_20260321164442_216_2.jpg"
    },
    {
        "category": "5 Arms Candelabras",
        "code": "MG-5A-003",
        "name": "5 Arms Crystal Candelabra - Gold Finish",
        "description": "Luxurious gold-finished 5-arm crystal candelabra",
        "height": "48cm",
        "image": "微信圖片_20260321164444_218_2.jpg"
    },
    {
        "category": "5 Arms Candelabras",
        "code": "MG-5A-004",
        "name": "5 Arms Crystal Candelabra - Silver Plated",
        "description": "Beautiful silver-plated 5-arm crystal candelabra",
        "height": "45cm",
        "image": "微信圖片_20260321164445_219_2.jpg"
    },
    {
        "category": "5 Arms Candelabras",
        "code": "MG-5A-005",
        "name": "5 Arms Crystal Candelabra - Crystal Clear",
        "description": "Pure crystal 5-arm candelabra with prismatic effect",
        "height": "42cm",
        "image": "微信圖片_20260321164447_222_2.jpg"
    },
    
    # 9 Arms Candelabras
    {
        "category": "9 Arms Candelabras",
        "code": "MG-9A-001",
        "name": "9 Arms Crystal Candelabra - Grand Design",
        "description": "Magnificent 9-arm crystal candelabra for grand spaces",
        "height": "65cm",
        "image": "微信圖片_20260321164448_223_2.jpg"
    },
    {
        "category": "9 Arms Candelabras",
        "code": "MG-9A-002",
        "name": "9 Arms Crystal Candelabra - Royal Collection",
        "description": "Royal-style 9-arm crystal candelabra with ornate details",
        "height": "70cm",
        "image": "微信圖片_20260321164449_224_2.jpg"
    },
    {
        "category": "9 Arms Candelabras",
        "code": "MG-9A-003",
        "name": "9 Arms Crystal Candelabra - Estate Edition",
        "description": "Elegant estate-style 9-arm crystal candelabra",
        "height": "68cm",
        "image": "微信圖片_20260321164450_225_2.jpg"
    },
    {
        "category": "9 Arms Candelabras",
        "code": "MG-9A-004",
        "name": "9 Arms Crystal Candelabra - Palace Series",
        "description": "Palace-inspired 9-arm crystal candelabra masterpiece",
        "height": "72cm",
        "image": "微信圖片_20260321164515_251_2.jpg"
    },
    {
        "category": "9 Arms Candelabras",
        "code": "MG-9A-005",
        "name": "9 Arms Crystal Candelabra - Luxe Edition",
        "description": "Ultra-luxurious 9-arm crystal candelabra",
        "height": "75cm",
        "image": "微信圖片_20260321164517_253_2.jpg"
    },
    
    # Multi-Arms Candelabras
    {
        "category": "Multi-Arms Candelabras",
        "code": "MG-MA-001",
        "name": "10 Arms Crystal Candelabra - Statement Piece",
        "description": "Dramatic 10-arm crystal candelabra as centerpiece",
        "height": "80cm",
        "image": "微信圖片_20260321164606_290_2.jpg"
    },
    {
        "category": "Multi-Arms Candelabras",
        "code": "MG-MA-002",
        "name": "12 Arms Crystal Candelabra - Grand Chandelier Style",
        "description": "Chandelier-style 12-arm crystal candelabra",
        "height": "90cm",
        "image": "微信圖片_20260321164607_291_2.jpg"
    },
    
    # Special Collections
    {
        "category": "Special Collections",
        "code": "MG-SC-001",
        "name": "Crystal Candelabra with Base Plate",
        "description": "Elegant candelabra with decorative base plate",
        "height": "55cm",
        "image": "微信圖片_20260321164716_351_2.jpg"
    },
    {
        "category": "Special Collections",
        "code": "MG-SC-002",
        "name": "Crystal Candelabra with Glass Shades",
        "description": "Candelabra featuring crystal arms and glass shades",
        "height": "60cm",
        "image": "微信圖片_20260321164721_355_2.jpg"
    },
    {
        "category": "Special Collections",
        "code": "MG-SC-003",
        "name": "Tall Crystal Candelabra - Column Style",
        "description": "Column-style tall crystal candelabra design",
        "height": "85cm",
        "image": "微信圖片_20260321164723_356_2.jpg"
    },
    {
        "category": "Special Collections",
        "code": "MG-SC-004",
        "name": "Crystal Candelabra - Pedestal Base",
        "description": "Elegant candelabra with crystal pedestal base",
        "height": "75cm",
        "image": "微信圖片_20260321164726_357_2.jpg"
    },
    
    # Classic Designs
    {
        "category": "Classic Designs",
        "code": "MG-CD-001",
        "name": "Vintage Crystal Candelabra",
        "description": "Vintage-inspired crystal candelabra with ornate details",
        "height": "52cm",
        "image": "微信圖片_20260321164735_359_2.jpg"
    },
    {
        "category": "Classic Designs",
        "code": "MG-CD-002",
        "name": "Traditional Crystal Candelabra",
        "description": "Traditional design with premium crystal quality",
        "height": "58cm",
        "image": "微信圖片_20260321164739_360_2.jpg"
    },
    {
        "category": "Classic Designs",
        "code": "MG-CD-003",
        "name": "Baroque Crystal Candelabra",
        "description": "Baroque-style crystal candelabra with intricate details",
        "height": "62cm",
        "image": "微信圖片_20260321164914_365_2.jpg"
    },
    {
        "category": "Classic Designs",
        "code": "MG-CD-004",
        "name": "Rococo Crystal Candelabra",
        "description": "Rococo-inspired elegant crystal candelabra",
        "height": "65cm",
        "image": "微信圖片_20260321164916_366_2.jpg"
    },
    
    # Modern Collection
    {
        "category": "Modern Collection",
        "code": "MG-MC-001",
        "name": "Minimalist Crystal Candelabra",
        "description": "Clean, minimalist design with premium crystals",
        "height": "48cm",
        "image": "微信圖片_20260321164919_369_2.jpg"
    },
    {
        "category": "Modern Collection",
        "code": "MG-MC-002",
        "name": "Geometric Crystal Candelabra",
        "description": "Modern geometric design crystal candelabra",
        "height": "55cm",
        "image": "微信圖片_20260321164927_376_2.jpg"
    },
    {
        "category": "Modern Collection",
        "code": "MG-MC-003",
        "name": "Contemporary Crystal Candelabra",
        "description": "Contemporary design with sleek crystal arms",
        "height": "60cm",
        "image": "微信圖片_20260321164932_381_2.jpg"
    },
    {
        "category": "Modern Collection",
        "code": "MG-MC-004",
        "name": "Crystal Candelabra - LED Compatible",
        "description": "Modern candelabra compatible with LED candles",
        "height": "58cm",
        "image": "微信圖片_20260321164933_382_2.jpg"
    },
    
    # Premium Collection
    {
        "category": "Premium Collection",
        "code": "MG-PC-001",
        "name": "Premium Crystal Candelabra - Full Crystal",
        "description": "Full crystal construction with premium quality",
        "height": "78cm",
        "image": "微信圖片_20260321165015_422_2.jpg"
    },
    {
        "category": "Premium Collection",
        "code": "MG-PC-002",
        "name": "Premium Crystal Candelabra - Gold Trim",
        "description": "Premium crystal with gold trim accents",
        "height": "82cm",
        "image": "微信圖片_20260321165016_423_2.jpg"
    },
    
    # Heritage Series
    {
        "category": "Heritage Series",
        "code": "MG-HS-001",
        "name": "Heritage Crystal Candelabra",
        "description": "Heritage collection with timeless design",
        "height": "68cm",
        "image": "微信圖片_20260321165323_609_2.jpg"
    },
    {
        "category": "Heritage Series",
        "code": "MG-HS-002",
        "name": "Antique Style Crystal Candelabra",
        "description": "Antique-style crystal candelabra masterpiece",
        "height": "72cm",
        "image": "微信圖片_20260321165331_616_2.jpg"
    },
    {
        "category": "Heritage Series",
        "code": "MG-HS-003",
        "name": "Crystal Candelabra with Scroll Details",
        "description": "Elegant scroll details on crystal arms",
        "height": "75cm",
        "image": "微信圖片_20260321165332_617_2.jpg"
    },
    {
        "category": "Heritage Series",
        "code": "MG-HS-004",
        "name": "Crystal Candelabra - Floral Motif",
        "description": "Floral motif crystal candelabra design",
        "height": "70cm",
        "image": "微信圖片_20260321165333_618_2.jpg"
    },
    
    # Luxury Series
    {
        "category": "Luxury Series",
        "code": "MG-LX-001",
        "name": "Luxury Crystal Candelabra - Crown Design",
        "description": "Crown-inspired luxury crystal candelabra",
        "height": "85cm",
        "image": "微信圖片_20260321165402_647_2.jpg"
    },
    {
        "category": "Luxury Series",
        "code": "MG-LX-002",
        "name": "Luxury Crystal Candelabra - Diamond Cut",
        "description": "Diamond-cut crystal with exceptional brilliance",
        "height": "88cm",
        "image": "微信圖片_20260321165403_648_2.jpg"
    },
    
    # Grand Collection
    {
        "category": "Grand Collection",
        "code": "MG-GC-001",
        "name": "Grand Crystal Candelabra - Tiered Design",
        "description": "Multi-tiered grand crystal candelabra",
        "height": "95cm",
        "image": "微信圖片_20260321165445_662_2.jpg"
    },
    {
        "category": "Grand Collection",
        "code": "MG-GC-002",
        "name": "Grand Crystal Candelabra - Cascade Style",
        "description": "Cascade-style grand crystal candelabra",
        "height": "98cm",
        "image": "微信圖片_20260321165446_663_2.jpg"
    },
    {
        "category": "Grand Collection",
        "code": "MG-GC-003",
        "name": "Grand Crystal Candelabra - Full Spectrum",
        "description": "Full spectrum crystal prisms",
        "height": "100cm",
        "image": "微信圖片_20260321165454_671_2.jpg"
    },
    {
        "category": "Grand Collection",
        "code": "MG-GC-004",
        "name": "Grand Crystal Candelabra - Crystal Tower",
        "description": "Tower-style grand crystal candelabra",
        "height": "105cm",
        "image": "微信圖片_20260321165455_672_2.jpg"
    },
    
    # Masterpiece Collection
    {
        "category": "Masterpiece Collection",
        "code": "MG-MP-001",
        "name": "Masterpiece Crystal Candelabra",
        "description": "One-of-a-kind masterpiece crystal candelabra",
        "height": "110cm",
        "image": "微信圖片_20260321165456_673_2.jpg"
    },
    {
        "category": "Masterpiece Collection",
        "code": "MG-MP-002",
        "name": "Crystal Candelabra - Imperial Design",
        "description": "Imperial-inspired crystal candelabra",
        "height": "115cm",
        "image": "微信圖片_20260321165505_681_2.jpg"
    },
    {
        "category": "Masterpiece Collection",
        "code": "MG-MP-003",
        "name": "Crystal Candelabra - Crystal Crown",
        "description": "Crown-topped crystal candelabra",
        "height": "108cm",
        "image": "微信圖片_20260321165509_685_2.jpg"
    },
    {
        "category": "Masterpiece Collection",
        "code": "MG-MP-004",
        "name": "Crystal Candelabra - Royal Heights",
        "description": "Royal heights crystal candelabra collection",
        "height": "120cm",
        "image": "微信圖片_20260321165510_686_2.jpg"
    },
    
    # Elite Collection
    {
        "category": "Elite Collection",
        "code": "MG-EC-001",
        "name": "Elite Crystal Candelabra",
        "description": "Elite collection crystal candelabra",
        "height": "92cm",
        "image": "微信圖片_20260321165514_690_2.jpg"
    },
    {
        "category": "Elite Collection",
        "code": "MG-EC-002",
        "name": "Crystal Candelabra - Supreme Quality",
        "description": "Supreme quality crystal candelabra",
        "height": "96cm",
        "image": "微信圖片_20260321165524_698_2.jpg"
    },
    {
        "category": "Elite Collection",
        "code": "MG-EC-003",
        "name": "Crystal Candelabra - Exquisite Details",
        "description": "Exquisite details throughout",
        "height": "94cm",
        "image": "微信圖片_20260321165534_706_2.jpg"
    },
    {
        "category": "Elite Collection",
        "code": "MG-EC-004",
        "name": "Crystal Candelabra - Ultimate Edition",
        "description": "Ultimate edition crystal candelabra",
        "height": "102cm",
        "image": "微信圖片_20260321165541_711_2.jpg"
    },
    
    # Signature Collection
    {
        "category": "Signature Collection",
        "code": "MG-SG-001",
        "name": "Signature Crystal Candelabra - Artist's Choice",
        "description": "Artist-designed signature collection",
        "height": "88cm",
        "image": "微信圖片_20260321165747_732_2.jpg"
    },
    {
        "category": "Signature Collection",
        "code": "MG-SG-002",
        "name": "Signature Crystal Candelabra - Limited Edition",
        "description": "Limited edition signature piece",
        "height": "90cm",
        "image": "微信圖片_20260321165749_733_2.jpg"
    },
    {
        "category": "Signature Collection",
        "code": "MG-SG-003",
        "name": "Crystal Candelabra - Designer Series",
        "description": "Designer series crystal candelabra",
        "height": "95cm",
        "image": "微信圖片_20260321165751_735_2.jpg"
    },
    
    # Crystal Masterworks
    {
        "category": "Crystal Masterworks",
        "code": "MG-CM-001",
        "name": "Crystal Masterwork - The Regent",
        "description": "The Regent - masterpiece crystal candelabra",
        "height": "125cm",
        "image": "微信圖片_20260321165848_768_2.jpg"
    },
    {
        "category": "Crystal Masterworks",
        "code": "MG-CM-002",
        "name": "Crystal Masterwork - The Sovereign",
        "description": "The Sovereign - majestic crystal candelabra",
        "height": "130cm",
        "image": "微信圖片_20260321165908_780_2.jpg"
    },
    {
        "category": "Crystal Masterworks",
        "code": "MG-CM-003",
        "name": "Crystal Masterwork - The Monarch",
        "description": "The Monarch - royal crystal candelabra",
        "height": "135cm",
        "image": "微信圖片_20260321165930_798_2.jpg"
    },
]


class ProductPage(Flowable):
    """Custom Flowable for product pages"""
    def __init__(self, product, page_num):
        Flowable.__init__(self)
        self.product = product
        self.page_num = page_num
    
    def wrap(self, availWidth, availHeight):
        return (availWidth, availHeight)
    
    def drawOn(self, canvas, x, y, _sW=0):
        doc_width, doc_height = landscape(A4)
        
        # Background
        canvas.setFillColor(white)
        canvas.rect(0, 0, doc_width, doc_height, fill=1, stroke=0)
        
        # Gold header line
        canvas.setStrokeColor(HexColor("#d4af37"))
        canvas.setLineWidth(2)
        canvas.line(1*cm, doc_height - 1.5*cm, doc_width - 1*cm, doc_height - 1.5*cm)
        
        # Product Code
        canvas.setFont("Helvetica-Bold", 32)
        canvas.setFillColor(HexColor("#1a1a2e"))
        canvas.drawString(1.5*cm, doc_height - 2.5*cm, self.product["code"])
        
        # Product Name
        canvas.setFont("Helvetica-Bold", 20)
        canvas.setFillColor(HexColor("#333333"))
        canvas.drawString(1.5*cm, doc_height - 3.2*cm, self.product["name"])
        
        # Category
        canvas.setFont("Helvetica-Oblique", 12)
        canvas.setFillColor(HexColor("#666666"))
        canvas.drawString(1.5*cm, doc_height - 3.7*cm, self.product["category"])
        
        # Product Image
        img_path = f"assets/candle-{self.product['image']}"
        if os.path.exists(img_path):
            try:
                img = PILImage.open(img_path)
                img_width, img_height = img.size
                
                # Calculate dimensions to fit
                max_width = doc_width - 4*cm
                max_height = doc_height - 10*cm
                ratio = min(max_width/img_width, max_height/img_height)
                
                new_width = img_width * ratio
                new_height = img_height * ratio
                
                # Center the image
                x_pos = (doc_width - new_width) / 2
                y_pos = 3.5*cm
                
                # Resize image
                img_resized = img.resize((int(new_width), int(new_height)), PILImage.LANCZOS)
                temp_path = "temp_catalog_img.jpg"
                img_resized.save(temp_path, "JPEG", quality=95)
                
                # Draw image
                canvas.drawImage(temp_path, x_pos, y_pos,
                              width=new_width, height=new_height,
                              preserveAspectRatio=True)
                
                # Clean up
                os.remove(temp_path)
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")
        
        # Product Information Box
        box_y = 2.5*cm
        
        # Category
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(HexColor("#1a1a2e"))
        canvas.drawString(1.5*cm, box_y, "Category:")
        canvas.setFont("Helvetica", 12)
        canvas.drawString(4.5*cm, box_y, self.product["category"])
        
        # Height
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(HexColor("#1a1a2e"))
        canvas.drawString(13*cm, box_y, "Height:")
        canvas.setFont("Helvetica", 12)
        canvas.drawString(16*cm, box_y, self.product["height"])
        
        # Description
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(HexColor("#1a1a2e"))
        canvas.drawString(1.5*cm, box_y - 0.6*cm, "Description:")
        canvas.setFont("Helvetica", 11)
        canvas.drawString(4.5*cm, box_y - 0.6*cm, self.product["description"])
        
        # Footer line
        canvas.setStrokeColor(HexColor("#d4af37"))
        canvas.setLineWidth(1)
        canvas.line(1*cm, 1.2*cm, doc_width - 1*cm, 1.2*cm)
        
        # Page number
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(HexColor("#808080"))
        canvas.drawRightString(doc_width - 1.5*cm, 0.8*cm, f"Page {self.page_num}")
        
        # Company info
        canvas.setFont("Helvetica-Oblique", 9)
        canvas.setFillColor(HexColor("#666666"))
        canvas.drawString(1.5*cm, 0.8*cm, f"{COMPANY_NAME} | {COMPANY_EMAIL} | {COMPANY_WEBSITE}")


class CoverPage(Flowable):
    """Custom Flowable for cover page"""
    def __init__(self):
        Flowable.__init__(self)
    
    def wrap(self, availWidth, availHeight):
        return (availWidth, availHeight)
    
    def drawOn(self, canvas, x, y, _sW=0):
        doc_width, doc_height = landscape(A4)
        
        # Dark background
        canvas.setFillColor(HexColor("#1a1a2e"))
        canvas.rect(0, 0, doc_width, doc_height, fill=1, stroke=0)
        
        # Gold border
        canvas.setStrokeColor(HexColor("#d4af37"))
        canvas.setLineWidth(3)
        canvas.line(1.5*cm, 1.5*cm, doc_width - 1.5*cm, 1.5*cm)
        canvas.line(1.5*cm, doc_height - 1.5*cm, doc_width - 1.5*cm, doc_height - 1.5*cm)
        
        # Main Title
        canvas.setFont("Helvetica-Bold", 72)
        canvas.setFillColor(HexColor("#d4af37"))
        canvas.drawCentredString(doc_width/2, doc_height/2 + 3*cm, "MIGAC")
        
        canvas.setFont("Helvetica-Bold", 28)
        canvas.setFillColor(white)
        canvas.drawCentredString(doc_width/2, doc_height/2 + 1*cm, "Crystal Candelabra Collection")
        
        canvas.setFont("Helvetica-Oblique", 16)
        canvas.setFillColor(HexColor("#a0a0a0"))
        canvas.drawCentredString(doc_width/2, doc_height/2 - 1*cm, "Premium Quality Crystal Crafts Since 2009")
        
        canvas.setFont("Helvetica", 14)
        canvas.setFillColor(white)
        canvas.drawCentredString(doc_width/2, doc_height/2 - 3*cm, COMPANY_NAME)
        
        canvas.setFont("Helvetica-Oblique", 12)
        canvas.setFillColor(HexColor("#808080"))
        canvas.drawCentredString(doc_width/2, doc_height/2 - 4*cm, f"{COMPANY_EMAIL} | {COMPANY_WEBSITE}")


def generate_catalog():
    """Generate the complete catalog"""
    output_file = "assets/MIGAC_CATALOG_2025_FINAL.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=landscape(A4),
        rightMargin=0,
        leftMargin=0,
        topMargin=0,
        bottomMargin=0
    )
    
    # Build story with pages
    story = []
    
    # Add cover page
    story.append(CoverPage())
    
    # Add product pages with page breaks
    for idx, product in enumerate(PRODUCTS, start=1):
        story.append(PageBreak())
        story.append(ProductPage(product, idx))
    
    # Build PDF
    doc.build(story)
    
    print(f"\n{'='*60}")
    print(f"  ✓ CATALOG GENERATED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"\n  📄 File: {output_file}")
    print(f"  📦 Total Products: {len(PRODUCTS)}")
    print(f"  📖 Total Pages: {len(PRODUCTS) + 1} (including cover)")
    print(f"\n{COMPANY_NAME}")
    print(f"📧 Email: {COMPANY_EMAIL}")
    print(f"🌐 Website: {COMPANY_WEBSITE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  MIGAC Crystal Candelabra Catalog Generator")
    print("=" * 60)
    print(f"\nGenerating catalog with {len(PRODUCTS)} products...\n")
    
    try:
        generate_catalog()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
