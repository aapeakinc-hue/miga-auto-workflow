#!/usr/bin/env python3
"""
Add Request Sample button to free-audit.html
"""

def add_request_sample_button():
    """Add Request Sample button to final CTA section"""
    
    # Read the file
    with open('free-audit.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the final CTA section and add a second button
    old_cta = '''            <a href="#form" class="btn-large">Get My Free Quote Now</a>
            <div class="guarantee">'''
    
    new_cta = '''            <div class="cta-buttons">
                <a href="#form" class="btn-large">Get My Free Quote Now</a>
                <a href="request-sample.html" class="btn-large secondary">Request Free Samples</a>
            </div>
            <div class="guarantee">'''
    
    # Replace
    content = content.replace(old_cta, new_cta)
    
    # Write back
    with open('free-audit.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Added Request Sample button:")
    print("  - Added secondary button for Request Free Samples")
    print("  - Links to request-sample.html")

if __name__ == "__main__":
    print("Adding Request Sample button...")
    print("=" * 60)
    add_request_sample_button()
    print("\n" + "=" * 60)
    print("✓ Done!")
