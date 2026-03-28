#!/usr/bin/env python3
"""
故障诊断脚本 - 快速检查常见问题
"""
import os
import sys

def diagnose_issues():
    """诊断常见问题"""
    print("=" * 60)
    print("🔍 故障诊断")
    print("=" * 60)
    print()

    issues = []

    # 1. 检查环境变量
    print("1. 检查环境变量配置")
    required_vars = ['SNOVIO_API_TOKEN', 'SNOVIO_CLIENT_ID', 'RESEND_API_KEY']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: 已配置")
        else:
            print(f"  ❌ {var}: 未配置")
            issues.append(f"缺少环境变量: {var}")
    print()

    # 2. 检查必需文件
    print("2. 检查必需文件")
    required_files = [
        'src/graphs/graph.py',
        'src/graphs/state.py',
        'config/email_generate_llm_cfg.json',
        'logs/'
    ]
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}: 存在")
        else:
            print(f"  ❌ {file_path}: 不存在")
            issues.append(f"缺少文件: {file_path}")
    print()

    # 3. 检查 Python 依赖
    print("3. 检查 Python 依赖")
    try:
        import langgraph
        print(f"  ✅ langgraph: {langgraph.__version__}")
    except ImportError:
        print("  ❌ langgraph: 未安装")
        issues.append("缺少依赖: langgraph")

    try:
        import langchain
        print(f"  ✅ langchain: {langchain.__version__}")
    except ImportError:
        print("  ❌ langchain: 未安装")
        issues.append("缺少依赖: langchain")
    print()

    # 4. 检查日志目录
    print("4. 检查日志目录")
    if os.path.exists('logs'):
        print(f"  ✅ logs 目录存在")
        # 检查最近的日志文件
        log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
        if log_files:
            print(f"  📄 找到 {len(log_files)} 个日志文件")
    else:
        print(f"  ❌ logs 目录不存在")
        issues.append("缺少日志目录")
    print()

    # 5. 输出诊断结果
    print("=" * 60)
    if issues:
        print("⚠️  发现问题:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
        print("💡 建议修复:")
        print("  1. 配置缺失的环境变量")
        print("  2. 安装缺失的 Python 依赖")
        print("  3. 检查必需文件是否存在")
        return 1
    else:
        print("✅ 未发现明显问题")
        print()
        print("💡 建议操作:")
        print("  1. 查看 GitHub Actions 运行日志")
        print("  2. 检查最近的错误日志")
        print("  3. 手动运行 workflow 测试")
        return 0

if __name__ == "__main__":
    sys.exit(diagnose_issues())
