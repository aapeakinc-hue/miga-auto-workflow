#!/usr/bin/env python3
"""
Update request-sample.html with correct image paths
"""

import re

# New sample data with correct image paths
new_samples = [
    {
        "filename": "images/sample_微信圖片_20260321162810_44_2.jpg",
        "title": "Classic Crystal Candelabra",
        "description": "Multi-Arm Design, gold plated base",
        "price": "Wholesale: $15-25/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321165154_518_2.jpg",
        "title": "Crystal Tea Light Holder",
        "description": "Set of 4, elegant design",
        "price": "Wholesale: $3-6/set"
    },
    {
        "filename": "images/sample_微信圖片_20260321165225_547_2.jpg",
        "title": "Luxury Crystal Chandelier",
        "description": "Suspension style, Multi-Arm Design",
        "price": "Wholesale: $80-150/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321165229_552_2.jpg",
        "title": "Crystal Wall Sconce",
        "description": "Modern design, easy installation",
        "price": "Wholesale: $12-22/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321162605_25_2.jpg",
        "title": "Crystal Decorative Ornament",
        "description": "Perfect for gifts & decor",
        "price": "Wholesale: $2-5/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321163151_67_2.jpg",
        "title": "Crystal Votive Set",
        "description": "Set of 6, clear crystal",
        "price": "Wholesale: $4-8/set"
    },
    {
        "filename": "images/sample_微信圖片_20260321165244_569_2.jpg",
        "title": "Premium Crystal Candelabra",
        "description": "Large multi-arm, premium quality",
        "price": "Wholesale: $25-40/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321165337_622_2.jpg",
        "title": "Elegant Crystal Holder",
        "description": "Simple yet elegant design",
        "price": "Wholesale: $8-15/pc"
    },
    {
        "filename": "images/sample_微信圖片_20260321165358_643_2.jpg",
        "title": "Crystal Candle Stand",
        "description": "Sturdy base, crystal accents",
        "price": "Wholesale: $10-18/pc"
    },
    {
        "filename": "images/sample_5_arms_candelabras.jpg",
        "title": "5-Arm Crystal Candelabra",
        "description": "Classic 5-arm design, perfect centerpiece",
        "price": "Wholesale: $18-28/pc"
    },
    {
        "filename": "images/sample_9_arms_candelabra.jpg",
        "title": "9-Arm Crystal Candelabra",
        "description": "Grand 9-arm design, luxury style",
        "price": "Wholesale: $35-55/pc"
    },
    {
        "filename": "images/sample_9_candlesticks_candelabra.jpg",
        "title": "9-Candlesticks Candelabra",
        "description": "Classic candlestick design, elegant",
        "price": "Wholesale: $30-45/pc"
    },
    {
        "filename": "images/sample_candle_holder.jpg",
        "title": "Crystal Candle Holder",
        "description": "Single holder, crystal clear",
        "price": "Wholesale: $5-10/pc"
    },
    {
        "filename": "images/sample_candlestick.jpg",
        "title": "Elegant Candlestick",
        "description": "Traditional design, premium finish",
        "price": "Wholesale: $7-12/pc"
    }
]

def generate_sample_card(sample, index):
    """Generate HTML for a sample card"""
    return f'''            <div class="sample-card" data-product="{sample['title']}" onclick="toggleSample(this)">
                <img src="{sample['filename']}" alt="{sample['title']}" class="sample-image">
                <div class="sample-info">
                    <h3>{sample['title']}</h3>
                    <p>{sample['description']}</p>
                    <div class="sample-price">{sample['price']}</div>
                    <div class="sample-cta">Click to Select</div>
                </div>
            </div>'''

def update_request_sample_html():
    """Update request-sample.html with correct image paths"""
    
    # Read the HTML file
    with open('request-sample.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find the sample grid section
    pattern = r'(<div class="sample-grid" id="sampleGrid">)(.*?)(</div>\s*</section>)'
    
    # Generate new sample cards HTML
    new_cards_html = "\n".join([generate_sample_card(sample, i) for i, sample in enumerate(new_samples, 1)])
    
    # Replace the sample grid content
    new_sample_grid = f'''<div class="sample-grid" id="sampleGrid">
{new_cards_html}
        </div>'''
    
    # Replace in HTML
    html_content = re.sub(pattern, new_sample_grid, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    with open('request-sample.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ Updated request-sample.html:")
    print(f"  - Changed image paths from products/ to images/")
    print(f"  - Updated with {len(new_samples)} sample images")
    print(f"  - All images now point to images/ directory")

if __name__ == "__main__":
    print("Updating request-sample.html with correct image paths...")
    print("=" * 60)
    
    update_request_sample_html()
    
    print("\n" + "=" * 60)
    print("✓ Done!")
