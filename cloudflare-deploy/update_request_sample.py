#!/usr/bin/env python3
"""
Update request-sample.html with new sample images
"""

import re

# New sample data
new_samples = [
    {
        "filename": "sample-01.jpg",
        "title": "Classic Crystal Candelabra",
        "description": "Multi-Arm Design, gold plated base",
        "price": "Wholesale: $15-25/pc"
    },
    {
        "filename": "sample-02.jpg",
        "title": "Crystal Tea Light Holder",
        "description": "Set of 4, elegant design",
        "price": "Wholesale: $3-6/set"
    },
    {
        "filename": "sample-03.jpg",
        "title": "Luxury Crystal Chandelier",
        "description": "Suspension style, Multi-Arm Design",
        "price": "Wholesale: $80-150/pc"
    },
    {
        "filename": "sample-04.jpg",
        "title": "Crystal Wall Sconce",
        "description": "Modern design, easy installation",
        "price": "Wholesale: $12-22/pc"
    },
    {
        "filename": "sample-05.jpg",
        "title": "Crystal Decorative Ornament",
        "description": "Perfect for gifts & decor",
        "price": "Wholesale: $2-5/pc"
    },
    {
        "filename": "sample-06.jpg",
        "title": "Crystal Votive Set",
        "description": "Set of 6, clear crystal",
        "price": "Wholesale: $4-8/set"
    },
    {
        "filename": "sample-07.jpg",
        "title": "Premium Crystal Candelabra",
        "description": "Large multi-arm, premium quality",
        "price": "Wholesale: $25-40/pc"
    },
    {
        "filename": "sample-08.jpg",
        "title": "Elegant Crystal Holder",
        "description": "Simple yet elegant design",
        "price": "Wholesale: $8-15/pc"
    },
    {
        "filename": "sample-09.jpg",
        "title": "Crystal Candle Stand",
        "description": "Sturdy base, crystal accents",
        "price": "Wholesale: $10-18/pc"
    },
    {
        "filename": "sample-10.jpg",
        "title": "5-Arm Crystal Candelabra",
        "description": "Classic 5-arm design, perfect centerpiece",
        "price": "Wholesale: $18-28/pc"
    },
    {
        "filename": "sample-11.jpg",
        "title": "9-Arm Crystal Candelabra",
        "description": "Grand 9-arm design, luxury style",
        "price": "Wholesale: $35-55/pc"
    },
    {
        "filename": "sample-12.jpg",
        "title": "9-Candlesticks Candelabra",
        "description": "Classic candlestick design, elegant",
        "price": "Wholesale: $30-45/pc"
    },
    {
        "filename": "sample-13.jpg",
        "title": "Crystal Candle Holder",
        "description": "Single holder, crystal clear",
        "price": "Wholesale: $5-10/pc"
    },
    {
        "filename": "sample-14.jpg",
        "title": "Elegant Candlestick",
        "description": "Traditional design, premium finish",
        "price": "Wholesale: $7-12/pc"
    }
]

def generate_sample_card(sample, index):
    """Generate HTML for a sample card"""
    return f'''            <div class="sample-card" data-product="{sample['title']}" onclick="toggleSample(this)">
                <img src="products/{sample['filename']}" alt="{sample['title']}" class="sample-image">
                <div class="sample-info">
                    <h3>{sample['title']}</h3>
                    <p>{sample['description']}</p>
                    <div class="sample-price">{sample['price']}</div>
                    <div class="sample-cta">Click to Select</div>
                </div>
            </div>'''

def update_request_sample_html():
    """Update request-sample.html with new sample images"""
    
    # Read the HTML file
    with open('request-sample.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find the sample grid section
    # Pattern to match from <div class="sample-grid" id="sampleGrid"> to </div> (closing of sample-grid)
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
    print(f"  - Replaced old sample images with {len(new_samples)} new images")
    print(f"  - Updated product information for all samples")

if __name__ == "__main__":
    print("Updating request-sample.html with new sample images...")
    print("=" * 60)
    
    update_request_sample_html()
    
    print("\n" + "=" * 60)
    print("✓ Done!")
