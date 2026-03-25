"""
简化版自动化工作流（带自动重试和健康检查）
每天 9 点自动运行，增强稳定性和容错能力
"""
import os
import sys
import json
import random
import requests
from datetime import datetime, timedelta
import logging

# 添加 utils 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入重试和健康检查工具
from utils.retry_utils import retry_on_failure, APIHealthChecker, log_retry_attempt

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Keys
SNOVIO_API_KEY = os.getenv('SNOVIO_API_KEY', '')
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# 优化关键词列表
OPTIMIZED_KEYWORDS = [
    # 美国市场
    "crystal candle holders wholesale USA",
    "crystal candelabra importers America",
    "crystal home decor wholesalers United States",
    "luxury crystal decor buyers USA",

    # 欧洲市场
    "crystal candle holders wholesalers UK",
    "crystal candelabra importers Europe",
    "crystal home decor distributors Germany",
    "luxury crystal decor buyers France",

    # 特定客户类型
    "gift shops crystal decor wholesalers",
    "home decor stores crystal candle holders",
    "wedding planners crystal candelabra suppliers",
    "luxury hotels crystal decor suppliers",

    # 批发商
    "crystal candle holders bulk buyers",
    "crystal candelabra wholesale importers"
]

# 发送历史文件
SENT_EMAILS_FILE = "logs/sent_emails.json"


def load_sent_emails():
    """加载已发送记录"""
    try:
        if os.path.exists(SENT_EMAILS_FILE):
            with open(SENT_EMAILS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"加载发送记录失败: {e}")
        return []


def save_sent_emails(sent_emails):
    """保存发送记录"""
    try:
        os.makedirs(os.path.dirname(SENT_EMAILS_FILE), exist_ok=True)
        with open(SENT_EMAILS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sent_emails, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存发送记录失败: {e}")


def is_email_sent(email, sent_emails, days=30):
    """检查邮箱是否已发送过"""
    if not sent_emails:
        return False

    cutoff_date = datetime.now() - timedelta(days=days)

    for record in sent_emails:
        if record.get('email') == email:
            send_date = datetime.fromisoformat(record.get('date', ''))
            if send_date > cutoff_date:
                return True

    return False


def search_customers(keyword):
    """搜索潜在客户（模拟）"""
    logger.info(f"正在搜索关键词: {keyword}")

    # 使用模拟数据（实际应该使用 Web Search API）
    mock_customers = [
        {
            "company": "Crystal Decor Imports",
            "website": "www.crystalimports.com",
            "description": "Wholesale crystal candle holders importer",
            "country": "USA"
        },
        {
            "company": "Luxury Home Decor Wholesale",
            "website": "www.luxuryhome.com",
            "description": "Home decor wholesaler specializing in crystal products",
            "country": "USA"
        },
        {
            "company": "European Crystal Supply",
            "website": "www.europeancrystal.eu",
            "description": "Crystal candelabra distributor in Europe",
            "country": "Germany"
        }
    ]

    logger.info(f"找到 {len(mock_customers)} 个潜在客户")
    return mock_customers


@retry_on_failure(
    max_retries=3,
    backoff_factor=2.0,
    allowed_exceptions=(requests.exceptions.RequestException,),
    on_retry=log_retry_attempt
)
def get_email_from_website(website):
    """
    从网站获取邮箱（使用 Snov.io API 或估算）
    带自动重试功能
    """
    try:
        # 尝试使用 Snov.io API（如果配置了）
        if SNOVIO_API_KEY:
            logger.info(f"使用 Snov.io API 获取邮箱: {website}")

            url = f"https://api.snov.io/v2/domain-emails-with-info"
            headers = {
                'Authorization': SNOVIO_API_KEY,
                'Content-Type': 'application/json'
            }
            data = {'domain': website}

            response = requests.post(url, json=data, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                emails = result.get('data', {}).get('emails', [])
                if emails:
                    email = emails[0].get('email')
                    logger.info(f"从 Snov.io 获取到邮箱: {email}")
                    return email
            else:
                logger.warning(f"Snov.io API 调用失败: {response.status_code}")

        # 如果 Snovio 失败，使用估计邮箱
        logger.info(f"使用估计邮箱: contact@{website}")
        return f"contact@{website}"

    except requests.exceptions.Timeout:
        logger.error(f"获取邮箱超时: {website}")
        raise
    except requests.exceptions.ConnectionError:
        logger.error(f"获取邮箱连接失败: {website}")
        raise
    except Exception as e:
        logger.error(f"获取邮箱失败: {e}")
        # 使用估计邮箱作为备选
        return f"contact@{website}"


def generate_email_content(customer, keyword):
    """生成邮件内容（使用模拟或 OpenAI API）"""
    logger.info(f"正在生成邮件内容: {customer['company']}")

    # 提取公司名称（用于个性化）
    company_name = customer.get('company', 'there')
    website = customer.get('website', '')
    country = customer.get('country', '')

    # 个性化邮件主题
    subject = f"Unique Crystal Products for {company_name}"

    # 吸引人的邮件正文
    email_content = {
        "subject": subject,
        "body": f"""Dear Team at {company_name},

I came across your website while searching for premium crystal gift suppliers, and I was impressed by your selection.

I'm writing to introduce Migac - we specialize in crystal gifts and crafts that have been delighting wholesalers and retailers worldwide for over 10 years.

Why Partner with Migac?

✨ Exquisite Craftsmanship
Every piece is handcrafted by skilled artisans with precision and care.

🌟 Product Range
- Crystal candle holders and candelabras
- Decorative crystal figurines
- Crystal gifts and crafts for all occasions
- Custom OEM/ODM designs

💰 Competitive Advantage
- Factory-direct pricing (30-40% below market)
- MOQ as low as 50 pieces
- Fast delivery within 15 days
- Free samples available

I believe our crystal collection would be a perfect addition to your product line and could help you stand out from competitors.

Quick Question:
Are you currently looking for new crystal suppliers for your upcoming season?

I'd love to send you our catalog and some sample photos to show you what makes Migac different.

Looking forward to your reply.

Best regards,

Aldrich Qi
Sales Director
Migac
Email: info@miga.cc
Website: www.miga.cc
Phone/WhatsApp: 19879476613

P.S. Reply "CATALOG" and I'll send you our latest 2024 crystal collection immediately.
"""
    }

    return email_content


@retry_on_failure(
    max_retries=3,
    backoff_factor=2.0,
    allowed_exceptions=(requests.exceptions.RequestException,),
    on_retry=log_retry_attempt
)
def send_email(to_email, subject, body):
    """
    发送邮件（使用 Resend API）
    带自动重试功能
    """
    if not RESEND_API_KEY:
        error_msg = "RESEND_API_KEY 未配置"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"正在发送邮件到: {to_email}")

    url = "https://api.resend.com/emails"
    headers = {
        'Authorization': f'Bearer {RESEND_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'from': 'info@miga.cc',
        'to': to_email,
        'subject': subject,
        'html': body.replace('\n', '<br>')
    }

    response = requests.post(url, json=data, headers=headers, timeout=30)

    if response.status_code == 200:
        result = response.json()
        logger.info(f"邮件发送成功: {result.get('id')}")
        return {'success': True, 'message_id': result.get('id')}
    elif response.status_code == 429:
        logger.error("邮件发送失败: 限流（429）")
        raise requests.exceptions.HTTPError("API 限流")
    elif response.status_code >= 500:
        logger.error(f"邮件发送失败: 服务器错误 {response.status_code}")
        raise requests.exceptions.HTTPError(f"服务器错误: {response.status_code}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        logger.error(f"邮件发送失败: {error_msg}")
        raise ValueError(f"API 错误: {error_msg}")


def generate_report(keyword, sent_count, total_count):
    """生成每日报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 每日外贸客户开发报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 时间: {timestamp}
🔍 关键词: {keyword}

📊 发送统计:
  - 总数: {total_count}
  - 成功: {sent_count}
  - 失败: {total_count - sent_count}

💡 建议:
  - 定期检查邮箱回复
  - 跟进有兴趣的客户
  - 优化关键词和邮件内容

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    logger.info(report)

    # 保存报告到文件
    try:
        os.makedirs("logs", exist_ok=True)
        report_file = f"logs/daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"报告已保存: {report_file}")
    except Exception as e:
        logger.error(f"保存报告失败: {e}")


def run_health_check():
    """运行 API 健康检查"""
    logger.info("🏥 开始 API 健康检查...")

    health_checker = APIHealthChecker()

    # 检查所有 API
    health_results = health_checker.check_all_apis(
        snovio_key=SNOVIO_API_KEY,
        resend_key=RESEND_API_KEY
    )

    # 生成报告
    report = health_checker.generate_health_report(health_results)
    logger.info(report)

    # 检查整体健康状态
    if health_results['overall_status'] == 'degraded':
        logger.warning("⚠️  部分 API 健康检查失败，工作流可能受到影响")

    return health_results


def auto_run_workflow():
    """自动运行工作流（带健康检查）"""
    logger.info("🤖 自动化外贸客户开发工作流启动")
    logger.info("=" * 50)

    # 1. 运行健康检查
    logger.info("\n")
    health_results = run_health_check()
    logger.info("\n")

    # 2. 加载已发送记录
    sent_emails = load_sent_emails()
    logger.info(f"📋 已发送记录: {len(sent_emails)} 条")

    # 3. 随机选择关键词
    selected_keyword = random.choice(OPTIMIZED_KEYWORDS)
    logger.info(f"🔍 今日关键词: {selected_keyword}")

    # 4. 搜索客户
    customers = search_customers(selected_keyword)

    if not customers:
        logger.warning("没有找到客户")
        return

    # 5. 处理每个客户
    success_count = 0
    total_count = len(customers)
    failed_emails = []

    for customer in customers:
        try:
            # 获取邮箱
            website = customer.get('website', '')
            estimated_email = f"contact@{website}"

            logger.info(f"使用估计邮箱: {estimated_email}")

            # 检查是否已发送
            if is_email_sent(estimated_email, sent_emails):
                logger.info(f"⏭️  跳过已发送: {estimated_email}")
                continue

            # 生成邮件内容
            email_content = generate_email_content(customer, selected_keyword)

            # 发送邮件（带自动重试）
            result = send_email(
                estimated_email,
                email_content['subject'],
                email_content['body']
            )

            if result['success']:
                # 记录发送
                sent_emails.append({
                    'email': estimated_email,
                    'date': datetime.now().isoformat(),
                    'company': customer['company'],
                    'keyword': selected_keyword
                })
                success_count += 1
                logger.info(f"✅ 发送成功: {estimated_email}")
            else:
                failed_emails.append({
                    'email': estimated_email,
                    'error': result.get('error', 'Unknown error')
                })
                logger.error(f"❌ 发送失败: {estimated_email} - {result.get('error')}")

        except Exception as e:
            logger.error(f"❌ 处理客户时发生异常: {e}")
            failed_emails.append({
                'email': website,
                'error': str(e)
            })

    # 6. 保存发送记录
    if sent_emails:
        save_sent_emails(sent_emails)

    # 7. 生成报告
    generate_report(selected_keyword, success_count, total_count)

    # 8. 输出失败信息（如果有）
    if failed_emails:
        logger.warning(f"\n⚠️  失败的邮件 ({len(failed_emails)} 个):")
        for item in failed_emails:
            logger.warning(f"  - {item['email']}: {item['error']}")

    logger.info("\n" + "=" * 50)
    logger.info(f"✅ 工作流完成 - 成功: {success_count}/{total_count}")
    logger.info("=" * 50)

    return {
        'success_count': success_count,
        'total_count': total_count,
        'health_status': health_results['overall_status']
    }


if __name__ == "__main__":
    try:
        auto_run_workflow()
    except KeyboardInterrupt:
        logger.info("\n⚠️  工作流被中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ 工作流运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
