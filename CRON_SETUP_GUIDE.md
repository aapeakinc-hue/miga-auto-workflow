# Cron 定时任务配置指南

## 🎯 目标

配置每天自动运行外贸客户开发工作流，无需手动操作。

---

## 📋 系统信息

- **项目路径**: /workspace/projects
- **Python 路径**: /usr/bin/python
- **工作流脚本**: src/auto_workflow.py

---

## 🚀 Linux/Mac 系统

### 方法1：使用 crontab（推荐）

#### 步骤1：编辑 crontab

```bash
crontab -e
```

首次使用会提示选择编辑器，推荐选择 `nano` 或 `vim`。

#### 步骤2：添加 Cron 任务

在文件末尾添加以下内容：

```bash
# 每天上午 9 点（北京时间）运行
0 1 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
```

**时间说明**：
- `0 1 * * *` = UTC 时间凌晨 1 点 = 北京时间上午 9 点
- UTC 和北京时间时差 8 小时

**其他时间选项**：

```bash
# 每天上午 9 点和下午 3 点（北京时间）
0 1,7 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1

# 每隔 6 小时运行一次
0 */6 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1

# 每天上午 9 点（UTC 时间，北京时间下午 5 点）
0 9 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
```

#### 步骤3：保存并退出

- **Nano**: 按 `Ctrl+X`，然后按 `Y`，最后按 `Enter`
- **Vim**: 按 `Esc`，输入 `:wq`，按 `Enter`

#### 步骤4：验证 Cron 任务

```bash
crontab -l
```

应该能看到你添加的任务。

---

### 方法2：使用配置文件（推荐用于管理）

#### 步骤1：创建 Cron 文件

```bash
cat > miga_crontab << 'EOF'
# 外贸客户开发工作流 - 每天上午 9 点（北京时间）
0 1 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
EOF
```

#### 步骤2：安装 Cron 任务

```bash
crontab miga_crontab
```

#### 步骤3：验证

```bash
crontab -l
```

---

### 方法3：使用系统 Cron.d 目录（系统级）

```bash
sudo tee /etc/cron.d/miga-auto-workflow > /dev/null << 'EOF'
# 外贸客户开发工作流 - 每天上午 9 点（北京时间）
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
0 1 * * * root cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
EOF
```

```bash
sudo chmod 644 /etc/cron.d/miga-auto-workflow
sudo service cron restart  # 或 sudo systemctl restart cron
```

---

## 🪟 Windows 系统

### 使用任务计划程序

#### 步骤1：打开任务计划程序

- 按 `Win + R`
- 输入 `taskschd.msc`
- 按回车

#### 步骤2：创建基本任务

1. 点击右侧 "创建基本任务"
2. 名称：`MIGA 外贸客户开发`
3. 描述：`每天自动运行外贸客户开发工作流`
4. 点击 "下一步"

#### 步骤3：设置触发器

1. 选择 "每天"
2. 开始时间：`09:00:00`
3. 重复周期：`每天`
4. 点击 "下一步"

#### 步骤4：设置操作

1. 选择 "启动程序"
2. 程序或脚本：`C:\Python39\python.exe`（根据你的 Python 安装路径）
3. 添加参数（可选）：`src/auto_workflow.py`
4. 起始于：`C:\workspace\projects`（根据你的项目路径）
5. 点击 "下一步"

#### 步骤5：完成

1. 查看摘要
2. 勾选 "当单击完成时，打开此任务属性的对话框"
3. 点击 "完成"

#### 步骤6：配置任务属性

1. 在 "常规" 标签：
   - 选择 "不管用户是否登录都要运行"
   - 勾选 "使用最高权限运行"

2. 在 "操作" 标签：
   - 选中现有操作，点击 "编辑"
   - 添加参数：`src/auto_workflow.py`
   - 添加重定向：`>> logs\cron.log 2>&1`

3. 点击 "确定"

#### 步骤7：测试任务

- 右键点击任务
- 选择 "运行"
- 检查日志文件

---

## ✅ 验证配置

### 1. 检查 Cron 服务状态

```bash
# Linux/Mac
sudo service cron status
# 或
sudo systemctl status cron
```

应该显示 `active (running)` 或 `running`

### 2. 测试脚本

```bash
cd /workspace/projects
/usr/bin/python src/auto_workflow.py
```

确认脚本正常运行。

### 3. 查看日志

```bash
tail -f logs/cron.log
```

### 4. 检查下次运行时间

```bash
# 查看系统下次 Cron 运行时间
anacron -T  # 如果使用 anacron
# 或查看系统时间
date
```

---

## 📊 监控 Cron 任务

### 查看实时日志

```bash
tail -f logs/cron.log
```

### 查看发送历史

```bash
cat logs/sent_emails.json
```

### 查看每日报告

```bash
ls -lh logs/daily_report_*.txt
cat logs/daily_report_*.txt | tail -50
```

### 查看 Cron 日志

```bash
# Ubuntu/Debian
sudo grep CRON /var/log/syslog | tail -20

# CentOS/RHEL
sudo tail -f /var/log/cron

# macOS
log show --predicate 'process == "cron"' --info --last 1h
```

---

## 🐛 故障排查

### 问题1：任务没有运行

**检查**：
```bash
# 1. 检查 Cron 服务
sudo service cron status

# 2. 查看 Cron 日志
sudo grep CRON /var/log/syslog | tail -20

# 3. 查看任务列表
crontab -l
```

**解决**：
- 确保 Cron 服务正在运行
- 检查任务配置是否正确
- 查看日志找出错误原因

---

### 问题2：Python 路径错误

**检查**：
```bash
which python
```

**解决**：
- 使用绝对路径（如 `/usr/bin/python`）
- 或在 crontab 中设置 PATH

```bash
PATH=/usr/local/bin:/usr/bin:/bin
0 1 * * * cd /workspace/projects && python src/auto_workflow.py >> logs/cron.log 2>&1
```

---

### 问题3：工作目录错误

**解决**：
- 在 crontab 中使用 `cd` 切换到工作目录
- 使用绝对路径

---

### 问题4：权限问题

**解决**：
```bash
# 确保日志目录可写
chmod 755 logs

# 确保脚本可执行
chmod +x src/auto_workflow.py
```

---

## 🔄 管理 Cron 任务

### 查看当前任务

```bash
crontab -l
```

### 编辑任务

```bash
crontab -e
```

### 删除所有任务

```bash
crontab -r
```

### 备份任务

```bash
crontab -l > my_crontab_backup.txt
```

### 恢复任务

```bash
crontab my_crontab_backup.txt
```

### 临时禁用任务

在每行前加 `#` 注释：
```bash
# 0 1 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
```

---

## 🎯 推荐配置

### 最佳实践

**使用配置文件方式**（推荐）：

```bash
# 1. 创建配置文件
cat > miga_crontab << 'EOF'
# 外贸客户开发工作流
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

# 每天上午 9 点（北京时间）
0 1 * * * cd /workspace/projects && /usr/bin/python src/auto_workflow.py >> logs/cron.log 2>&1
EOF

# 2. 安装任务
crontab miga_crontab

# 3. 验证
crontab -l

# 4. 查看日志
tail -f logs/cron.log
```

---

## 📋 完整检查清单

- [ ] Python 环境正常（`python --version`）
- [ ] 工作流脚本测试通过（`python src/auto_workflow.py`）
- [ ] 日志目录存在且可写（`logs/`）
- [ ] Cron 服务运行正常（`sudo service cron status`）
- [ ] Cron 任务已添加（`crontab -l`）
- [ ] 时间配置正确（考虑时区）
- [ ] 测试运行成功
- [ ] 日志正常输出

---

## 🎉 配置完成

### 配置成功后

**每天自动完成**：
- ✅ 搜索潜在客户
- ✅ 获取邮箱地址
- ✅ 生成开发邮件
- ✅ 发送邮件
- ✅ 记录发送历史
- ✅ 生成每日报告

**你只需要**：
- 📧 检查邮箱回复
- 📊 查看发送报告
- 💬 跟进有兴趣的客户

---

## 💡 提示

**如果需要立即测试**：
```bash
cd /workspace/projects
/usr/bin/python src/auto_workflow.py
```

**查看日志**：
```bash
tail -f logs/cron.log
```

**查看发送历史**：
```bash
cat logs/sent_emails.json | jq .
```

---

**配置完成后，工作流将全自动运行！** 🚀
