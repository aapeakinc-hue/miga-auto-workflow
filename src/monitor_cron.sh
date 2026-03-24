#!/bin/bash

# Cron 任务监控脚本
# 用于查看和管理外贸客户开发工作流的 Cron 任务

echo "🤖 外贸客户开发工作流 - Cron 任务监控"
echo "======================================"
echo ""

# 1. 检查 Cron 服务状态
echo "📋 1. Cron 服务状态:"
echo ""
if service cron status > /dev/null 2>&1; then
    echo "✅ Cron 服务运行中"
    service cron status | head -5
else
    echo "❌ Cron 服务未运行"
    echo "尝试启动..."
    service cron start
    echo "✅ Cron 服务已启动"
fi
echo ""

# 2. 查看 Cron 任务
echo "📋 2. 当前 Cron 任务:"
echo ""
crontab -l
echo ""

# 3. 查看下次运行时间
echo "📋 3. 下次运行时间:"
echo ""
echo "Cron 任务将在每天 UTC 凌晨 1 点（北京时间上午 9 点）运行"
echo "当前时间: $(date)"
echo ""
echo "距离下次运行还剩:"
python3 -c "from datetime import datetime, timedelta; now = datetime.utcnow(); next_run = now.replace(hour=1, minute=0, second=0, microsecond=0); if next_run <= now: next_run += timedelta(days=1); delta = next_run - now; print(f\"  {delta.seconds // 3600} 小时 {(delta.seconds % 3600) // 60} 分钟\")"
echo ""

# 4. 查看最近日志
echo "📋 4. 最近的 Cron 日志:"
echo ""
if [ -f logs/cron.log ]; then
    if [ -s logs/cron.log ]; then
        echo "最近 10 行日志:"
        tail -10 logs/cron.log
    else
        echo "Cron 日志文件为空（任务还未运行）"
    fi
else
    echo "Cron 日志文件不存在"
fi
echo ""

# 5. 查看发送历史
echo "📋 5. 发送历史:"
echo ""
if [ -f logs/sent_emails.json ]; then
    sent_count=$(python3 -c "import json; data=json.load(open('logs/sent_emails.json')); print(len(data))" 2>/dev/null)
    echo "已发送邮件总数: $sent_count"
    echo ""
    echo "最近 5 条发送记录:"
    python3 -c "import json; data=json.load(open('logs/sent_emails.json')); [print(f\"  {i+1}. {r['email']} ({r['company']}) - {r['date'][:10]}\") for i, r in enumerate(data[-5:])]" 2>/dev/null || echo "  无法读取发送记录"
else
    echo "发送历史文件不存在"
fi
echo ""

# 6. 查看最新报告
echo "📋 6. 最新每日报告:"
echo ""
latest_report=$(ls -t logs/daily_report_*.txt 2>/dev/null | head -1)
if [ -n "$latest_report" ]; then
    echo "最新报告: $latest_report"
    echo ""
    cat "$latest_report"
else
    echo "没有找到每日报告"
fi
echo ""

# 7. 系统信息
echo "📋 7. 系统信息:"
echo ""
echo "项目路径: $(pwd)"
echo "Python 版本: $(python3 --version)"
echo "当前时间: $(date)"
echo ""

# 8. 快速操作
echo "🔧 快速操作:"
echo ""
echo "1. 立即运行工作流:   python src/auto_workflow.py"
echo "2. 查看 Cron 日志:    tail -f logs/cron.log"
echo "3. 查看发送历史:     cat logs/sent_emails.json"
echo "4. 编辑 Cron 任务:    crontab -e"
echo "5. 测试 Cron 任务:    手动运行脚本"
echo ""

echo "======================================"
echo "✅ 监控完成！"
