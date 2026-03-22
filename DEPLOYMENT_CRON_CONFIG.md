# MIGA 数据驱动外贸客户开发系统 - 定时任务配置

## Linux/macOS Cron 配置

### 每日工作流（每天晚上10点执行）
```bash
0 22 * * * cd /path/to/project && python main_data_driven.py --daily >> /app/work/logs/bypass/app.log 2>&1
```

### 周度工作流（每周日晚上10点执行）
```bash
0 22 * * 0 cd /path/to/project && python main_data_driven.py --weekly >> /app/work/logs/bypass/app.log 2>&1
```

### 月度工作流（每月最后一天晚上10点执行）
```bash
0 22 28-31 * * cd /path/to/project && python main_data_driven.py --monthly >> /app/work/logs/bypass/app.log 2>&1
```

## 安装 Cron 任务

### 1. 打开 crontab 编辑器
```bash
crontab -e
```

### 2. 添加以下任务
```bash
# MIGA 数据驱动系统定时任务
# 每日工作流 - 每天22:00执行
0 22 * * * cd /path/to/project && python main_data_driven.py --daily >> /app/work/logs/bypass/app.log 2>&1

# 周度工作流 - 每周日22:00执行
0 22 * * 0 cd /path/to/project && python main_data_driven.py --weekly >> /app/work/logs/bypass/app.log 2>&1

# 月度工作流 - 每月最后一天22:00执行
0 22 28-31 * * cd /path/to/project && python main_data_driven.py --monthly >> /app/work/logs/bypass/app.log 2>&1
```

### 3. 保存并退出
- Vim: 按 `Esc`，输入 `:wq`，按 `Enter`
- Nano: 按 `Ctrl+O` 保存，按 `Ctrl+X` 退出

### 4. 验证任务已添加
```bash
crontab -l
```

## Windows Task Scheduler 配置

### 创建每日任务

1. 打开"任务计划程序"（Task Scheduler）
2. 点击右侧"创建基本任务"
3. 输入名称：`MIGA 每日工作流`
4. 选择触发器：`每天`
5. 设置时间：`22:00`
6. 选择操作：`启动程序`
7. 程序：`python.exe`（完整路径，如 `C:\Python312\python.exe`）
8. 参数：`main_data_driven.py --daily`
9. 起始于：`项目目录路径`（如 `C:\Users\MIGA\Project`）
10. 点击"完成"

### 创建周度任务

1. 打开"任务计划程序"
2. 点击右侧"创建基本任务"
3. 输入名称：`MIGA 周度工作流`
4. 选择触发器：`每周`
5. 设置时间：`22:00`
6. 选择星期日
7. 选择操作：`启动程序`
8. 程序：`python.exe`（完整路径）
9. 参数：`main_data_driven.py --weekly`
10. 起始于：`项目目录路径`
11. 点击"完成"

### 创建月度任务

1. 打开"任务计划程序"
2. 点击右侧"创建基本任务"
3. 输入名称：`MIGA 月度工作流`
4. 选择触发器：`每月`
5. 设置时间：`22:00`
6. 选择月份：`1-12`
7. 选择日期：`28,29,30,31`（确保月末都能执行）
8. 选择操作：`启动程序`
9. 程序：`python.exe`（完整路径）
10. 参数：`main_data_driven.py --monthly`
11. 起始于：`项目目录路径`
12. 点击"完成"

## Docker 容器配置

### 创建 cron 脚本文件

创建 `cron_tasks.sh` 文件：
```bash
#!/bin/bash
# 每日工作流 - 每天22:00
0 22 * * * cd /app && python main_data_driven.py --daily >> /app/work/logs/bypass/app.log 2>&1

# 周度工作流 - 每周日22:00
0 22 * * 0 cd /app && python main_data_driven.py --weekly >> /app/work/logs/bypass/app.log 2>&1

# 月度工作流 - 每月最后一天22:00
0 22 28-31 * * cd /app && python main_data_driven.py --monthly >> /app/work/logs/bypass/app.log 2>&1
```

### Dockerfile 配置

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 复制项目文件
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 安装 cron
RUN apt-get update && apt-get install -y cron

# 复制 cron 配置
COPY cron_tasks.sh /etc/cron.d/miga-cron

# 设置权限
RUN chmod 0644 /etc/cron.d/miga-cron
RUN crontab /etc/cron.d/miga-cron

# 启动 cron
CMD cron -f
```

## systemd 服务配置（Linux）

### 创建服务文件

创建 `/etc/systemd/system/miga-daily.service`：
```ini
[Unit]
Description=MIGA Daily Workflow
After=network.target

[Service]
Type=oneshot
User=root
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 main_data_driven.py --daily
StandardOutput=append:/app/work/logs/bypass/app.log
StandardError=append:/app/work/logs/bypass/app.log

[Install]
WantedBy=multi-user.target
```

### 创建定时器文件

创建 `/etc/systemd/system/miga-daily.timer`：
```ini
[Unit]
Description=MIGA Daily Workflow Timer

[Timer]
OnCalendar=*-*-* 22:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动定时器
sudo systemctl start miga-daily.timer

# 启用开机自启
sudo systemctl enable miga-daily.timer

# 查看状态
sudo systemctl status miga-daily.timer
```

## 监控和日志

### 查看日志

```bash
# 查看最新日志
tail -f /app/work/logs/bypass/app.log

# 搜索错误
grep -i "error" /app/work/logs/bypass/app.log

# 查看今天的日志
grep "$(date +%Y-%m-%d)" /app/work/logs/bypass/app.log
```

### 查看定时任务执行情况

```bash
# Linux/macOS
grep CRON /var/log/syslog

# 或者
journalctl -u cron
```

## 故障排查

### 问题1：定时任务没有执行

**检查步骤**：
1. 确认 cron 服务正在运行
```bash
# Linux
sudo systemctl status cron

# macOS
sudo launchctl list | grep cron
```

2. 检查 cron 日志
```bash
grep CRON /var/log/syslog
```

3. 手动执行命令测试
```bash
cd /path/to/project && python main_data_driven.py --daily
```

### 问题2：邮件发送失败

**检查步骤**：
1. 检查网络连接
```bash
ping api.resend.com
```

2. 查看日志中的错误信息
```bash
grep -i "error\|failed" /app/work/logs/bypass/app.log
```

3. 验证 API Key 配置

### 问题3：数据库文件权限问题

**解决方案**：
```bash
# 确保数据库文件有正确的权限
chmod 644 *.db
```

## 建议的执行时间

- **每日工作流**: 晚上 22:00（确保所有白天工作已完成）
- **周度工作流**: 周日 22:00（总结一周工作）
- **月度工作流**: 月末最后一天 22:00（生成月度报告）

## 安全建议

1. **保护 API Key**: 确保 API Key 不被泄露
2. **日志轮转**: 设置日志轮转，避免日志文件过大
3. **备份**: 定期备份数据库文件
4. **监控**: 设置监控系统，及时发现异常

---

**配置完成后，请定期检查系统状态和日志，确保定时任务正常运行。**
