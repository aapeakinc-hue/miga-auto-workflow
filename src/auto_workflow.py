"""
自动化工作流 - 每天自动运行
自动选择关键词、搜索客户、发送邮件
"""
import sys
import os
import json
import random
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.getenv('COZE_WORKSPACE_PATH', ''), 'src'))

from graphs.graph import main_graph

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

# 发送历史记录（避免重复发送同一客户）
SENT_EMAILS_FILE = "logs/sent_emails.json"

def load_sent_emails():
    """加载已发送的邮箱记录"""
    try:
        with open(SENT_EMAILS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"⚠️  加载发送记录失败: {e}")
        return []

def save_sent_emails(sent_emails):
    """保存已发送的邮箱记录"""
    try:
        os.makedirs(os.path.dirname(SENT_EMAILS_FILE), exist_ok=True)
        with open(SENT_EMAILS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sent_emails, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️  保存发送记录失败: {e}")

def is_email_sent(email, sent_emails, days=30):
    """检查邮箱是否在指定天数内已发送过"""
    if not sent_emails:
        return False

    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)

    for record in sent_emails:
        if record.get('email') == email:
            send_date = datetime.fromisoformat(record.get('date', ''))
            if send_date > cutoff_date:
                return True

    return False

def auto_run_workflow():
    """自动运行工作流"""
    print("🤖 自动化外贸客户开发工作流启动")
    print("=" * 50)

    # 加载已发送记录
    sent_emails = load_sent_emails()
    print(f"📋 已发送记录: {len(sent_emails)} 条")

    # 随机选择关键词（每天不同）
    selected_keyword = random.choice(OPTIMIZED_KEYWORDS)
    print(f"🔍 今日关键词: {selected_keyword}")

    # 运行工作流
    params = {
        "target_keywords": selected_keyword,
        "website_url": "https://miga.cc"
    }

    try:
        print("\n⏳ 正在执行工作流...")
        result = main_graph.invoke(params)

        # 统计结果
        send_results = result.get('send_results', {})
        total = send_results.get('total', 0)
        success = send_results.get('success', 0)
        failed = send_results.get('failed', 0)

        print(f"\n✅ 工作流执行完成！")
        print(f"📊 结果统计:")
        print(f"  - 总数: {total}")
        print(f"  - 成功: {success}")
        print(f"  - 失败: {failed}")

        # 处理成功的发送
        if success > 0:
            details = send_results.get('details', [])
            new_sends = []

            for detail in details:
                if detail.get('status') == 'success':
                    to_email = detail.get('to_email', '')
                    to_company = detail.get('to_company', 'N/A')

                    # 检查是否已发送过
                    if not is_email_sent(to_email, sent_emails):
                        # 添加到发送记录
                        new_send = {
                            "email": to_email,
                            "company": to_company,
                            "date": datetime.now().isoformat(),
                            "keyword": selected_keyword,
                            "message_id": detail.get('message_id', '')
                        }
                        new_sends.append(new_send)
                        sent_emails.append(new_send)

                        print(f"  ✅ 发送成功: {to_email} ({to_company})")
                    else:
                        print(f"  ⏭️  已跳过（30天内已发送）: {to_email}")

            # 保存更新后的记录
            if new_sends:
                save_sent_emails(sent_emails)
                print(f"\n💾 已保存 {len(new_sends)} 条新发送记录")

        # 生成每日报告
        generate_daily_report(result, selected_keyword, sent_emails)

        return result

    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def generate_daily_report(result, keyword, sent_emails):
    """生成每日报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 每日外贸客户开发报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 时间: {timestamp}
🔍 关键词: {keyword}

📊 发送统计:
  - 总数: {result.get('send_results', {}).get('total', 0)}
  - 成功: {result.get('send_results', {}).get('success', 0)}
  - 失败: {result.get('send_results', {}).get('failed', 0)}

📋 历史记录:
  - 累计发送: {len(sent_emails)} 封

💡 建议:
  - 定期检查邮箱回复
  - 跟进有兴趣的客户
  - 优化关键词和邮件内容

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    print(report)

    # 保存报告到文件
    try:
        os.makedirs("logs", exist_ok=True)
        report_file = f"logs/daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 报告已保存: {report_file}")
    except Exception as e:
        print(f"⚠️  保存报告失败: {e}")

if __name__ == "__main__":
    result = auto_run_workflow()
    print("\n" + "=" * 50)
    print("🎉 自动化工作流执行完成！")
