#!/bin/bash
# MIGAC Website Quick Deployment Script

echo "================================================"
echo "MIGAC Website - Quick Deployment"
echo "================================================"
echo ""

# Check deployment directory
if [ ! -d "cloudflare-deploy" ]; then
    echo "❌ Error: cloudflare-deploy directory not found!"
    exit 1
fi

echo "✅ Found deployment directory"
echo ""

# Count files
echo "📊 Deployment Files:"
echo "-------------------"

# HTML files
html_count=$(find cloudflare-deploy -name "*.html" | wc -l)
echo "HTML Pages: $html_count"

# PDF files
pdf_count=$(find cloudflare-deploy -name "*.pdf" | wc -l)
echo "PDF Catalogs: $pdf_count"

# Images
img_count=$(find cloudflare-deploy/images -type f 2>/dev/null | wc -l)
echo "Images: $img_count"

# CSS files
css_count=$(find cloudflare-deploy -name "*.css" | wc -l)
echo "Stylesheets: $css_count"

echo ""
echo "✅ All deployment files ready!"
echo ""

# Show deployment options
echo "================================================"
echo "Deployment Options:"
echo "================================================"
echo ""
echo "Option A: Manual Upload (Fastest - 5 minutes)"
echo "-------------------------------------------"
echo "1. Go to: https://dash.cloudflare.com"
echo "2. Navigate to: Pages > Create a project"
echo "3. Select 'Upload assets'"
echo "4. Drag and drop the 'cloudflare-deploy/' folder"
echo "5. Click 'Deploy Site'"
echo "6. Wait 2-5 minutes"
echo "7. Get your website URL"
echo ""

echo "Option B: GitHub Integration (Auto-updates)"
echo "-------------------------------------------"
echo "1. Initialize Git:"
echo "   cd cloudflare-deploy"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'English website launch'"
echo "   git branch -M main"
echo ""
echo "2. Create GitHub repository:"
echo "   Go to https://github.com/new"
echo "   Create empty repository"
echo ""
echo "3. Push to GitHub:"
echo "   git remote add origin YOUR_REPO_URL"
echo "   git push -u origin main"
echo ""
echo "4. Connect Cloudflare Pages:"
echo "   Go to Cloudflare Pages Dashboard"
echo "   Select 'Connect to Git'"
echo "   Choose your repository"
echo "   Configure build settings (leave empty)"
echo "   Click 'Save and Deploy'"
echo ""

echo "================================================"
echo "Post-Deployment Checklist:"
echo "================================================"
echo "□ Test all pages load correctly"
echo "□ Test contact form submissions"
echo "□ Verify WhatsApp link works"
echo "□ Test catalog download"
echo "□ Check mobile responsiveness"
echo "□ Add custom domain (optional)"
echo "□ Add Google Analytics (optional)"
echo ""

echo "================================================"
echo "Documentation:"
echo "================================================"
echo "Full deployment guide: DEPLOYMENT.md"
echo "Quick reference: cloudflare-deploy/README_DEPLOYMENT.md"
echo ""

echo "================================================"
echo "Website is READY for deployment! 🚀"
echo "================================================"
