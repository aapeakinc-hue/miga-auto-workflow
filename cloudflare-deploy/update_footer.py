#!/usr/bin/env python3
"""
更新所有页面的 Footer
- 简化左侧公司简介
- 优化中间栏目间距
- 添加地址信息
"""

import os
import re

# 新的 Footer 内容
NEW_FOOTER = '''    <footer class="footer">
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
</html>'''

# 需要更新的文件列表
FILES_TO_UPDATE = [
    'index.html',
    'products.html',
    'about.html',
    'contact.html',
    'best-sellers.html',
    'wedding-collection.html',
    'event-collection.html',
    'rental-collection.html',
    'luxury-collection.html',
    'catalog.html',
    'free-audit.html',
    'faq.html',
    'case-studies.html'
]

def update_file_footer(filepath):
    """更新单个文件的 Footer"""
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换 footer 部分
    # 使用正则表达式匹配从 <footer class="footer"> 到 </footer> 的内容
    footer_pattern = r'<footer class="footer">.*?</footer>'
    
    # 先检查是否有 footer
    if '<footer class="footer">' not in content:
        print(f"⚠️  {filepath} 中没有找到 footer")
        return False
    
    # 替换 footer
    new_content = re.sub(footer_pattern, NEW_FOOTER.split('</body>')[0], content, flags=re.DOTALL)
    
    # 删除旧的 WhatsApp 按钮
    whatsapp_pattern = r'<!-- WhatsApp Float Button -->.*?<a href="https://wa\.me/8619879476613"[^>]*>.*?</a>'
    new_content = re.sub(whatsapp_pattern, '', new_content, flags=re.DOTALL)
    
    # 确保文件以 </body></html> 结尾
    if not new_content.strip().endswith('</body></html>'):
        # 移除旧的结束标签
        new_content = re.sub(r'</body>\s*</html>\s*$', '', new_content.strip())
        # 添加新的结束标签
        new_content = new_content.strip() + '\n</body>\n</html>'
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已更新: {filepath}")
    return True

def main():
    print("开始更新 Footer...\n")
    
    updated_count = 0
    for filename in FILES_TO_UPDATE:
        if update_file_footer(filename):
            updated_count += 1
    
    print(f"\n✅ 完成！共更新 {updated_count} 个文件")

if __name__ == '__main__':
    main()
