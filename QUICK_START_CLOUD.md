# 🚀 云端部署快速开始（5分钟完成）

## ⚡ 最快部署方式（推荐新手）

### 第1步：购买云服务器（2分钟）

1. **访问云服务商**（任选一个）：
   - 腾讯云：https://cloud.tencent.com/
   - 阿里云：https://www.aliyun.com/
   - 华为云：https://www.huaweicloud.com/
   - DigitalOcean：https://www.digitalocean.com/（海外，推荐）

2. **购买配置**：
   - 地区：建议选 **香港** 或 **新加坡**（速度快）
   - 配置：2核4GB（约 ¥60-100/月）
   - 系统：Ubuntu 22.04 LTS
   - 购买时长：1个月先试试

3. **拿到服务器信息**：
   - 公网IP地址（如：123.45.67.89）
   - root密码（或SSH密钥）

---

### 第2步：连接服务器（1分钟）

**Windows用户**：
1. 按 `Win + R`
2. 输入 `cmd`，回车
3. 输入：
   ```bash
   ssh root@你的服务器IP
   ```
   例如：
   ```bash
   ssh root@123.45.67.89
   ```
4. 输入密码（不会显示字符，正常输入即可）
5. 看到 `root@xxx:~#` 说明连接成功

**Mac用户**：
1. 打开终端
2. 输入：
   ```bash
   ssh root@你的服务器IP
   ```

---

### 第3步：上传项目文件（2分钟）

**方法A：你已有项目文件**

**在你的本地电脑（Windows PowerShell）**：

1. 打开你的项目文件夹
2. 右键项目文件夹 → "发送到" → "压缩(zipped)文件夹"
3. 打开PowerShell（在项目文件夹里按住Shift+右键 → "在此处打开PowerShell窗口"）

执行：
```powershell
# 替换下面的IP和文件名
scp miga-crm.zip root@123.45.67.89:/tmp/
```

**回到服务器SSH窗口**：

```bash
# 解压到项目目录
sudo mkdir -p /opt/miga-crm
sudo mv /tmp/miga-crm.zip /opt/miga-crm/
cd /opt/miga-crm
sudo unzip miga-crm.zip
sudo mv miga-crm/* .
sudo rm -rf miga-crm miga-crm.zip
```

**方法B：直接在服务器上创建（文件较少的情况）**

**如果项目只有几个文件，直接在服务器上创建**：

```bash
cd /opt/miga-crm
sudo nano main_data_driven.py
# 粘贴代码内容，保存退出（Ctrl+O, Enter, Ctrl+X）
# 重复此步骤创建其他文件
```

---

### 第4步：一键部署环境（30秒）

**在服务器SSH窗口执行**：

```bash
# 上传部署脚本到服务器（如果你还没有）
# （这个步骤需要在本地执行，将 deploy_on_server.sh 上传到服务器）

# 然后在服务器上运行
cd /opt/miga-crm
sudo bash deploy_on_server.sh
```

**看到 "🎉 环境准备完成！" 说明成功！**

---

### 第5步：配置并运行（1分钟）

**1. 编辑配置文件**：

```bash
nano /opt/miga-crm/.env
```

**修改这几项（根据你的实际情况）**：

```env
SMTP_PASSWORD=你的API_Key
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=info@miga.cc
DEFAULT_YEARLY_GOAL=1000000  # 改成你的年度目标
```

**保存退出：`Ctrl + O` → `Enter` → `Ctrl + X`**

---

**2. 初始化系统**：

```bash
cd /opt/miga-crm
source venv/bin/activate
sudo python main_data_driven.py --init
```

**看到4个 "✅" 说明初始化成功！**

---

**3. 测试运行**：

```bash
sudo python main_data_driven.py --daily
```

**检查你的邮箱 info@miga.cc，应该会收到测试邮件！**

---

**4. 配置定时任务**：

```bash
crontab -e
```

**选择编辑器（输入1或2），然后粘贴以下内容**：

```bash
0 8 * * * cd /opt/miga-crm && source venv/bin/activate && sudo python main_data_driven.py --daily >> logs/daily_workflow.log 2>&1
```

**保存退出：`Ctrl + O` → `Enter` → `Ctrl + X`**

---

## ✅ 完成！

**现在系统会每天早上8:00自动运行！**

### 检查是否正常运行

**查看日志**：
```bash
tail -f /opt/miga-crm/logs/daily_workflow.log
```

**查看定时任务**：
```bash
crontab -l
```

---

## 🆘 遇到问题？

### 问题：连接不上服务器
**解决**：
1. 检查服务器是否开机
2. 检查IP地址是否正确
3. 检查密码是否正确

### 问题：命令不存在
**解决**：
```bash
# 如果提示找不到某个命令，先更新系统
sudo apt update && sudo apt upgrade -y
```

### 问题：权限不足
**解决**：
```bash
# 所有命令前面加上 sudo
sudo 你的命令
```

### 问题：文件上传失败
**解决**：
1. 确认文件路径正确
2. 确认服务器IP正确
3. 尝试使用其他上传方法（如WinSCP、FileZilla等图形化工具）

---

## 📞 需要帮助？

如果遇到问题，检查：
1. 日志文件：`cat /opt/miga-crm/logs/daily_workflow.log`
2. 系统日志：`sudo grep CRON /var/log/syslog | tail -20`

**祝你部署成功！🎉**
