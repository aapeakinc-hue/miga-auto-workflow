#!/bin/bash
# MIGA 数据驱动外贸客户开发系统 - 部署检查脚本

echo "================================================================================"
echo "MIGA 数据驱动系统 - 部署检查"
echo "================================================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查结果统计
PASS=0
FAIL=0
WARN=0

# 检查1: Python版本
echo "检查1: Python版本"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Python版本: $PYTHON_VERSION (要求: 3.8+)"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC} - Python版本: $PYTHON_VERSION (要求: 3.8+)"
    ((FAIL++))
fi
echo ""

# 检查2: 依赖包
echo "检查2: 依赖包"

check_package() {
    PACKAGE=$1
    if pip show $PACKAGE > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC} - $PACKAGE 已安装"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC} - $PACKAGE 未安装"
        ((FAIL++))
    fi
}

check_package "langgraph"
check_package "langchain"
check_package "requests"
check_package "pydantic"
check_package "jinja2"
echo ""

# 检查3: 数据库文件
echo "检查3: 数据库文件"

check_database() {
    DB_FILE=$1
    if [ -f "$DB_FILE" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $DB_FILE 存在"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠️  WARN${NC} - $DB_FILE 不存在（将在首次运行时创建）"
        ((WARN++))
    fi
}

check_database "market_data.db"
check_database "goals.db"
check_database "daily_planner.db"
check_database "miga_crm.db"
echo ""

# 检查4: 核心模块文件
echo "检查4: 核心模块文件"

check_module() {
    MODULE=$1
    if [ -f "$MODULE" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $MODULE 存在"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC} - $MODULE 不存在"
        ((FAIL++))
    fi
}

check_module "market_research.py"
check_module "goal_setting.py"
check_module "daily_planner.py"
check_module "report_generator.py"
check_module "summary_sender.py"
check_module "goal_adjuster.py"
check_module "workflow_orchestrator.py"
check_module "main_data_driven.py"
echo ""

# 检查5: 工作流文件
echo "检查5: 工作流文件"

check_workflow() {
    WORKFLOW=$1
    if [ -f "$WORKFLOW" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $WORKFLOW 存在"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠️  WARN${NC} - $WORKFLOW 不存在"
        ((WARN++))
    fi
}

check_workflow "src/graphs/graph.py"
check_workflow "src/graphs/state.py"
echo ""

# 检查6: 日志目录
echo "检查6: 日志目录"

if [ -d "/app/work/logs/bypass" ]; then
    echo -e "${GREEN}✅ PASS${NC} - 日志目录存在: /app/work/logs/bypass"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} - 日志目录不存在（将在首次运行时创建）"
    ((WARN++))
fi
echo ""

# 检查7: API配置
echo "检查7: API配置"

if grep -q "re_cB3gsHB9_2rJhdZsAoFdCA6i12zynFm6F" summary_sender.py 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - Resend API Key 已配置"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} - Resend API Key 可能未配置"
    ((WARN++))
fi

if grep -q "info@miga.cc" summary_sender.py 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - 发件邮箱已配置: info@miga.cc"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC} - 发件邮箱未配置"
    ((FAIL++))
fi
echo ""

# 检查8: 系统初始化状态
echo "检查8: 系统初始化状态"

INIT_RESULT=$(python main_data_driven.py --status 2>&1 | grep "数据库状态" -A 10)

if echo "$INIT_RESULT" | grep -q "✅"; then
    echo -e "${GREEN}✅ PASS${NC} - 系统已初始化"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} - 系统可能未初始化（请运行: python main_data_driven.py --init）"
    ((WARN++))
fi
echo ""

# 检查9: 测试邮件发送（可选）
echo "检查9: 测试邮件发送（可选）"
read -p "是否发送测试邮件到 info@miga.cc? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    TEST_RESULT=$(python -c "
from summary_sender import SummarySender
sender = SummarySender()
test_report = {
    'report_type': 'test',
    'report_date': '2026-03-22',
    'market': 'USA',
    'metrics': {'test': 1},
    'highlights': ['测试邮件'],
    'issues': [],
    'action_items': []
}
result = sender.send_daily_summary(test_report)
print(result.get('success', False))
" 2>&1)

    if [ "$TEST_RESULT" = "True" ]; then
        echo -e "${GREEN}✅ PASS${NC} - 测试邮件发送成功"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC} - 测试邮件发送失败"
        ((FAIL++))
    fi
else
    echo -e "${YELLOW}⚠️  SKIP${NC} - 跳过邮件发送测试"
    ((WARN++))
fi
echo ""

# 检查10: 磁盘空间
echo "检查10: 磁盘空间"

DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✅ PASS${NC} - 磁盘空间充足 (已使用: ${DISK_USAGE}%)"
    ((PASS++))
elif [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠️  WARN${NC} - 磁盘空间紧张 (已使用: ${DISK_USAGE}%)"
    ((WARN++))
else
    echo -e "${RED}❌ FAIL${NC} - 磁盘空间不足 (已使用: ${DISK_USAGE}%)"
    ((FAIL++))
fi
echo ""

# 检查总结
echo "================================================================================"
echo "检查总结"
echo "================================================================================"
echo ""
echo -e "${GREEN}通过: $PASS${NC}"
echo -e "${RED}失败: $FAIL${NC}"
echo -e "${YELLOW}警告: $WARN${NC}"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✅ 所有关键检查通过！系统已准备好部署。${NC}"
    echo ""
    echo "下一步操作："
    echo "1. 设置定时任务: 参考 DEPLOYMENT_CRON_CONFIG.md"
    echo "2. 运行首次测试: python main_data_driven.py --daily"
    echo "3. 检查邮箱 info@miga.cc 接收报告"
else
    echo -e "${RED}❌ 有 $FAIL 项检查失败，请修复后再部署。${NC}"
    exit 1
fi

echo ""
echo "================================================================================"
