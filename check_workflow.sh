#!/bin/bash
# 诊断脚本：检查 GitHub Actions 失败原因

echo "========================================="
echo "  GitHub Actions 失败诊断"
echo "========================================="
echo ""

# 检查 Python 脚本是否存在
echo "🔍 检查 Python 脚本..."
if [ -f "src/simple_auto_workflow.py" ]; then
    echo "✅ src/simple_auto_workflow.py 存在"
else
    echo "❌ src/simple_auto_workflow.py 不存在"
fi

if [ -f "src/intelligent_auto_ops.py" ]; then
    echo "✅ src/intelligent_auto_ops.py 存在"
else
    echo "❌ src/intelligent_auto_ops.py 不存在"
fi

if [ -f "src/send_notification.py" ]; then
    echo "✅ src/send_notification.py 存在"
else
    echo "❌ src/send_notification.py 不存在"
fi

echo ""
echo "🔍 检查目录结构..."
if [ -d "src" ]; then
    echo "✅ src 目录存在"
    echo "src 目录内容："
    ls -la src/
else
    echo "❌ src 目录不存在"
fi

echo ""
echo "🔍 检查依赖..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt 存在"
    echo "内容："
    cat requirements.txt
else
    echo "⚠️  requirements.txt 不存在"
fi

echo ""
echo "🔍 检查日志目录..."
mkdir -p logs
echo "✅ logs 目录已创建"

echo ""
echo "========================================="
echo "  诊断完成"
echo "========================================="
