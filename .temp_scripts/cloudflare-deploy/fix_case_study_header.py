#!/usr/bin/env python3
"""
Fix case-studies.html header navigation button
"""

def fix_header_button():
    """Fix the header-cta to header-btn class"""
    
    # Read the file
    with open('case-studies.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace header-cta class with header-btn
    old_link = '''            <a href="request-sample.html" class="header-cta">Get Free Samples</a>'''
    
    new_link = '''            <a href="request-sample.html" class="header-btn">Get Free Samples</a>'''
    
    content = content.replace(old_link, new_link)
    
    # Write back
    with open('case-studies.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Fixed header navigation button:")
    print("  - Changed class from 'header-cta' to 'header-btn'")
    print("  - Button will now display correctly with proper styling")

if __name__ == "__main__":
    print("Fixing case-studies header navigation...")
    print("=" * 60)
    fix_header_button()
    print("\n" + "=" * 60)
    print("✓ Done!")
