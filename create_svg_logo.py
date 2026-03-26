#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 SVG 格式的 Logo（矢量格式，可在 CorelDRAW 中打开）
"""

# SVG 格式的 Logo - 专业设计
svg_logo = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" width="400" height="120">
  <!-- Background (optional, remove if you want transparent) -->
  <!-- <rect width="400" height="120" fill="white" /> -->

  <!-- Logo Text - MIGAC -->
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&amp;display=swap');
      .logo-text {
        font-family: 'Montserrat', 'Arial', sans-serif;
        font-weight: 900;
        font-size: 64px;
        fill: #1a237e;
        letter-spacing: 4px;
      }
      .logo-dot {
        font-family: 'Montserrat', 'Arial', sans-serif;
        font-weight: 900;
        font-size: 64px;
        fill: #FFD700;
      }
      .tagline {
        font-family: 'Montserrat', 'Arial', sans-serif;
        font-weight: 700;
        font-size: 14px;
        fill: #0d47a1;
        letter-spacing: 8px;
        text-transform: uppercase;
      }
    </style>
  </defs>

  <!-- Main Logo Text -->
  <text x="20" y="75" class="logo-text">MIGAC</text>
  <text x="230" y="75" class="logo-dot">.</text>

  <!-- Tagline -->
  <text x="20" y="100" class="tagline">Crystal Crafts</text>

  <!-- Decorative Crystal Element -->
  <g transform="translate(310, 20)">
    <!-- Crystal Shape -->
    <polygon points="40,0 80,30 80,70 40,100 0,70 0,30" fill="#1a237e" opacity="0.9"/>
    <polygon points="40,10 70,35 70,65 40,90 10,65 10,35" fill="#0d47a1" opacity="0.8"/>
    <polygon points="40,20 60,40 60,60 40,80 20,60 20,40" fill="#FFD700" opacity="0.6"/>
    <!-- Highlight -->
    <polygon points="40,25 55,40 40,55 25,40" fill="white" opacity="0.3"/>
  </g>
</svg>'''

# 保存 SVG 文件
with open('cloudflare-deploy/images/MIGAC_logo.svg', 'w', encoding='utf-8') as f:
    f.write(svg_logo)

print("✅ SVG Logo created: cloudflare-deploy/images/MIGAC_logo.svg")
print("   This is a vector format that can be opened in CorelDRAW")
print("   File can be edited and saved as CDR format in CorelDRAW")

# 同时创建一个简化版本（更小的尺寸）
svg_logo_small = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" width="200" height="50">
  <defs>
    <style>
      .logo-text {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 32px;
        fill: #1a237e;
        letter-spacing: 2px;
      }
      .logo-dot {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 32px;
        fill: #FFD700;
      }
    </style>
  </defs>

  <text x="10" y="35" class="logo-text">MIGAC</text>
  <text x="115" y="35" class="logo-dot">.</text>

  <!-- Small Crystal -->
  <g transform="translate(145, 5)">
    <polygon points="15,0 30,10 30,30 15,40 0,30 0,10" fill="#1a237e" opacity="0.9"/>
    <polygon points="15,8 24,16 24,24 15,32 6,24 6,16" fill="#FFD700" opacity="0.6"/>
  </g>
</svg>'''

with open('cloudflare-deploy/images/MIGAC_logo_small.svg', 'w', encoding='utf-8') as f:
    f.write(svg_logo_small)

print("✅ Small SVG Logo created: cloudflare-deploy/images/MIGAC_logo_small.svg")
print("\n📝 How to use:")
print("1. Open SVG file in CorelDRAW")
print("2. Edit as needed (change colors, fonts, etc.)")
print("3. Save as CDR format: File > Save As > CDR")
print("\n💡 SVG is a vector format, so it can be scaled to any size without quality loss!")
