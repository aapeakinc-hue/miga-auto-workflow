# ❌ Failure 故障排查指南

## 🔍 快速诊断

### 请确认具体是哪个失败？

1. **GitHub Actions 运行失败**
   - 运行 workflow 时显示红色 ❌
   - 查看运行日志显示错误

2. **本地运行失败**
   - 运行 `python3 src/main.py` 失败
   - 运行 `test_run` 失败

3. **其他失败**
   - 请描述具体错误信息

---

## 🐛 常见失败原因及解决方案

### 问题 1: GitHub Actions 环境变量未找到

**错误信息**：
```
ERROR: SNOVIO_API_TOKEN not found
ERROR: RESEND_API_KEY not found
```

**原因**：
- GitHub Secrets 配置的名称与 workflow 文件引用不一致

**解决方案**：
1. 检查 GitHub Secrets 配置
   - 访问：https://github.com/aapeakinc-hue/miga-auto-workflow/settings/secrets/actions
   - 确认以下 Secrets 存在：
     - `SNOVIO_API_TOKEN`
     - `SNOVIO_CLIENT_ID`
     - `RESEND_API_KEY`

2. 检查 workflow 文件引用
   - 查看 `.github/workflows/auto-workflow.yml`
   - 确认引用的 Secret 名称正确

**正确的配置**：
```yaml
env:
  SNOVIO_API_TOKEN: ${{ secrets.SNOVIO_API_TOKEN }}
  SNOVIO_CLIENT_ID: ${{ secrets.SNOVIO_CLIENT_ID }}
  RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
```

---

### 问题 2: Python 依赖安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement
ERROR: No matching distribution found for xxx
```

**原因**：
- 依赖包版本不兼容
- 网络问题导致下载失败

**解决方案**：
1. 检查 `requirements.txt` 是否正确
2. 更新依赖版本
3. 重新运行 workflow

---

### 问题 3: 工作流执行超时

**错误信息**：
```
Error: The operation was timeout
```

**原因**：
- API 请求超时
- 工作流执行时间过长

**解决方案**：
1. 检查 API 服务是否正常
2. 减少每次处理的客户数量
3. 增加 workflow 超时时间

---

### 问题 4: 邮件发送失败

**错误信息**：
```
ERROR: Failed to send email
ERROR: API key invalid
```

**原因**：
- API Key 无效或过期
- 邮箱地址不存在

**解决方案**：
1. 检查 API Key 是否正确
2. 确认 API Key 没有过期
3. 检查邮箱地址格式

---

### 问题 5: 内存不足

**错误信息**：
```
Error: Out of memory
```

**原因**：
- 处理的数据量过大
- 内存泄漏

**解决方案**：
1. 减少批处理大小
2. 优化代码内存使用
3. 增加 GitHub Actions runner 内存

---

## 🔧 调试步骤

### 步骤 1: 查看详细日志

1. 进入 GitHub Actions 页面
   - 访问：https://github.com/aapeakinc-hue/miga-auto-workflow/actions

2. 点击失败的 workflow 运行

3. 点击每个失败的步骤
   - 查看详细日志
   - 找到错误堆栈

4. 记录错误信息
   - 复制错误消息
   - 复制错误堆栈

### 步骤 2: 本地复现

尝试在本地运行相同的命令：

```bash
# 设置环境变量
export SNOVIO_API_TOKEN="fbf98546081c2793e21d6de6540ce2ca"
export SNOVIO_CLIENT_ID="746628993ee9eda28e455e53751030bd"
export RESEND_API_KEY="re_5pAqrE8V_6DgcPEqkjR8yyN3PzSRhStat"

# 运行工作流
cd src
python auto_workflow_with_real_api.py --keywords "美国水晶工艺品批发商"
```

### 步骤 3: 检查配置文件

1. 检查 workflow 文件
   ```bash
   cat .github/workflows/auto-workflow.yml
   ```

2. 检查 Secrets 配置
   - 访问 GitHub Secrets 页面
   - 确认所有 Secrets 都已配置

3. 检查依赖文件
   ```bash
   cat requirements.txt
   ```

---

## 📞 需要帮助？

如果以上方法无法解决问题，请提供：

1. **错误信息**
   - 完整的错误消息
   - 错误堆栈信息

2. **运行日志**
   - GitHub Actions 运行链接
   - 或复制相关日志片段

3. **配置信息**
   - 确认哪些 Secrets 已配置
   - workflow 文件的引用部分

4. **复现步骤**
   - 如何触发这个错误
   - 是手动运行还是自动运行

---

## ✅ 成功的标准

一个成功的运行应该包含：

```
✅ 检出代码成功
✅ Python 环境设置成功
✅ 依赖安装成功
✅ 运行自动化工作流成功
📊 发送统计：
  - 总数: 3
  - 成功: 3
  - 失败: 0
✅ 日志上传成功
✅ 通知发送成功
```

---

**请告诉我具体遇到了什么错误，我会帮您解决！**
