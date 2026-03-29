#!/usr/bin/env python3
"""
总结邮件发送系统
功能：发送总结报告到 info@miga.cc
"""
import json
from typing import Dict, List
from datetime import datetime, date
import requests

class SummarySender:
    """总结邮件发送器"""

    def __init__(self, api_key: str = "re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F"):
        self.api_key = api_key
        self.base_url = "https://api.resend.com/emails"
        self.from_email = "info@miga.cc"
        self.from_name = "MIGA 自动化系统"

    def send_daily_summary(self, report: Dict, to_email: str = None) -> Dict:
        """发送每日总结邮件"""
        if to_email is None:
            to_email = self.from_email

        subject = f"MIGA 每日总结 - {report['report_date']} - {report['market']}"
        html_content = self._format_daily_report_html(report)
        text_content = self._format_daily_report_text(report)

        return self._send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_weekly_summary(self, report: Dict, to_email: str = None) -> Dict:
        """发送周度总结邮件"""
        if to_email is None:
            to_email = self.from_email

        subject = f"MIGA 周度总结 - {report['week_start']} 至 {report['week_end']} - {report['market']}"
        html_content = self._format_weekly_report_html(report)
        text_content = self._format_weekly_report_text(report)

        return self._send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_monthly_summary(self, report: Dict, to_email: str = None) -> Dict:
        """发送月度总结邮件"""
        if to_email is None:
            to_email = self.from_email

        year_month = f"{report['year']}-{report['month']:02d}"
        subject = f"MIGA 月度总结 - {year_month} - {report['market']}"
        html_content = self._format_monthly_report_html(report)
        text_content = self._format_monthly_report_text(report)

        return self._send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_annual_summary(self, report: Dict, to_email: str = None) -> Dict:
        """发送年度总结邮件"""
        if to_email is None:
            to_email = self.from_email

        subject = f"MIGA 年度总结 - {report['year']}"
        html_content = self._format_annual_report_html(report)
        text_content = self._format_annual_report_text(report)

        return self._send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_goal_adjustment_notification(self, adjustment: Dict, to_email: str = None) -> Dict:
        """发送目标调整通知"""
        if to_email is None:
            to_email = self.from_email

        subject = f"MIGA 目标调整通知 - {adjustment.get('year', '')}-{adjustment.get('month', '')}"
        html_content = self._format_goal_adjustment_html(adjustment)
        text_content = self._format_goal_adjustment_text(adjustment)

        return self._send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def _send_email(self, to_email: str, subject: str,
                   html_content: str, text_content: str) -> Dict:
        """发送邮件"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content,
            "text": text_content
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message_id": result.get("id", ""),
                    "message": "邮件发送成功"
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _format_daily_report_html(self, report: Dict) -> str:
        """格式化每日报告为HTML"""
        metrics = report.get("metrics", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        action_items = report.get("action_items", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MIGA 每日总结</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
        .highlight {{ color: #28a745; }}
        .issue {{ color: #dc3545; }}
        .action-item {{ color: #17a2b8; }}
        .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MIGA 每日工作总结</h1>
        <p>日期: {report['report_date']} | 市场: {report['market']}</p>
    </div>

    <div class="content">
        <div class="section">
            <h2 class="section-title">📊 今日数据</h2>
            <div class="metric">
                <strong>任务总数:</strong> {metrics.get('tasks_total', 0)}
            </div>
            <div class="metric">
                <strong>完成任务:</strong> {metrics.get('tasks_completed', 0)}
            </div>
            <div class="metric">
                <strong>完成率:</strong> {metrics.get('completion_rate', 0):.1f}%
            </div>
            <div class="metric">
                <strong>发送邮件:</strong> {metrics.get('emails_sent', 0)} 封
            </div>
            <div class="metric">
                <strong>新增客户:</strong> {metrics.get('new_customers', 0)} 个
            </div>
            <div class="metric">
                <strong>互动次数:</strong> {metrics.get('interactions', 0)} 次
            </div>
        </div>
"""

        # 亮点
        if highlights:
            html += """
        <div class="section">
            <h2 class="section-title">🎯 今日亮点</h2>
            <ul>
"""
            for highlight in highlights:
                html += f"                <li class='highlight'>{highlight}</li>\n"
            html += """            </ul>
        </div>
"""

        # 问题
        if issues:
            html += """
        <div class="section">
            <h2 class="section-title">⚠️ 存在问题</h2>
            <ul>
"""
            for issue in issues:
                html += f"                <li class='issue'>{issue}</li>\n"
            html += """            </ul>
        </div>
"""

        # 行动项
        if action_items:
            html += """
        <div class="section">
            <h2 class="section-title">📋 行动计划</h2>
            <ul>
"""
            for action in action_items:
                html += f"                <li class='action-item'>{action}</li>\n"
            html += """            </ul>
        </div>
"""

        html += """
    </div>

    <div class="footer">
        <p>MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc</p>
        <p>此邮件由自动化系统生成，请勿回复</p>
    </div>
</body>
</html>
"""

        return html

    def _format_daily_report_text(self, report: Dict) -> str:
        """格式化每日报告为纯文本"""
        metrics = report.get("metrics", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        action_items = report.get("action_items", [])

        text = f"""
MIGA 每日工作总结
{'=' * 60}
日期: {report['report_date']}
市场: {report['market']}

📊 今日数据
----------
任务总数: {metrics.get('tasks_total', 0)}
完成任务: {metrics.get('tasks_completed', 0)}
完成率: {metrics.get('completion_rate', 0):.1f}%
发送邮件: {metrics.get('emails_sent', 0)} 封
新增客户: {metrics.get('new_customers', 0)} 个
互动次数: {metrics.get('interactions', 0)} 次
"""

        if highlights:
            text += "\n🎯 今日亮点\n----------\n"
            for highlight in highlights:
                text += f"{highlight}\n"

        if issues:
            text += "\n⚠️ 存在问题\n----------\n"
            for issue in issues:
                text += f"{issue}\n"

        if action_items:
            text += "\n📋 行动计划\n----------\n"
            for action in action_items:
                text += f"{action}\n"

        text += f"""
{'=' * 60}
MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc
此邮件由自动化系统生成，请勿回复
"""

        return text

    def _format_weekly_report_html(self, report: Dict) -> str:
        """格式化周度报告为HTML"""
        weekly_metrics = report.get("weekly_metrics", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MIGA 周度总结</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
        .highlight {{ color: #28a745; }}
        .issue {{ color: #dc3545; }}
        .recommendation {{ color: #17a2b8; }}
        .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MIGA 周度工作总结</h1>
        <p>周期: {report['week_start']} 至 {report['week_end']} | 市场: {report['market']}</p>
    </div>

    <div class="content">
        <div class="section">
            <h2 class="section-title">📊 本周数据</h2>
            <div class="metric">
                <strong>总任务数:</strong> {weekly_metrics.get('total_tasks', 0)}
            </div>
            <div class="metric">
                <strong>完成任务:</strong> {weekly_metrics.get('completed_tasks', 0)}
            </div>
            <div class="metric">
                <strong>平均完成率:</strong> {weekly_metrics.get('avg_completion_rate', 0):.1f}%
            </div>
            <div class="metric">
                <strong>发送邮件:</strong> {weekly_metrics.get('total_emails_sent', 0)} 封
            </div>
            <div class="metric">
                <strong>新增客户:</strong> {weekly_metrics.get('total_new_customers', 0)} 个
            </div>
            <div class="metric">
                <strong>互动次数:</strong> {weekly_metrics.get('total_interactions', 0)} 次
            </div>
        </div>
"""

        # 亮点
        if highlights:
            html += """
        <div class="section">
            <h2 class="section-title">🎯 本周亮点</h2>
            <ul>
"""
            for highlight in highlights:
                html += f"                <li class='highlight'>{highlight}</li>\n"
            html += """            </ul>
        </div>
"""

        # 问题
        if issues:
            html += """
        <div class="section">
            <h2 class="section-title">⚠️ 存在问题</h2>
            <ul>
"""
            for issue in issues:
                html += f"                <li class='issue'>{issue}</li>\n"
            html += """            </ul>
        </div>
"""

        # 建议
        if recommendations:
            html += """
        <div class="section">
            <h2 class="section-title">💡 改进建议</h2>
            <ul>
"""
            for rec in recommendations:
                html += f"                <li class='recommendation'>{rec}</li>\n"
            html += """            </ul>
        </div>
"""

        html += """
    </div>

    <div class="footer">
        <p>MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc</p>
        <p>此邮件由自动化系统生成，请勿回复</p>
    </div>
</body>
</html>
"""

        return html

    def _format_weekly_report_text(self, report: Dict) -> str:
        """格式化周度报告为纯文本"""
        weekly_metrics = report.get("weekly_metrics", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        text = f"""
MIGA 周度工作总结
{'=' * 60}
周期: {report['week_start']} 至 {report['week_end']}
市场: {report['market']}

📊 本周数据
----------
总任务数: {weekly_metrics.get('total_tasks', 0)}
完成任务: {weekly_metrics.get('completed_tasks', 0)}
平均完成率: {weekly_metrics.get('avg_completion_rate', 0):.1f}%
发送邮件: {weekly_metrics.get('total_emails_sent', 0)} 封
新增客户: {weekly_metrics.get('total_new_customers', 0)} 个
互动次数: {weekly_metrics.get('total_interactions', 0)} 次
"""

        if highlights:
            text += "\n🎯 本周亮点\n----------\n"
            for highlight in highlights:
                text += f"{highlight}\n"

        if issues:
            text += "\n⚠️ 存在问题\n----------\n"
            for issue in issues:
                text += f"{issue}\n"

        if recommendations:
            text += "\n💡 改进建议\n----------\n"
            for rec in recommendations:
                text += f"{rec}\n"

        text += f"""
{'=' * 60}
MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc
此邮件由自动化系统生成，请勿回复
"""

        return text

    def _format_monthly_report_html(self, report: Dict) -> str:
        """格式化月度报告为HTML"""
        monthly_metrics = report.get("monthly_metrics", {})
        goal_achievement = report.get("goal_achievement", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MIGA 月度总结</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
        .achievement {{ color: #28a745; }}
        .issue {{ color: #dc3545; }}
        .recommendation {{ color: #17a2b8; }}
        .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MIGA 月度工作总结</h1>
        <p>时间: {report['year']}-{report['month']:02d} | 市场: {report['market']}</p>
    </div>

    <div class="content">
        <div class="section">
            <h2 class="section-title">📊 本月数据</h2>
            <div class="metric">
                <strong>总任务数:</strong> {monthly_metrics.get('total_tasks', 0)}
            </div>
            <div class="metric">
                <strong>完成任务:</strong> {monthly_metrics.get('completed_tasks', 0)}
            </div>
            <div class="metric">
                <strong>平均完成率:</strong> {monthly_metrics.get('avg_completion_rate', 0):.1f}%
            </div>
            <div class="metric">
                <strong>发送邮件:</strong> {monthly_metrics.get('total_emails_sent', 0)} 封
            </div>
            <div class="metric">
                <strong>新增客户:</strong> {monthly_metrics.get('total_new_customers', 0)} 个
            </div>
            <div class="metric">
                <strong>互动次数:</strong> {monthly_metrics.get('total_interactions', 0)} 次
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">🎯 目标达成情况</h2>
"""

        # 目标达成情况
        for metric, rate in goal_achievement.items():
            if isinstance(rate, (int, float)):
                html += f"""
            <div class="achievement">
                <strong>{metric}:</strong> {rate:.1f}%
            </div>
"""

        html += """
        </div>
"""

        # 亮点
        if highlights:
            html += """
        <div class="section">
            <h2 class="section-title">🎯 本月亮点</h2>
            <ul>
"""
            for highlight in highlights:
                html += f"                <li class='highlight'>{highlight}</li>\n"
            html += """            </ul>
        </div>
"""

        # 问题
        if issues:
            html += """
        <div class="section">
            <h2 class="section-title">⚠️ 存在问题</h2>
            <ul>
"""
            for issue in issues:
                html += f"                <li class='issue'>{issue}</li>\n"
            html += """            </ul>
        </div>
"""

        # 建议
        if recommendations:
            html += """
        <div class="section">
            <h2 class="section-title">💡 改进建议</h2>
            <ul>
"""
            for rec in recommendations:
                html += f"                <li class='recommendation'>{rec}</li>\n"
            html += """            </ul>
        </div>
"""

        html += """
    </div>

    <div class="footer">
        <p>MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc</p>
        <p>此邮件由自动化系统生成，请勿回复</p>
    </div>
</body>
</html>
"""

        return html

    def _format_monthly_report_text(self, report: Dict) -> str:
        """格式化月度报告为纯文本"""
        monthly_metrics = report.get("monthly_metrics", {})
        goal_achievement = report.get("goal_achievement", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        text = f"""
MIGA 月度工作总结
{'=' * 60}
时间: {report['year']}-{report['month']:02d}
市场: {report['market']}

📊 本月数据
----------
总任务数: {monthly_metrics.get('total_tasks', 0)}
完成任务: {monthly_metrics.get('completed_tasks', 0)}
平均完成率: {monthly_metrics.get('avg_completion_rate', 0):.1f}%
发送邮件: {monthly_metrics.get('total_emails_sent', 0)} 封
新增客户: {monthly_metrics.get('total_new_customers', 0)} 个
互动次数: {monthly_metrics.get('total_interactions', 0)} 次

🎯 目标达成情况
----------
"""

        for metric, rate in goal_achievement.items():
            if isinstance(rate, (int, float)):
                text += f"{metric}: {rate:.1f}%\n"

        if highlights:
            text += "\n🎯 本月亮点\n----------\n"
            for highlight in highlights:
                text += f"{highlight}\n"

        if issues:
            text += "\n⚠️ 存在问题\n----------\n"
            for issue in issues:
                text += f"{issue}\n"

        if recommendations:
            text += "\n💡 改进建议\n----------\n"
            for rec in recommendations:
                text += f"{rec}\n"

        text += f"""
{'=' * 60}
MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc
此邮件由自动化系统生成，请勿回复
"""

        return text

    def _format_annual_report_html(self, report: Dict) -> str:
        """格式化年度报告为HTML"""
        annual_achievement = report.get("annual_achievement", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MIGA 年度总结</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .achievement {{ color: #28a745; }}
        .issue {{ color: #dc3545; }}
        .recommendation {{ color: #17a2b8; }}
        .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MIGA 年度工作总结</h1>
        <p>年份: {report['year']}</p>
    </div>

    <div class="content">
        <div class="section">
            <h2 class="section-title">📊 年度目标达成情况</h2>
"""

        # 各市场目标达成情况
        for market, achievement in annual_achievement.items():
            html += f"""
            <div class="achievement">
                <strong>{market} 市场:</strong>
                <ul>
"""
            for metric, rate in achievement.items():
                if isinstance(rate, (int, float)):
                    html += f"                    <li>{metric}: {rate:.1f}%</li>\n"
            html += """
                </ul>
            </div>
"""

        html += """
        </div>
"""

        # 亮点
        if highlights:
            html += """
        <div class="section">
            <h2 class="section-title">🎯 年度亮点</h2>
            <ul>
"""
            for highlight in highlights:
                html += f"                <li class='highlight'>{highlight}</li>\n"
            html += """            </ul>
        </div>
"""

        # 问题
        if issues:
            html += """
        <div class="section">
            <h2 class="section-title">⚠️ 存在问题</h2>
            <ul>
"""
            for issue in issues:
                html += f"                <li class='issue'>{issue}</li>\n"
            html += """            </ul>
        </div>
"""

        # 建议
        if recommendations:
            html += """
        <div class="section">
            <h2 class="section-title">💡 改进建议</h2>
            <ul>
"""
            for rec in recommendations:
                html += f"                <li class='recommendation'>{rec}</li>\n"
            html += """            </ul>
        </div>
"""

        html += """
    </div>

    <div class="footer">
        <p>MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc</p>
        <p>此邮件由自动化系统生成，请勿回复</p>
    </div>
</body>
</html>
"""

        return html

    def _format_annual_report_text(self, report: Dict) -> str:
        """格式化年度报告为纯文本"""
        annual_achievement = report.get("annual_achievement", {})
        highlights = report.get("highlights", [])
        issues = report.get("issues", [])
        recommendations = report.get("recommendations", [])

        text = f"""
MIGA 年度工作总结
{'=' * 60}
年份: {report['year']}

📊 年度目标达成情况
----------
"""

        for market, achievement in annual_achievement.items():
            text += f"{market} 市场:\n"
            for metric, rate in achievement.items():
                if isinstance(rate, (int, float)):
                    text += f"  {metric}: {rate:.1f}%\n"
            text += "\n"

        if highlights:
            text += "🎯 年度亮点\n----------\n"
            for highlight in highlights:
                text += f"{highlight}\n"

        if issues:
            text += "\n⚠️ 存在问题\n----------\n"
            for issue in issues:
                text += f"{issue}\n"

        if recommendations:
            text += "\n💡 改进建议\n----------\n"
            for rec in recommendations:
                text += f"{rec}\n"

        text += f"""
{'=' * 60}
MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc
此邮件由自动化系统生成，请勿回复
"""

        return text

    def _format_goal_adjustment_html(self, adjustment: Dict) -> str:
        """格式化目标调整通知为HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>目标调整通知</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>目标调整通知</h1>
        <p>时间: {adjustment.get('year', '')}-{adjustment.get('month', '')} | 市场: {adjustment.get('market', '')}</p>
    </div>

    <div class="content">
        <div class="section">
            <h2 class="section-title">📊 目标达成情况</h2>
"""

        # 达成情况
        achievements = adjustment.get("achievements", {})
        for metric, data in achievements.items():
            if "achievement_rate" in data:
                html += f"""
            <div>
                <strong>{metric}:</strong>
                目标: {data.get('target', 0)}
                实际: {data.get('actual', 0)}
                达成率: {data.get('achievement_rate', 0):.1f}%
            </div>
"""

        html += """
        </div>

        <div class="section">
            <h2 class="section-title">🔄 调整建议</h2>
"""

        # 调整建议
        adjustments = adjustment.get("adjustments", {})
        for metric, data in adjustments.items():
            if "adjustment_factor" in data:
                factor = data["adjustment_factor"]
                if factor > 1:
                    html += f"""
            <div style="color: #28a745;">
                <strong>{metric}:</strong> 提高 {((factor - 1) * 100):.0f}% - {data.get('adjustment_reason', '')}
            </div>
"""
                elif factor < 1:
                    html += f"""
            <div style="color: #dc3545;">
                <strong>{metric}:</strong> 降低 {((1 - factor) * 100):.0f}% - {data.get('adjustment_reason', '')}
            </div>
"""
                else:
                    html += f"""
            <div style="color: #6c757d;">
                <strong>{metric}:</strong> 保持不变 - {data.get('adjustment_reason', '')}
            </div>
"""

        html += """
        </div>

        <div class="section">
            <h2 class="section-title">💡 综合建议</h2>
            <p>""" + adjustment.get("recommendation", "") + """</p>
        </div>
    </div>

    <div class="footer">
        <p>MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc</p>
        <p>此邮件由自动化系统生成，请勿回复</p>
    </div>
</body>
</html>
"""

        return html

    def _format_goal_adjustment_text(self, adjustment: Dict) -> str:
        """格式化目标调整通知为纯文本"""
        text = f"""
目标调整通知
{'=' * 60}
时间: {adjustment.get('year', '')}-{adjustment.get('month', '')}
市场: {adjustment.get('market', '')}

📊 目标达成情况
----------
"""

        achievements = adjustment.get("achievements", {})
        for metric, data in achievements.items():
            if "achievement_rate" in data:
                text += f"{metric}:\n"
                text += f"  目标: {data.get('target', 0)}\n"
                text += f"  实际: {data.get('actual', 0)}\n"
                text += f"  达成率: {data.get('achievement_rate', 0):.1f}%\n\n"

        text += "🔄 调整建议\n----------\n"

        adjustments = adjustment.get("adjustments", {})
        for metric, data in adjustments.items():
            if "adjustment_factor" in data:
                factor = data["adjustment_factor"]
                if factor > 1:
                    text += f"{metric}: 提高 {((factor - 1) * 100):.0f}% - {data.get('adjustment_reason', '')}\n"
                elif factor < 1:
                    text += f"{metric}: 降低 {((1 - factor) * 100):.0f}% - {data.get('adjustment_reason', '')}\n"
                else:
                    text += f"{metric}: 保持不变 - {data.get('adjustment_reason', '')}\n"

        text += f"""
💡 综合建议
----------
{adjustment.get("recommendation", "")}

{'=' * 60}
MIGA Team | 网址: https://miga.cc | 邮箱: info@miga.cc
此邮件由自动化系统生成，请勿回复
"""

        return text

if __name__ == "__main__":
    # 测试邮件发送
    from datetime import date

    sender = SummarySender()

    # 创建示例报告
    sample_report = {
        "report_type": "daily",
        "report_date": date.today().isoformat(),
        "market": "USA",
        "metrics": {
            "tasks_total": 5,
            "tasks_completed": 4,
            "completion_rate": 80.0,
            "emails_sent": 19,
            "new_customers": 25,
            "interactions": 30
        },
        "highlights": [
            "✓ 今日发送邮件 19 封，达到目标",
            "✓ 新增客户 25 个，表现优秀"
        ],
        "issues": [
            "⚠️ 任务完成率 80.0%，还有提升空间"
        ],
        "action_items": [
            "明日计划发送25封邮件以弥补今日不足"
        ]
    }

    # 发送测试邮件
    result = sender.send_daily_summary(sample_report)
    print("邮件发送结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
