#!/bin/bash

# ===================================
# MIGA外贸客户开发系统 - 系统状态监控脚本
# ===================================
# 使用方法: bash system_status.sh

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  MIGA外贸客户开发系统 - 系统状态监控"
echo "=========================================="
echo ""

# 1. 检查系统基本信息
echo -e "${BLUE}[1] 系统基本信息${NC}"
echo "----------------------------------------"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "服务器: $(hostname)"
echo "系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "运行时间: $(uptime -p)"
echo ""

# 2. 检查Python环境
echo -e "${BLUE}[2] Python环境检查${NC}"
echo "----------------------------------------"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python已安装: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python未安装${NC}"
fi
echo ""

# 3. 检查项目目录
echo -e "${BLUE}[3] 项目目录检查${NC}"
echo "----------------------------------------"
PROJECT_DIR="/opt/miga-crm"
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${GREEN}✅ 项目目录存在: $PROJECT_DIR${NC}"
    echo "目录大小: $(du -sh $PROJECT_DIR | cut -f1)"
else
    echo -e "${RED}❌ 项目目录不存在${NC}"
fi
echo ""

# 4. 检查虚拟环境
echo -e "${BLUE}[4] Python虚拟环境检查${NC}"
echo "----------------------------------------"
VENV_DIR="$PROJECT_DIR/venv"
if [ -d "$VENV_DIR" ]; then
    echo -e "${GREEN}✅ 虚拟环境存在${NC}"
    echo "激活: source $VENV_DIR/bin/activate"
else
    echo -e "${RED}❌ 虚拟环境不存在${NC}"
fi
echo ""

# 5. 检查数据库文件
echo -e "${BLUE}[5] 数据库文件检查${NC}"
echo "----------------------------------------"
DATA_DIR="$PROJECT_DIR/data"
if [ -d "$DATA_DIR" ]; then
    DB_COUNT=$(find $DATA_DIR -name "*.db" | wc -l)
    if [ $DB_COUNT -eq 4 ]; then
        echo -e "${GREEN}✅ 数据库文件完整 ($DB_COUNT 个)${NC}"
        ls -lh $DATA_DIR/*.db
    else
        echo -e "${YELLOW}⚠️  数据库文件不完整 ($DB_COUNT 个，期望 4 个)${NC}"
    fi
else
    echo -e "${RED}❌ 数据目录不存在${NC}"
fi
echo ""

# 6. 检查定时任务
echo -e "${BLUE}[6] 定时任务检查${NC}"
echo "----------------------------------------"
if command -v crontab &> /dev/null; then
    CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "miga-crm" || echo "0")
    if [ $CRON_COUNT -gt 0 ]; then
        echo -e "${GREEN}✅ 定时任务已配置 ($CRON_COUNT 个相关任务)${NC}"
        echo ""
        echo "定时任务列表："
        crontab -l | grep "miga-crm"
    else
        echo -e "${YELLOW}⚠️  未找到定时任务${NC}"
    fi
else
    echo -e "${RED}❌ Cron服务未安装${NC}"
fi
echo ""

# 7. 检查服务状态
echo -e "${BLUE}[7] 系统服务检查${NC}"
echo "----------------------------------------"
if systemctl is-active --quiet cron; then
    echo -e "${GREEN}✅ Cron服务运行中${NC}"
else
    echo -e "${RED}❌ Cron服务未运行${NC}"
fi
echo ""

# 8. 检查最近日志
echo -e "${BLUE}[8] 最近运行日志${NC}"
echo "----------------------------------------"
LOG_DIR="$PROJECT_DIR/logs"
if [ -d "$LOG_DIR" ]; then
    echo "日志目录: $LOG_DIR"
    echo ""
    echo "日志文件列表："
    ls -lh $LOG_DIR/*.log 2>/dev/null || echo "  (暂无日志文件)"
    echo ""
    echo "最新日志（最后20行）："
    if [ -f "$LOG_DIR/daily_workflow.log" ]; then
        tail -n 20 $LOG_DIR/daily_workflow.log
    else
        echo "  (暂无日志内容)"
    fi
else
    echo -e "${YELLOW}⚠️  日志目录不存在${NC}"
fi
echo ""

# 9. 检查系统资源
echo -e "${BLUE}[9] 系统资源使用${NC}"
echo "----------------------------------------"
echo "CPU使用率: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')"
echo "内存使用:"
free -h | grep Mem
echo "磁盘使用:"
df -h $PROJECT_DIR | tail -1 | awk '{print "  使用: " $3 " / " $2 " (" $5 ")"}'
echo ""

# 10. 检查Python进程
echo -e "${BLUE}[10] Python进程检查${NC}"
echo "----------------------------------------"
PYTHON_PROCS=$(ps aux | grep python | grep -v grep | grep -c || echo "0")
if [ $PYTHON_PROCS -gt 0 ]; then
    echo -e "${GREEN}✅ 正在运行的Python进程: $PYTHON_PROCS 个${NC}"
    echo ""
    ps aux | grep python | grep -v grep
else
    echo -e "${YELLOW}⚠️  没有正在运行的Python进程${NC}"
fi
echo ""

# 11. 检查环境变量配置
echo -e "${BLUE}[11] 环境变量配置${NC}"
echo "----------------------------------------"
ENV_FILE="$PROJECT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}✅ 环境变量文件存在${NC}"
    echo ""
    echo "配置内容（敏感信息已隐藏）："
    grep -v "PASSWORD\|SECRET" $ENV_FILE | sed 's/=.*/=***/' || echo "  (无法读取配置)"
else
    echo -e "${RED}❌ 环境变量文件不存在${NC}"
fi
echo ""

# 12. 网络连接测试
echo -e "${BLUE}[12] 网络连接测试${NC}"
echo "----------------------------------------"
echo "测试SMTP连接..."
if command -v nc &> /dev/null; then
    if nc -z -w5 smtp.resend.com 587 2>/dev/null; then
        echo -e "${GREEN}✅ SMTP服务器连接正常${NC}"
    else
        echo -e "${YELLOW}⚠️  SMTP服务器连接失败${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法测试网络连接（nc命令不可用）${NC}"
fi
echo ""

# 13. 最近一次执行情况
echo -e "${BLUE}[13] 最近一次执行情况${NC}"
echo "----------------------------------------"
LOG_FILE="$PROJECT_DIR/logs/daily_workflow.log"
if [ -f "$LOG_FILE" ]; then
    LAST_RUN=$(tail -n 1 $LOG_FILE | head -n 1)
    echo "最后执行时间: $LAST_RUN"
    echo ""
    echo "最近执行结果（最后50行）："
    tail -n 50 $LOG_FILE
else
    echo -e "${YELLOW}⚠️  暂无执行记录${NC}"
fi
echo ""

# 总结
echo "=========================================="
echo "  状态检查完成"
echo "=========================================="
echo ""
echo "常用命令："
echo "  查看实时日志: tail -f $PROJECT_DIR/logs/daily_workflow.log"
echo "  手动执行: cd $PROJECT_DIR && source venv/bin/activate && python main_data_driven.py --daily"
echo "  查看定时任务: crontab -l"
echo "  编辑定时任务: crontab -e"
echo "  重新初始化: cd $PROJECT_DIR && source venv/bin/activate && python main_data_driven.py --init"
echo ""
