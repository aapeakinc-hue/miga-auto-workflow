# 🚀 Google Cloud 免费部署详细教程

## ✅ 第1步：启用 Compute Engine API

**你已经在这个页面了！**

1. 在你看到的 "Compute Engine API" 页面上
2. 点击 **"启用"** (Enable) 按钮
3. 等待几秒钟，看到状态变为 **"已启用"**

---

## 📝 第2步：创建虚拟机（VM Instance）

### 方法A：通过控制台创建（推荐新手）

#### 2.1 进入虚拟机创建页面
1. 在Google Cloud控制台左侧菜单
2. 找到 **"Compute Engine"** → 点击展开
3. 点击 **"虚拟机实例" (VM instances)**
4. 点击 **"创建实例" (Create instance)** 按钮（蓝色按钮）

#### 2.2 配置虚拟机（重要！）

##### 基本信息设置
- **名称 (Name)**: `miga-crm`
- **区域 (Region)**:
  - 推荐选择：`asia-east1` (台湾) 或 `asia-southeast1` (新加坡)
  - 这样在国内访问速度快

##### 机器配置（关键！）
- **系列 (Series)**: 选择 **"E2"** (免费tier系列)
- **机器类型 (Machine type)**: 选择 **"e2-micro"** (2 vCPU, 1GB内存)
  - ✅ 这个配置是永久免费的！
  - ❌ 不要选其他配置，否则会收费！

##### 启动盘设置
- **操作系统**: 选择 **"Ubuntu"**
- **版本**: 选择 **"Ubuntu 22.04 LTS Minimal"**
- **磁盘类型**: **"标准持久化磁盘" (Standard persistent disk)**
- **磁盘大小**: **30 GB** (免费额度内)
- 点击 **"选择" (Select)**

##### 身份和API访问权限
- **访问权限范围**: 选择 **"允许每个API的完全访问权限" (Allow full access to all Cloud APIs)**

##### 防火墙设置
- ✅ 勾选 **"允许HTTP流量" (Allow HTTP traffic)**
- ✅ 勾选 **"允许HTTPS流量" (Allow HTTPS traffic)**

#### 2.3 创建虚拟机
1. 检查所有配置无误
2. 点击页面底部的 **"创建" (Create)** 按钮
3. 等待1-2分钟，虚拟机创建完成

#### 2.4 查看虚拟机信息
1. 创建完成后，你会看到虚拟机列表
2. 找到你刚创建的 `miga-crm` 虚拟机
3. 记录下 **"外部IP" (External IP)** - 这个就是服务器的公网IP地址

---

## 🔑 第3步：设置SSH访问

### 方法A：使用Google Cloud Console的SSH按钮（最简单）

1. 在虚拟机列表中，找到 `miga-crm`
2. 点击右侧的 **"SSH"** 按钮
3. 会打开一个新的浏览器窗口/标签
4. 自动连接到虚拟机，无需密码

### 方法B：使用自己的SSH密钥（推荐，更安全）

#### 3.1 创建SSH密钥对
**在你的本地电脑上执行**：

**Windows用户 (PowerShell)**:
```powershell
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -f ~/.ssh/google_cloud_key

# 查看公钥
cat ~/.ssh/google_cloud_key.pub
```

**Mac/Linux用户**:
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -f ~/.ssh/google_cloud_key

# 查看公钥
cat ~/.ssh/google_cloud_key.pub
```

#### 3.2 添加SSH密钥到虚拟机

1. 在虚拟机列表中，找到 `miga-crm`
2. 点击虚拟机名称进入详情页
3. 点击 **"编辑" (Edit)** 按钮
4. 找到 **"SSH密钥" (SSH Keys)** 部分
5. 点击 **"添加整个项目" (Add item)**
6. 将刚才生成的公钥内容粘贴进去
7. 点击 **"保存" (Save)**

#### 3.3 使用SSH连接

**Windows用户 (PowerShell)**:
```powershell
ssh -i ~/.ssh/google_cloud_key 你的用户名@你的外部IP
```

**Mac/Linux用户**:
```bash
ssh -i ~/.ssh/google_cloud_key 你的用户名@你的外部IP
```

**注意**：
- 用户名通常是：`ubuntu` 或 你创建时设置的用户名
- 外部IP就是第2步记录的那个IP

---

## 📦 第4步：上传项目文件到服务器

### 方法A：使用SCP上传（推荐）

**在你的本地电脑上执行**：

**Windows用户 (PowerShell)**:
```powershell
# 1. 先打包项目文件
# 在项目文件夹中，右键 → 发送到 → 压缩(zipped)文件夹

# 2. 上传到服务器
scp -i ~/.ssh/google_cloud_key miga-crm.zip ubuntu@你的外部IP:/tmp/

# 示例：
# scp -i ~/.ssh/google_cloud_key miga-crm.zip ubuntu@34.123.45.67:/tmp/
```

**Mac/Linux用户**:
```bash
# 1. 先打包项目文件
tar -czf miga-crm.tar.gz 项目文件夹/

# 2. 上传到服务器
scp -i ~/.ssh/google_cloud_key miga-crm.tar.gz ubuntu@你的外部IP:/tmp/
```

### 方法B：使用Git克隆（推荐，如果有Git仓库）

**在服务器上执行**：
```bash
# 连接到服务器后
git clone https://github.com/你的用户名/miga-crm.git
mv miga-crm/* .
rm -rf miga-crm
```

---

## 🛠️ 第5步：在服务器上部署系统

### 5.1 创建项目目录
```bash
# 连接到服务器后
sudo mkdir -p /opt/miga-crm
cd /opt/miga-crm
```

### 5.2 解压项目文件

**如果是.zip文件**:
```bash
sudo mv /tmp/miga-crm.zip .
sudo unzip miga-crm.zip
sudo mv miga-crm/* .
sudo rm -rf miga-crm miga-crm.zip
```

**如果是.tar.gz文件**:
```bash
sudo mv /tmp/miga-crm.tar.gz .
sudo tar -xzf miga-crm.tar.gz
sudo mv miga-crm/* .
sudo rm -rf miga-crm miga-crm.tar.gz
```

### 5.3 运行一键部署脚本
```bash
# 上传部署脚本到服务器（如果还没有）
# 从本地上传：
scp -i ~/.ssh/google_cloud_key deploy_on_server.sh ubuntu@你的外部IP:/opt/miga-crm/

# 在服务器上运行：
cd /opt/miga-crm
sudo bash deploy_on_server.sh
```

### 5.4 编辑配置文件
```bash
nano /opt/miga-crm/.env
```

**修改以下内容**：
```env
# 邮箱配置
SMTP_PASSWORD=你的Resend_API_Key
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=info@miga.cc

# 目标配置
DEFAULT_YEARLY_GOAL=1000000
DEFAULT_MARKET_SIZE=50000000
```

**保存退出**：`Ctrl + O` → `Enter` → `Ctrl + X`

### 5.5 初始化系统
```bash
cd /opt/miga-crm
source venv/bin/activate
sudo python main_data_driven.py --init
```

**应该看到4个 "✅"**，表示数据库创建成功！

### 5.6 测试运行
```bash
sudo python main_data_driven.py --daily
```

**检查你的邮箱 info@miga.cc**，应该会收到测试邮件！

---

## ⏰ 第6步：配置定时任务

### 6.1 编辑crontab
```bash
crontab -e
```

### 6.2 添加定时任务
**在文件末尾粘贴以下内容**：

```bash
# MIGA外贸客户开发系统定时任务

# 每天早上8:00执行每日工作流
0 8 * * * cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --daily >> logs/daily_workflow.log 2>&1

# 每月1号凌晨1:00调整目标
0 1 1 * * cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --adjust_goals >> logs/monthly_adjustment.log 2>&1

# 每周日凌晨2:00生成周报
0 2 * * 0 cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --weekly >> logs/weekly_report.log 2>&1

# 每天凌晨4:00备份数据
0 4 * * * /opt/miga-crm/backup.sh >> logs/backup.log 2>&1

# 每天凌晨3:00清理7天前的日志
0 3 * * * find /opt/miga-crm/logs -name "*.log" -mtime +7 -delete
```

**保存退出**：`Ctrl + O` → `Enter` → `Ctrl + X`

---

## ✅ 第7步：验证部署

### 7.1 查看系统状态
```bash
bash /opt/miga-crm/system_status.sh
```

**所有项目都应该显示绿色 ✅**

### 7.2 查看定时任务
```bash
crontab -l
```

**应该看到刚才添加的5个定时任务**

### 7.3 查看日志
```bash
tail -f /opt/miga-crm/logs/daily_workflow.log
```

**应该看到系统运行的日志**

---

## 🎉 部署完成！

### 系统将自动：
- ✅ 每天早上8:00执行每日工作流
- ✅ 每天自动发送报告到 info@miga.cc
- ✅ 每月1号自动调整目标
- ✅ 每周自动生成周报
- ✅ 每天自动备份数据

### 常用命令：
```bash
# 查看系统状态
bash /opt/miga-crm/system_status.sh

# 查看实时日志
tail -f /opt/miga-crm/logs/daily_workflow.log

# 手动执行每日工作流
cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --daily

# 查看定时任务
crontab -l
```

---

## 💡 Google Cloud免费额度说明

### 永久免费内容：
- **虚拟机**: 1个 e2-micro 实例（每月744小时）
- **存储**: 30GB 标准持久化磁盘
- **快照**: 5GB 快照存储
- **负载均衡**: 仅限HTTP(S)负载均衡
- **出站流量**: 每月1GB免费（中国地区是10GB）

### 注意事项：
⚠️ **必须选择**：
- 机器类型：**e2-micro** (免费)
- 区域：**us-central1, us-west1, us-east1** (美国) 或 **asia-east1, asia-southeast1** (亚洲)
- 磁盘类型：**标准持久化磁盘** (Standard persistent disk)

❌ **避免选择**：
- n1, n2, n2d, c2, e2-medium/large等（会收费）
- 高性能SSD（会收费）
- 非免费区域的实例（会收费）

---

## 🔧 故障排查

### 问题1：无法连接SSH
**解决**：
1. 检查防火墙规则是否允许SSH（端口22）
2. 尝试使用Google Cloud Console的SSH按钮
3. 检查虚拟机是否正在运行

### 问题2：定时任务没有执行
**解决**：
```bash
# 检查Cron服务
sudo service cron status

# 查看系统日志
sudo journalctl -xe | grep CRON

# 手动测试命令
cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --daily
```

### 问题3：邮件发送失败
**解决**：
```bash
# 检查环境变量配置
cat /opt/miga-crm/.env

# 查看错误日志
tail -n 50 /opt/miga-crm/logs/daily_workflow.log
```

---

## 📞 需要帮助？

**如果遇到问题，请检查**：
1. **Google Cloud控制台** - 查看虚拟机状态
2. **系统日志** - `tail -f /opt/miga-crm/logs/daily_workflow.log`
3. **系统状态** - `bash /opt/miga-crm/system_status.sh`

---

**祝你部署成功！系统将为你7x24小时自动工作！🚀**
