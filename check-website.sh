#!/bin/bash
# MIGAC Website Local Check Script

echo "================================================"
echo "MIGAC Website - Local File Check"
echo "================================================"
echo ""

# Check if cloudflare-deploy directory exists
if [ ! -d "cloudflare-deploy" ]; then
    echo "❌ Error: cloudflare-deploy directory not found!"
    exit 1
fi

cd cloudflare-deploy

echo "✅ Found deployment directory"
echo ""

# Check HTML files
echo "📄 HTML Files Check:"
echo "-------------------"
html_files=("index.html" "about.html" "products.html" "contact.html" "download.html")
for file in "${html_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "✓ $file ($size)"
    else
        echo "✗ $file (missing)"
    fi
done
echo ""

# Check PDF files
echo "📄 PDF Files Check:"
echo "-------------------"
if [ -f "MIGAC_CATALOG_2025_FINAL.pdf" ]; then
    size=$(du -h "MIGAC_CATALOG_2025_FINAL.pdf" | cut -f1)
    echo "✓ MIGAC_CATALOG_2025_FINAL.pdf ($size)"
else
    echo "✗ MIGAC_CATALOG_2025_FINAL.pdf (missing)"
fi
echo ""

# Check CSS files
echo "🎨 CSS Files Check:"
echo "-------------------"
if [ -f "style.css" ]; then
    size=$(du -h "style.css" | cut -f1)
    echo "✓ style.css ($size)"
else
    echo "✗ style.css (missing)"
fi
echo ""

# Check Images
echo "🖼️ Images Check:"
echo "-------------------"
if [ -d "images" ]; then
    img_count=$(find images -type f | wc -l)
    img_size=$(du -h images | cut -f1)
    echo "✓ images/ directory exists"
    echo "  Total images: $img_count"
    echo "  Total size: $img_size"
else
    echo "✗ images/ directory not found"
fi
echo ""

# Check other files
echo "📋 Other Files Check:"
echo "-------------------"
other_files=("robots.txt" "sitemap.xml" "README.md")
for file in "${other_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (missing)"
    fi
done
echo ""

# Total files
total_files=$(find . -type f | wc -l)
total_size=$(du -h . | cut -f1)

echo "================================================"
echo "Summary:"
echo "================================================"
echo "Total files: $total_files"
echo "Total size: $total_size"
echo ""

# Check for common issues
echo "🔍 Common Issues Check:"
echo "-------------------"

# Check index.html for catalog link
if [ -f "index.html" ]; then
    if grep -q "MIGAC_CATALOG_2025_FINAL.pdf" index.html; then
        echo "✓ Index.html has correct catalog link"
    else
        echo "⚠ Index.html catalog link may be incorrect"
    fi
fi

# Check products.html for catalog link
if [ -f "products.html" ]; then
    if grep -q "MIGAC_CATALOG_2025_FINAL.pdf" products.html; then
        echo "✓ Products.html has correct catalog link"
    else
        echo "⚠ Products.html catalog link may be incorrect"
    fi
fi

echo ""
echo "================================================"
echo "✅ Local files check completed!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Upload cloudflare-deploy/ to Cloudflare Pages"
echo "2. Configure DNS to point to Pages"
echo "3. Test website access"
echo ""
