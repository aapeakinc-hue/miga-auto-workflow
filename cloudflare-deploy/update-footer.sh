#!/bin/bash

# Footer 模板
NEW_FOOTER='    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>MIGAC Crystal Crafts</h3>
                <p>Professional crystal crafts manufacturer since 2009. Serving 182+ international clients worldwide.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <a href="index.html">Home</a>
                <a href="products.html">Products</a>
                <a href="about.html">About Us</a>
                <a href="contact.html">Contact</a>
            </div>
            <div class="footer-section">
                <h3>Products</h3>
                <a href="products.html">Crystal Candle Holders</a>
                <a href="products.html">Candelabras</a>
                <a href="products.html">Decorative Crafts</a>
                <a href="products.html">Custom Designs</a>
            </div>
            <div class="footer-section">
                <h3>Contact</h3>
                <p>📧 info@miga.cc</p>
                <p>📱 Phone/WhatsApp: +86 19879476613</p>
                <p>💬 WeChat: Migac1319</p>
                <p>📍 Crystal Industrial Park, Pujiang, China</p>
                <p>🌐 www.miga.cc</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 MIGAC Crystal Crafts Co., Ltd. All Rights Reserved.</p>
        </div>
    </footer>

    <!-- WhatsApp Float Button -->
    <a href="https://wa.me/8619879476613" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">
        💬
    </a>
</body>
</html>'

# 需要更新的文件列表
FILES="index.html products.html about.html contact.html best-sellers.html wedding-collection.html event-collection.html rental-collection.html luxury-collection.html catalog.html free-audit.html faq.html case-studies.html"

# 循环更新每个文件
for file in $FILES; do
    if [ -f "$file" ]; then
        echo "Updating $file..."
        # 删除旧的 footer 和 whatsapp 按钮
        sed -i '/^    <footer class="footer">/,/^<\/footer>/d' "$file"
        sed -i '/^    <!-- WhatsApp Float Button -->/,/^    <a href="https:\/\/wa.me\/8619879476613"/d' "$file"
        sed -i '/^    <a href="https:\/\/wa.me\/8619879476613"/d' "$file"
        
        # 删除旧的 </body> 和 </html>
        sed -i '/^<\/body>$/d' "$file"
        sed -i '/^<\/html>$/d' "$file"
        
        # 添加新的 footer 和结束标签
        echo "$NEW_FOOTER" >> "$file"
        echo "✓ $file updated"
    fi
done

echo "All files updated!"
