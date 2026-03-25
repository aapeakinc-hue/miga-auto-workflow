# GitHub Actions 修复脚本

> **用途**: 修复GitHub Actions工作流运行失败问题
> **日期**: 2026年3月25日

---

## 🚨 发现的问题

### 1. Python路径问题

**问题**: 模块导入路径可能不正确

**影响**:
- `simple_auto_workflow_v2.py` 无法导入 `utils.retry_utils`
- `intelligent_auto_ops.py` 无法导入 `monitoring.auto_monitor`

---

## ✅ 解决方案

### 方案: 修复Python路径

#### 修改 `src/simple_auto_workflow_v2.py`

**当前代码**:
```python
# 添加 utils 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入重试和健康检查工具
from utils.retry_utils import retry_on_failure, APIHealthChecker, log_retry_attempt
```

**修复后**:
```python
# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入重试和健康检查工具
from src.utils.retry_utils import retry_on_failure, APIHealthChecker, log_retry_attempt
```

---

#### 修改 `src/intelligent_auto_ops.py`

**当前代码**:
```python
# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入运维模块
from monitoring.auto_monitor import WorkflowMonitor, AutoFixer, PerformanceTracker
```

**修复后**:
```python
# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入运维模块
from src.monitoring.auto_monitor import WorkflowMonitor, AutoFixer, PerformanceTracker
```

---

## 🔧 应用修复

### 方法1: 手动修改

1. 打开 `src/simple_auto_workflow_v2.py`
2. 找到 `sys.path.insert(0, ...)`
3. 修改为上面"修复后"的代码
4. 打开 `src/intelligent_auto_ops.py`
5. 找到 `sys.path.insert(0, ...)`
6. 修改为上面"修复后"的代码

---

### 方法2: 使用脚本自动修复（推荐）

运行以下命令：

```bash
# 创建修复脚本
cat > fix_python_path.py << 'EOF'
#!/usr/bin/env python3
"""
修复Python路径问题
"""
import os
import re

def fix_simple_auto_workflow():
    """修复 simple_auto_workflow_v2.py"""
    file_path = 'src/simple_auto_workflow_v2.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换路径添加代码
    old_code = """# 添加 utils 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入重试和健康检查工具
from utils.retry_utils import """

    new_code = """# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入重试和健康检查工具
from src.utils.retry_utils import """

    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成: {file_path}")
        return True
    else:
        print(f"⚠️  未找到需要修复的代码: {file_path}")
        return False


def fix_intelligent_auto_ops():
    """修复 intelligent_auto_ops.py"""
    file_path = 'src/intelligent_auto_ops.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换路径添加代码
    old_code = """# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入运维模块
from monitoring.auto_monitor import """

    new_code = """# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入运维模块
from src.monitoring.auto_monitor import """

    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成: {file_path}")
        return True
    else:
        print(f"⚠️  未找到需要修复的代码: {file_path}")
        return False


if __name__ == "__main__":
    print("=== 修复Python路径问题 ===")
    fix1 = fix_simple_auto_workflow()
    fix2 = fix_intelligent_auto_ops()
    
    if fix1 or fix2:
        print("\n✅ 修复完成！请提交代码。")
    else:
        print("\n⚠️  未发现需要修复的问题，可能已经修复过。")
EOF

# 运行修复脚本
python3 fix_python_path.py
```

---

## 🧪 测试修复

### 运行测试

```bash
# 测试 simple_auto_workflow_v2.py
cd src
python3 -c "
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from src.utils.retry_utils import retry_on_failure
print('✅ simple_auto_workflow_v2.py 导入成功')
"

# 测试 intelligent_auto_ops.py
cd src
python3 -c "
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from src.monitoring.auto_monitor import WorkflowMonitor
print('✅ intelligent_auto_ops.py 导入成功')
"
```

---

## 📋 GitHub Secrets配置

### 必须配置的Secrets

在GitHub仓库中配置以下Secrets：

**路径**: `Settings → Secrets and variables → Actions`

| Secret名称 | 描述 | 必填 |
|-----------|------|------|
| `SNOVIO_API_KEY` | Snov.io API密钥 | ✅ |
| `RESEND_API_KEY` | Resend API密钥 | ✅ |
| `NOTIFICATION_EMAIL` | 通知邮箱地址 | ✅ |
| `GITHUB_TOKEN` | GitHub API令牌 | ✅ (自动提供) |

---

## 🚀 提交修复

### 提交代码

```bash
# 添加修改的文件
git add src/simple_auto_workflow_v2.py src/intelligent_auto_ops.py

# 提交
git commit -m "fix: 修复Python路径导入问题，解决GitHub Actions运行失败"

# 推送
git push origin main
```

---

## ✅ 验证修复

### 检查GitHub Actions

1. 访问仓库的 `Actions` 标签页
2. 查看最新的工作流运行
3. 检查是否成功

### 预期结果

- ✅ 工作流成功运行
- ✅ 没有导入错误
- ✅ 邮件通知发送成功

---

## 📞 故障排查

### 如果修复后仍然失败

1. **检查日志**
   - 在GitHub Actions页面查看详细日志
   - 查找具体的错误信息

2. **检查Secrets**
   - 确保所有必需的Secrets都已配置
   - 确保Secrets的值正确

3. **检查依赖**
   - 确保所有依赖都已安装
   - 检查requirements.txt是否完整

4. **检查网络**
   - 确保GitHub Actions可以访问外部API
   - 检查API密钥是否有效

---

**文档版本**: v1.0
**创建日期**: 2026年3月25日
**维护人**: Migac Team
