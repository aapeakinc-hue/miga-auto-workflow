# 📚 MIGA外贸客户开发系统 - 云端部署文档包

## 🎯 这个文档包包含什么？

这是完整的云端部署指南，帮助你将外贸客户开发系统部署到云服务器，实现7x24小时全自动运行。

---

## 📄 文档列表

### 1. [CLOUD_DEPLOYMENT_GUIDE.md](./CLOUD_DEPLOYMENT_GUIDE.md) - 完整部署指南
**适合人群**：需要详细了解每个步骤的用户
**包含内容**：
- 服务器要求和购买指南
- 详细的部署步骤（环境配置、代码上传、定时任务配置）
- 故障排查指南
- 安全建议和性能优化
- 监控和维护说明

---

### 2. [QUICK_START_CLOUD.md](./QUICK_START_CLOUD.md) - 5分钟快速开始
**适合人群**：希望快速上手的用户
**包含内容**：
- 购买云服务器的快速步骤
- 连接服务器的简单方法
- 上传项目文件的3种方法
- 一键部署环境
- 配置和测试的简化步骤
- 常见问题快速解决

---

## 🛠️ 脚本工具

### 1. [deploy_on_server.sh](./deploy_on_server.sh) - 一键部署脚本
**功能**：自动完成服务器环境配置
**使用方法**：
```bash
# 上传脚本到服务器后执行
sudo bash deploy_on_server.sh
```

**自动完成**：
- 安装系统依赖（git, python3, cron等）
- 创建项目目录
- 创建Python虚拟环境
- 安装所有Python依赖包
- 创建目录结构
- 生成环境变量配置模板
- 创建数据库备份脚本
- 生成定时任务模板

---

### 2. [system_status.sh](./system_status.sh) - 系统状态监控脚本
**功能**：一键查看系统运行状态
**使用方法**：
```bash
bash system_status.sh
```

**检查内容**：
- 系统基本信息
- Python环境
- 项目目录
- 虚拟环境
- 数据库文件
- 定时任务
- 服务状态
- 最近日志
- 系统资源
- Python进程
- 环境变量配置
- 网络连接
- 最近执行情况

---

## 🚀 快速开始（推荐路线）

### 路线A：新手路线（最简单）

1. **阅读**：[QUICK_START_CLOUD.md](./QUICK_START_CLOUD.md)
2. **购买服务器**：按照文档第1步购买
3. **连接服务器**：按照文档第2步连接
4. **上传项目**：按照文档第3步上传
5. **运行脚本**：
   ```bash
   sudo bash deploy_on_server.sh
   ```
6. **配置系统**：按照快速开始文档第5步
7. **完成！**

---

### 路线B：进阶路线（了解更多）

1. **阅读**：[CLOUD_DEPLOYMENT_GUIDE.md](./CLOUD_DEPLOYMENT_GUIDE.md)
2. **手动配置**：按照完整指南逐步操作
3. **监控维护**：使用 [system_status.sh](./system_status.sh) 定期检查

---

## 📋 部署检查清单

完成部署后，请确认以下项目：

### 基础环境
- [ ] 云服务器已购买并可以SSH连接
- [ ] Ubuntu 20.04+ / CentOS 7+ 操作系统
- [ ] Python 3.8+ 已安装
- [ ] 项目文件已上传到 `/opt/miga-crm/`

### 环境配置
- [ ] Python虚拟环境已创建
- [ ] 所有依赖包已安装（langgraph, langchain, requests等）
- [ ] 环境变量文件 `.env` 已创建并配置正确
- [ ] 目录结构完整（logs, data, reports等）

### 系统初始化
- [ ] 系统初始化成功（4个数据库文件已创建）
  - market_data.db
  - goals.db
  - daily_planner.db
  - miga_crm.db

### 自动化配置
- [ ] 定时任务已配置（crontab -l 可以看到）
- [ ] 每日工作流定时任务（每天早上8:00）
- [ ] 目标调整定时任务（每月1号凌晨）
- [ ] 数据备份定时任务（每天凌晨）

### 测试验证
- [ ] 手动执行每日工作流成功
- [ ] 测试邮件成功发送到 info@miga.cc
- [ ] 日志目录有正常输出
- [ ] 系统状态监控脚本运行正常

---

## 🔧 常用命令速查

### 连接服务器
```bash
ssh root@你的服务器IP
```

### 查看系统状态
```bash
bash /opt/miga-crm/system_status.sh
```

### 手动执行每日工作流
```bash
cd /opt/miga-crm
source venv/bin/activate
python main_data_driven.py --daily
```

### 查看实时日志
```bash
tail -f /opt/miga-crm/logs/daily_workflow.log
```

### 查看定时任务
```bash
crontab -l
```

### 编辑定时任务
```bash
crontab -e
```

### 重新初始化系统
```bash
cd /opt/miga-crm
source venv/bin/activate
python main_data_driven.py --init
```

### 手动备份数据
```bash
bash /opt/miga-crm/backup.sh
```

### 重启Cron服务
```bash
sudo service cron restart
```

---

## 🆘 常见问题

### Q1: 定时任务没有执行？
**解决**：
```bash
# 检查Cron服务
service cron status

# 查看Cron日志
sudo grep CRON /var/log/syslog | tail -20

# 手动测试命令
cd /opt/miga-crm && source venv/bin/activate && python main_data_driven.py --daily
```

### Q2: 邮件发送失败？
**解决**：
```bash
# 检查环境变量配置
cat /opt/miga-crm/.env

# 查看错误日志
tail -n 50 /opt/miga-crm/logs/daily_workflow.log
```

### Q3: 数据库文件损坏？
**解决**：
```bash
# 使用备份恢复
cp /opt/miga-crm/backups/backup_xxx/data/*.db /opt/miga-crm/data/

# 或重新初始化
cd /opt/miga-crm
source venv/bin/activate
python main_data_driven.py --init
```

### Q4: 系统资源不足？
**解决**：
```bash
# 查看资源使用
htop

# 清理日志
find /opt/miga-crm/logs -name "*.log" -mtime +7 -delete
```

---

## 📞 技术支持

### 获取帮助

1. **查看日志**：
   ```bash
   cat /opt/miga-crm/logs/daily_workflow.log
   ```

2. **查看系统状态**：
   ```bash
   bash /opt/miga-crm/system_status.sh
   ```

3. **检查服务**：
   ```bash
   sudo grep CRON /var/log/syslog | tail -20
   ```

---

## ✅ 部署完成标志

当以下条件全部满足时，说明部署成功：

1. ✅ 可以SSH连接到服务器
2. ✅ 项目文件在 `/opt/miga-crm/` 目录
3. ✅ 运行 `bash system_status.sh` 显示全部绿色 ✅
4. ✅ 定时任务已配置（crontab -l 可见）
5. ✅ 手动执行工作流成功
6. ✅ 测试邮件成功发送
7. ✅ 次日早上8:00自动执行并收到邮件

---

## 🎉 祝你部署成功！

**系统将自动为你**：
- 📊 每天执行市场研究和客户开发
- 📧 每天发送工作报告到你的邮箱
- 🎯 每月自动调整目标
- 📈 基于数据驱动持续优化

**如果遇到问题，请参考**：
- [CLOUD_DEPLOYMENT_GUIDE.md](./CLOUD_DEPLOYMENT_GUIDE.md) - 完整指南
- [QUICK_START_CLOUD.md](./QUICK_START_CLOUD.md) - 快速开始

---

**祝你外贸业务蒸蒸日上！🚀**
