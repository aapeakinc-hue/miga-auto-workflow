# ☁️ 外贸客户开发系统 - 云端部署完整指南

## 📋 部署概述

本指南将帮助您将外贸客户开发系统部署到云端服务器，实现7x24小时全自动运行。

### 🎯 部署后效果
- ✅ 每日自动执行市场研究、目标管理、客户开发流程
- ✅ 自动生成并发送每日报告到您的邮箱
- ✅ 基于数据自动调整月度目标
- ✅ 无需人工干预，系统全自动运行

---

## 📦 前置要求

### 1. 云服务器要求
- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **配置建议**:
  - CPU: 2核及以上
  - 内存: 4GB及以上
  - 硬盘: 40GB及以上
  - 网络: 1Mbps及以上
- **推荐云服务商**: 腾讯云、阿里云、华为云、AWS、DigitalOcean等

### 2. 域名（可选但推荐）
- 用于访问邮件日志和监控页面（如果需要Web界面）

### 3. 邮箱服务
- 需要配置SMTP邮箱用于发送报告
- 推荐使用企业邮箱或Gmail

---

## 🚀 快速部署（3步完成）

### 步骤 1：购买并连接云服务器

#### 1.1 购买服务器
- 登录云服务商控制台
- 选择适合的配置（推荐：2核4GB）
- 选择操作系统：Ubuntu 22.04 LTS（推荐）
- 设置安全组/防火墙：
  - 开放SSH端口（22）
  - 如需Web访问，开放80/443

#### 1.2 连接服务器

**Windows用户**:
```bash
# 使用PowerShell或CMD
ssh root@你的服务器公网IP
# 输入密码后登录
```

**Mac/Linux用户**:
```bash
ssh root@你的服务器公网IP
```

---

### 步骤 2：执行一键部署脚本

**登录服务器后，执行以下命令**：

```bash
# 1. 安装必要依赖
sudo apt update && sudo apt install -y git python3 python3-pip python3-venv cron

# 2. 创建项目目录
mkdir -p /opt/miga-crm
cd /opt/miga-crm

# 3. 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate

# 4. 安装项目依赖
pip install --upgrade pip
pip install langgraph langchain langchain-core requests python-dotenv

# 5. 创建必要目录
mkdir -p logs data reports
```

---

### 步骤 3：上传项目代码

**方法A：使用Git（推荐）**

如果你已经把项目推送到Git仓库：

```bash
# 克隆项目
git clone https://github.com/你的用户名/miga-crm.git .

# 或者如果项目在其他位置，先复制代码到服务器
```

**方法B：使用SCP上传（本地有项目文件）**

**在本地电脑（Windows PowerShell）执行**：

```powershell
# 压缩项目文件
# 在本地项目目录下，右键 → 发送到 → 压缩(zipped)文件夹

# 上传到服务器
scp miga-crm.zip root@你的服务器IP:/opt/miga-crm/
```

**然后在服务器上解压**：

```bash
# 登录服务器后
cd /opt/miga-crm
unzip miga-crm.zip
```

**方法C：直接在服务器上创建文件**

如果项目文件较少，可以直接复制粘贴代码文件。

---

## ⚙️ 配置系统

### 1. 配置环境变量

创建配置文件：

```bash
nano /opt/miga-crm/.env
```

**粘贴以下内容**（根据实际情况修改）：

```env
# 数据库路径
DB_DIR=/opt/miga-crm/data

# 邮箱配置（示例使用Resend）
SMTP_SERVER=smtp.resend.com
SMTP_PORT=587
SMTP_USERNAME=resend
SMTP_PASSWORD=你的Resend_API_Key
FROM_EMAIL=noreply@你的域名.com
TO_EMAIL=info@miga.cc

# 工作流配置
DEFAULT_YEARLY_GOAL=1000000
DEFAULT_MARKET_SIZE=50000000
```

**保存退出**：`Ctrl + O` → `Enter` → `Ctrl + X`

---

### 2. 创建必要的数据目录

```bash
cd /opt/miga-crm
mkdir -p logs data reports assets/mock
```

---

### 3. 初始化系统

```bash
# 激活虚拟环境
source /opt/miga-crm/venv/bin/activate

# 运行系统初始化
cd /opt/miga-crm
python main_data_driven.py --init
```

**预期输出**：
```
✅ 市场数据库创建成功
✅ 目标数据库创建成功
✅ 每日计划数据库创建成功
✅ CRM数据库创建成功
✅ 系统初始化完成
```

---

## ⏰ 配置定时任务（Cron）

### 1. 编辑crontab

```bash
crontab -e
```

**首次使用会提示选择编辑器，选择 `nano`（通常选1或2）**

---

### 2. 添加定时任务

**在文件末尾粘贴以下内容**：

```bash
# MIGA外贸客户开发系统定时任务配置

# 每天早上8:00执行每日工作流
0 8 * * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily >> logs/daily_workflow.log 2>&1

# 每月1号凌晨1:00调整目标
0 1 1 * * cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --adjust_goals >> logs/monthly_adjustment.log 2>&1

# 每周日凌晨2:00生成周报
0 2 * * 0 cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --weekly >> logs/weekly_report.log 2>&1

# 每天凌晨3:00清理7天前的日志
0 3 * * * find /opt/miga-crm/logs -name "*.log" -mtime +7 -delete
```

**保存退出**：`Ctrl + O` → `Enter` → `Ctrl + X`

---

### 3. 验证定时任务

```bash
# 查看已配置的定时任务
crontab -l
```

**应该看到刚才添加的任务列表**。

---

## 🧪 测试部署

### 测试1：手动执行每日工作流

```bash
cd /opt/miga-crm
source venv/bin/activate
python main_data_driven.py --daily
```

**检查**：
- 是否成功发送邮件到 info@miga.cc
- 查看日志：`tail -f logs/daily_workflow.log`

---

### 测试2：检查数据库

```bash
# 查看数据库文件
ls -lh /opt/miga-crm/data/

# 应该看到4个.db文件
# market_data.db, goals.db, daily_planner.db, miga_crm.db
```

---

## 📊 监控与维护

### 1. 查看运行日志

```bash
# 查看今日日志
tail -n 100 /opt/miga-crm/logs/daily_workflow.log

# 实时监控日志
tail -f /opt/miga-crm/logs/daily_workflow.log

# 查看所有日志文件
ls -lh /opt/miga-crm/logs/
```

---

### 2. 常用监控命令

```bash
# 检查定时任务状态
service cron status

# 查看最近的定时任务执行记录
sudo grep CRON /var/log/syslog | tail -20

# 检查Python进程
ps aux | grep python

# 查看系统资源使用
htop
# 如果没有htop，安装：sudo apt install htop
```

---

### 3. 数据备份（建议）

**创建备份脚本**：

```bash
nano /opt/miga-crm/backup.sh
```

**粘贴以下内容**：

```bash
#!/bin/bash

# 备份目录
BACKUP_DIR="/opt/miga-crm/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp /opt/miga-crm/data/*.db $BACKUP_DIR/backup_$DATE/

# 压缩
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C /opt/miga-crm data logs reports

# 删除30天前的备份
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "备份完成: backup_$DATE.tar.gz"
```

**保存退出**，然后执行：

```bash
# 给脚本执行权限
chmod +x /opt/miga-crm/backup.sh

# 添加到定时任务（每天凌晨4:00备份）
crontab -e
```

**添加**：
```bash
0 4 * * * /opt/miga-crm/backup.sh >> /opt/miga-crm/logs/backup.log 2>&1
```

---

## 🔧 故障排查

### 问题1：定时任务没有执行

**排查步骤**：

```bash
# 1. 检查cron服务状态
service cron status
# 如果未运行：sudo service cron start

# 2. 查看系统日志
sudo grep CRON /var/log/syslog | tail -20

# 3. 检查脚本权限
ls -l /opt/miga-crm/main_data_driven.py
# 应该有执行权限，否则：chmod +x /opt/miga-crm/main_data_driven.py

# 4. 手动测试命令
cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily
```

---

### 问题2：邮件发送失败

**排查步骤**：

```bash
# 1. 检查环境变量配置
cat /opt/miga-crm/.env

# 2. 查看错误日志
tail -n 50 /opt/miga-crm/logs/daily_workflow.log

# 3. 测试SMTP连接
python3 << EOF
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test email from server")
msg['Subject'] = "Test Email"
msg['From'] = "noreply@yourdomain.com"
msg['To'] = "info@miga.cc"

try:
    with smtplib.SMTP('smtp.resend.com', 587) as server:
        server.starttls()
        server.login('resend', 'your-api-key')
        server.send_message(msg)
    print("✅ Email sent successfully")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

---

### 问题3：Python依赖缺失

**排查步骤**：

```bash
# 1. 激活虚拟环境
source /opt/miga-crm/venv/bin/activate

# 2. 查看已安装的包
pip list

# 3. 重新安装依赖
pip install --upgrade langgraph langchain langchain-core requests python-dotenv
```

---

### 问题4：数据库文件损坏

**解决方案**：

```bash
# 1. 停止定时任务
crontab -e
# 注释掉所有任务，保存

# 2. 备份当前数据库
cp /opt/miga-crm/data/*.db /opt/miga-crm/backup/

# 3. 重新初始化
cd /opt/miga-crm
source venv/bin/activate
python main_data_driven.py --init

# 4. 如果需要恢复旧数据
cp /opt/miga-crm/backup/*.db /opt/miga-crm/data/

# 5. 恢复定时任务
crontab -e
# 取消注释
```

---

## 📈 性能优化

### 1. 使用Supervisor管理进程（可选）

如果需要更可靠的进程管理，可以安装Supervisor：

```bash
# 安装
sudo apt install -y supervisor

# 创建配置文件
sudo nano /etc/supervisor/conf.d/miga-crm.conf
```

**配置内容**：

```ini
[program:miga-crm-daily]
command=/opt/miga-crm/venv/bin/python /opt/miga-crm/main_data_driven.py --daily
directory=/opt/miga-crm
user=root
autostart=false
autorestart=false
redirect_stderr=true
stdout_logfile=/opt/miga-crm/logs/supervisor.log
```

---

### 2. 使用Gunicorn + Flask（如需Web界面）

如果需要Web监控界面：

```bash
# 安装
pip install gunicorn flask

# 创建Web服务
nano /opt/miga-crm/web_server.py
```

---

## 🔐 安全建议

1. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **配置防火墙**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   ```

3. **使用密钥登录代替密码**
   ```bash
   ssh-keygen -t rsa -b 4096
   # 将公钥添加到服务器 ~/.ssh/authorized_keys
   ```

4. **定期备份数据**
   - 使用上面的backup.sh脚本
   - 或使用云服务商的快照功能

---

## 📞 技术支持

如遇到问题，请检查：
1. 日志文件：`/opt/miga-crm/logs/`
2. 系统日志：`/var/log/syslog`
3. Cron日志：`sudo grep CRON /var/log/syslog`

---

## ✅ 部署检查清单

完成部署后，请确认以下项目：

- [ ] 服务器购买并连接成功
- [ ] Python 3.8+ 已安装
- [ ] 项目文件已上传到 `/opt/miga-crm/`
- [ ] 虚拟环境已创建并激活
- [ ] 所有依赖包已安装
- [ ] `.env` 配置文件已创建并填写正确
- [ ] 系统初始化成功（4个数据库文件已创建）
- [ ] 定时任务已配置（crontab -l 可看到任务）
- [ ] 手动执行每日工作流成功
- [ ] 测试邮件成功发送到 info@miga.cc
- [ ] 日志目录有正常输出
- [ ] 备份脚本已配置（可选）

---

## 🎉 部署完成！

恭喜！你的外贸客户开发系统已成功部署到云端！

**下一步**：
1. 等待第二天早上8:00，检查是否自动执行
2. 确认收到每日报告邮件
3. 查看日志确认系统正常运行

**系统将自动**：
- 📊 每天执行市场研究和客户开发
- 📧 每天发送工作报告到你的邮箱
- 🎯 每月自动调整目标
- 📈 基于数据驱动持续优化

---

**祝你外贸业务蒸蒸日上！🚀**
