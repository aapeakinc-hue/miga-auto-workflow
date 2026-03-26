#!/usr/bin/env python3
"""
将网站文件中的中文内容替换为英文
"""

import re

# 完整的中文到英文翻译映射
translation_map = {
    # 公司信息
    "义乌市邦邺工艺品厂": "Yiwu Bangye Handicraft Factory",
    "义乌市后宅街道城北路L38": "Chengbei Road L38, Houzhai Street, Yiwu City",
    "中国浙江省浦江县水晶路": "Crystal Road, Pujiang County, Zhejiang Province, China",
    "香港嘉明水晶工艺品有限公司": "Kamong Crystal Arts and Crafts Co., Ltd.",
    
    # 通用词汇
    "浏览": "Browse",
    "目录": "Catalog",
    "款式": "Styles",
    "精选": "Featured",
    "展示": "Showcase",
    "卡片": "Card",
    "替换为真实": "Replace with real",
    "图片": "image",
    "产品": "products",
    "立即": "Send",
    "和": "and",
    "联系方式": "Contact Information",
    "我们的专业团队将在": "Our professional team will respond to your inquiry within",
    "小时内回复您的询盘": "hours",
    "号": "No.",
    "北京时间": "Beijing Time",
    "请输入您的": "Please enter your",
    "公司名称": "company name",
    "请输入您的公司名称": "Please enter your company name",
    "号码": "number",
    "请输入您的号码": "Please enter your number",
    "咨询": "Inquiry",
    "索要": "Request",
    "请详细描述您的需求": "Please describe your requirements in detail",
    "包括": "including",
    "类型": "type",
    "数量": "quantity",
    "规格": "specifications",
    "等信息": "and other information",
    "常见问题": "FAQ",
    "最小起订量是多少": "What is the Minimum Order Quantity (MOQ)?",
    "大部分": "Most",
    "的最小起订量是": "products have a minimum order quantity of",
    "件": "pieces",
    
    # 产品相关
    "经典水晶烛台": "Classic Crystal Candelabra",
    "优雅设计": "Elegant Design",
    "适合婚庆": "Perfect for Weddings",
    "装饰": "Decorations",
    "礼品等多种场景": "and Gifts",
    "热销": "Best Seller",
    "奢华水晶吊灯烛台": "Luxury Crystal Chandelier Candelabra",
    "水晶茶烛灯": "Crystal Tea Light Holder",
    "水晶装饰摆件": "Crystal Decorative Ornaments",
    "水晶壁灯": "Crystal Wall Sconce",
    "水晶吊灯": "Crystal Chandelier",
    "工艺精品": "Craft Masterpieces",
    "新品": "New Arrival",
    
    # 公司介绍
    "我们始终坚持": "We always adhere to the",
    "的理念": "philosophy",
    "年专业经验": "years of professional experience",
    "年": "years",
    "成立于": "Founded in",
    "是一家专注于水晶工艺品制造的专业厂家": "is a professional manufacturer specializing in crystal crafts",
    "拥有": "With",
    "生产基地遍布浦江水晶园区": "production bases across Pujiang Crystal Industrial Parks",
    "已服务": "Having served",
    "多个": "multiple",
    "国际客户": "international clients",
    "为全球客户提供高品质的水晶烛台和工艺品": "providing high-quality crystal candelabras and crafts to global clients",
    "提供高品质水晶烛台和工艺品": "providing high-quality crystal candelabras and crafts",
    "出口": "Exported to",
    "远销美国": "the United States",
    "欧洲": "Europe",
    "中东等": "the Middle East and other regions",
    "包括批发商": "including wholesalers",
    "零售商": "retailers",
    "婚庆公司等": "wedding companies, and more",
    "专为酒店": "Specializing for hotels",
    "餐厅设计": "restaurant designs",
    "工程款": "engineering projects",
    
    # 品质保证
    "品质第一": "Quality First",
    "客户至上": "Customer First",
    "都经过严格质检": "All undergo strict quality inspection",
    "支持质量保证": "Support quality assurance",
    "有什么质量保证": "What quality guarantees do you offer?",
    "质量认证": "quality certification",
    
    # 营销相关
    "营造温馨氛围": "Creating a warm atmosphere",
    "点亮您的空间": "Light up your space",
    "彰显尊贵品质": "Showcasing noble quality",
    "提升空间品味": "Elevating spatial taste",
    "精致小巧": "Exquisite and compact",
    "奢华大气": "Luxurious and grand",
    "独特设计": "Unique design",
    "工艺精湛": "Exquisite craftsmanship",
    "高端品质": "High-end quality",
    "高端定制": "High-end customization",
    
    # 服务相关
    "服务": "Service",
    "我们的": "Our",
    "我们会在": "We will",
    "我们都能满足您的需求": "we can meet all your needs",
    "无论是现货": "Whether it's in-stock items",
    "还是": "or",
    "定制款": "customized orders",
    "如需立即咨询": "If you need immediate consultation",
    "我们支持": "We support",
    "我们支持小批量试单": "We support small batch trial orders",
    "我们有丰富的国际物流经验": "We have extensive international logistics experience",
    "可以帮助处理清关": "can help handle customs clearance",
    "运输等事宜": "shipping and other logistics",
    "我们拥有专业的设计团队": "We have a professional design team",
    "支持根据您的需求进行定制": "support customization according to your needs",
    "对于": "For",
    "对于新客户": "For new customers",
    "通常需要": "usually requires",
    "天": "days",
    "通常": "Typically",
    "天发货": "days to ship",
    "具体取决于订单数量和复杂程度": "specifically depends on order quantity and complexity",
    "生产周期需要多久": "What is the production cycle?",
    "具体起订量请咨询我们的销售团队": "For specific MOQ, please consult our sales team",
    
    # 支付和物流
    "支持国际配送吗": "Do you support international delivery?",
    "支持全球配送": "We support global delivery",
    "支持什么付款方式": "What payment methods do you support?",
    "我们通过": "We accept",
    "等付款方式": "and other payment methods",
    "付款": "payment",
    "定金": "deposit",
    "发货前支付": "pay before shipping",
    "如果": "if",
    "有任何问题": "you have any questions",
    "请": "please",
    "联系我们": "contact us",
    "包装设计等": "packaging design, and more",
    
    # 表单相关
    "处理表单提交成功后的显示": "Handle successful form submission display",
    "提交成功": "Submitted Successfully",
    "提交失败": "Submission Failed",
    "请稍后重试": "Please try again later",
    "你好": "Hello",
    "我想咨询水晶烛台": "I want to inquire about crystal candelabras",
    "我们会在": "We will",
    "秒后滚动到成功消息": "scroll to success message after seconds",
    "可使用": "Available",
    
    # 导航和链接
    "快速链接": "Quick Links",
    "联系": "Contact",
    "关于": "About",
    "下载": "Download",
    "更多": "More",
    "查看": "View",
    "详情": "Details",
    "地址": "Address",
    "中心": "Center",
    
    # 表单字段
    "提交": "Submit",
    "重置": "Reset",
    "姓名": "Name",
    "邮箱": "Email",
    "电话": "Phone",
    "消息": "Message",
    "发送": "Send",
    "收到": "Received",
    "谢谢": "Thank you",
    "我们会尽快回复": "We will reply as soon as possible",
    "平滑滚动": "Smooth scroll",
    
    # 下载相关
    "网站文件下载": "Website File Download",
    "下载后的操作步骤": "Post-download Steps",
    "步骤": "Steps",
    "点击下载": "Click to Download",
    "解压文件": "Extract Files",
    "打开": "Open",
    "配置域名": "Configure Domain",
    "上传文件": "Upload Files",
    "部署指南": "Deployment Guide",
    "验证网站": "Verify Website",
    "访问": "Visit",
    "推荐": "Recommended",
    "预计总时间": "Estimated Total Time",
    "分钟": "minutes",
    "解压到当前文件夹": "Extract to current folder",
    "拖拽": "Drag",
    "文件夹": "Folder",
    "单个文件下载": "Individual File Download",
    "下载压缩包": "Download ZIP",
    "下载后解压得到": "Extract after download to get",
    "右键点击下载的压缩包": "Right-click on downloaded ZIP",
    "添加": "Add",
    "选择": "Select",
    "所有": "All",
    "处理": "process",
    "是的": "Yes",
    "是否支持": "Do you support",
    "需要": "Need",
    "设计": "Design",
    "定制": "Customization",
}

def replace_chinese_in_file(filename):
    """替换文件中的中文内容"""
    with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计替换次数
    replace_count = 0
    
    # 按长度从长到短排序，避免部分替换
    sorted_translations = sorted(translation_map.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        if chinese in content:
            content = content.replace(chinese, english)
            replace_count += 1
            print(f"  ✓ {chinese} → {english}")
    
    # 保存文件
    with open(f'cloudflare-deploy/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return replace_count

# 处理所有文件
files = ['index.html', 'about.html', 'products.html', 'contact.html', 'download.html']

print("=" * 80)
print("开始替换中文内容为英文...")
print("=" * 80)
print()

total_replaced = 0

for filename in files:
    print(f"\n处理 {filename}:")
    print("-" * 80)
    
    # 先检查有多少中文
    with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    before_count = len(chinese_pattern.findall(content))
    
    if before_count > 0:
        count = replace_chinese_in_file(filename)
        total_replaced += count
        print(f"\n✅ 替换了 {count} 处中文内容")
        
        # 验证
        with open(f'cloudflare-deploy/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        after_count = len(chinese_pattern.findall(content))
        
        if after_count == 0:
            print(f"✅ 验证通过：无剩余中文")
        else:
            print(f"⚠️  警告：还有 {after_count} 处中文未翻译")
    else:
        print("  无中文内容")

print("\n" + "=" * 80)
print("替换完成")
print("=" * 80)
print(f"\n总计替换了 {total_replaced} 处中文内容")
print("\n下一步：")
print("1. 重新部署到 Cloudflare Pages")
print("2. 测试所有页面")
print("3. 确认无中文内容")
