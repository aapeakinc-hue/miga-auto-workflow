#!/usr/bin/env python3
"""
Fix RELATED PRODUCTS section in product-template.html
"""

def fix_related_products():
    """Fix RELATED PRODUCTS section"""
    
    # Read the file
    with open('product-template.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the new related products section with different images and correct links
    new_related_section = '''    <!-- Related Products -->
    <section class="related-section">
        <div class="related-content">
            <h2 class="related-title">Related Products</h2>
            <div class="related-grid">
                <div class="related-card">
                    <div class="related-image">
                        <img src="images/product-9-arms-candelabra.jpg" alt="9 Arms Crystal Candelabra" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <h3>9 Arms Crystal Candelabra</h3>
                    <a href="products.html" class="related-btn">View Details</a>
                </div>

                <div class="related-card">
                    <div class="related-image">
                        <img src="images/product-5-arms-candelabra.jpg" alt="5 Arms Crystal Candelabra" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <h3>5 Arms Crystal Candelabra</h3>
                    <a href="products.html" class="related-btn">View Details</a>
                </div>

                <div class="related-card">
                    <div class="related-image">
                        <img src="images/product-12-arms-candelabra.jpg" alt="12 Arms Grand Crystal" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <h3>12 Arms Grand Crystal</h3>
                    <a href="products.html" class="related-btn">View Details</a>
                </div>

                <div class="related-card">
                    <div class="related-image">
                        <img src="images/candle holders.jpg" alt="Crystal Candle Holder Set" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <h3>Crystal Candle Holder Set</h3>
                    <a href="products.html" class="related-btn">View Details</a>
                </div>
            </div>
        </div>
    </section>'''
    
    # Find and replace the related products section
    import re
    
    # Pattern to match the entire related products section
    pattern = r'    <!-- Related Products -->.*?    </section>\s*    <!-- Footer -->'
    
    # Replace with new section
    new_content = re.sub(pattern, new_related_section + '\n\n    <!-- Footer -->', content, flags=re.DOTALL)
    
    # Write back
    with open('product-template.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✓ Fixed RELATED PRODUCTS section:")
    print("  - Updated all 4 products with different images")
    print("  - Changed all links from '#' to 'products.html'")
    print("  - Updated alt text to match products")

if __name__ == "__main__":
    print("Fixing RELATED PRODUCTS section...")
    print("=" * 60)
    fix_related_products()
    print("\n" + "=" * 60)
    print("✓ Done!")
