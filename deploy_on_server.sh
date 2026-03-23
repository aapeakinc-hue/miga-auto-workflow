#!/bin/bash

# ===================================
# MIGA外贸客户开发系统 - 一键部署脚本
# ===================================
# 使用方法: sudo bash deploy_on_server.sh

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  MIGA外贸客户开发系统 - 开始部署"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 1. 更新系统并安装依赖
echo -e "${YELLOW}[1/8] 正在更新系统并安装依赖...${NC}"
apt update && apt install -y git python3 python3-pip python3-venv cron curl
echo -e "${GREEN}✅ 系统依赖安装完成${NC}"
echo ""

# 2. 创建项目目录
echo -e "${YELLOW}[2/8] 正在创建项目目录...${NC}"
mkdir -p /opt/miga-crm
cd /opt/miga-crm
echo -e "${GREEN}✅ 项目目录创建完成: /opt/miga-crm${NC}"
echo ""

# 3. 创建Python虚拟环境
echo -e "${YELLOW}[3/8] 正在创建Python虚拟环境...${NC}"
python3 -m venv venv
echo -e "${GREEN}✅ 虚拟环境创建完成${NC}"
echo ""

# 4. 激活虚拟环境并安装Python依赖
echo -e "${YELLOW}[4/8] 正在安装Python依赖包...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install langgraph langchain langchain-core requests python-dotenv
echo -e "${GREEN}✅ Python依赖安装完成${NC}"
echo ""

# 5. 创建必要的目录结构
echo -e "${YELLOW}[5/8] 正在创建目录结构...${NC}"
mkdir -p /opt/miga-crm/logs
mkdir -p /opt/miga-crm/data
mkdir -p /opt/miga-crm/reports
mkdir -p /opt/miga-crm/assets/mock
mkdir -p /opt/miga-crm/backups
echo -e "${GREEN}✅ 目录结构创建完成${NC}"
echo ""

# 6. 创建环境变量模板
echo -e "${YELLOW}[6/8] 正在创建环境变量配置文件...${NC}"
cat > /opt/miga-crm/.env << 'EOF'
# MIGA外贸客户开发系统 - 环境变量配置
# 请根据实际情况修改以下配置

# ===================================
# 数据库路径配置
# ===================================
DB_DIR=/opt/miga-crm/data

# ===================================
# 邮箱配置（SMTP）
# ===================================
SMTP_SERVER=smtp.resend.com
SMTP_PORT=587
SMTP_USERNAME=resend
SMTP_PASSWORD=请填写你的API_Key
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=info@miga.cc

# ===================================
# 工作流配置
# ===================================
# 年度目标（美元）
DEFAULT_YEARLY_GOAL=1000000
# 市场规模（美元）
DEFAULT_MARKET_SIZE=50000000

# ===================================
# 调试配置（生产环境建议设为false）
# ===================================
DEBUG=false
EOF
echo -e "${GREEN}✅ 环境变量配置文件已创建: /opt/miga-crm/.env${NC}"
echo -e "${YELLOW}⚠️  请编辑此文件，填写正确的SMTP配置${NC}"
echo ""

# 7. 创建数据库备份脚本
echo -e "${YELLOW}[7/8] 正在创建数据库备份脚本...${NC}"
cat > /opt/miga-crm/backup.sh << 'EOF'
#!/bin/bash

# 数据库备份脚本
# 执行: bash /opt/miga-crm/backup.sh

BACKUP_DIR="/opt/miga-crm/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mkdir -p $BACKUP_DIR/backup_$DATE
cp /opt/miga-crm/data/*.db $BACKUP_DIR/backup_$DATE/

# 压缩备份
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C /opt/miga-crm data logs reports

# 删除30天前的备份
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "$(date '+%Y-%m-%d %H:%M:%S') 备份完成: backup_$DATE.tar.gz" >> /opt/miga-crm/logs/backup.log
EOF

chmod +x /opt/miga-crm/backup.sh
echo -e "${GREEN}✅ 备份脚本创建完成${NC}"
echo ""

# 8. 创建定时任务模板
echo -e "${YELLOW}[8/8] 正在创建定时任务模板...${NC}"
cat > /opt/miga-crm/crontab_template.txt << 'EOF'
# MIGA外贸客户开发系统 - 定时任务配置
# 将此内容添加到 crontab 中

# 每天早上8:00执行每日工作流
0 8 * * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily >> logs/daily_workflow.log 2>&1

# 每月1号凌晨1:00调整目标
0 1 1 * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --adjust_goals >> logs/monthly_adjustment.log 2>&1

# 每周日凌晨2:00生成周报
0 2 * * 0 cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --weekly >> logs/weekly_report.log 2>&1

# 每天凌晨4:00备份数据
0 4 * * * /opt/miga-crm/backup.sh >> logs/backup.log 2>&1

# 每天凌晨3:00清理7天前的日志
0 3 * * * find /opt/miga-crm/logs -name "*.log" -mtime +7 -delete
EOF
echo -e "${GREEN}✅ 定时任务模板创建完成: /opt/miga-crm/crontab_template.txt${NC}"
echo ""

# 部署完成
echo "=========================================="
echo -e "${GREEN}  🎉 环境准备完成！${NC}"
echo "=========================================="
echo ""
echo "接下来的步骤："
echo ""
echo "1. 上传项目代码到 /opt/miga-crm/"
echo "   - 使用: scp -r 项目文件 root@服务器IP:/opt/miga-crm/"
echo ""
echo "2. 编辑配置文件"
echo "   - 命令: nano /opt/miga-crm/.env"
echo "   - 修改SMTP配置和目标设置"
echo ""
echo "3. 初始化系统"
echo "   - 命令: cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --init"
echo ""
echo "4. 配置定时任务"
echo "   - 命令: crontab -e"
echo "   - 复制 /opt/miga-crm/crontab_template.txt 中的内容"
echo ""
echo "5. 测试运行"
echo "   - 命令: cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily"
echo ""
echo "=========================================="
echo "  部署文档: CLOUD_DEPLOYMENT_GUIDE.md"
echo "=========================================="
