#!/usr/bin/env python3
"""
自动化系统诊断脚本
检查所有组件是否正常工作
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_python_version():
    """检查 Python 版本"""
    print_section("1. Python 版本检查")
    version = sys.version
    print(f"✅ Python 版本: {version}")
    return True

def check_dependencies():
    """检查依赖包"""
    print_section("2. 依赖包检查")

    required_packages = [
        "langchain",
        "langgraph",
        "pydantic",
        "requests",
        "beautifulsoup4",
        "httpx",
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing.append(package)

    if missing:
        print(f"\n⚠️  缺失的包: {', '.join(missing)}")
        print("💡 运行: pip install -r requirements.txt")
        return False

    return True

def check_workflow_import():
    """检查工作流导入"""
    print_section("3. 工作流导入检查")

    try:
        from graphs.graph import main_graph
        print("✅ 工作流导入成功")
        return True
    except Exception as e:
        print(f"❌ 工作流导入失败: {e}")
        return False

def check_config_files():
    """检查配置文件"""
    print_section("4. 配置文件检查")

    config_files = [
        "src/graphs/graph.py",
        "src/graphs/state.py",
        "src/auto_workflow_with_real_api.py",
        "config/email_generate_llm_cfg.json",
        "requirements.txt",
    ]

    all_exist = True
    for file in config_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 文件不存在")
            all_exist = False

    return all_exist

def check_environment_variables():
    """检查环境变量"""
    print_section("5. 环境变量检查")

    required_env = [
        "SNOVIO_API_TOKEN",
        "SNOVIO_CLIENT_ID",
        "RESEND_API_KEY",
    ]

    all_set = True
    for env in required_env:
        value = os.getenv(env)
        if value:
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print(f"✅ {env} = {masked}")
        else:
            print(f"⚠️  {env} - 未设置（本地运行可能需要）")
            all_set = False

    return all_set

def check_logs_directory():
    """检查日志目录"""
    print_section("6. 日志目录检查")

    logs_dir = "logs"
    if os.path.exists(logs_dir):
        print(f"✅ {logs_dir} 目录存在")
        files = os.listdir(logs_dir)
        print(f"   包含 {len(files)} 个文件")
        return True
    else:
        print(f"⚠️  {logs_dir} 目录不存在")
        return False

def run_quick_test():
    """运行快速测试"""
    print_section("7. 快速功能测试")

    try:
        # 测试工作流导入
        from graphs.graph import main_graph
        from graphs.state import GraphInput

        # 创建测试输入
        test_input = GraphInput(
            target_keywords="测试",
            website_url="https://www.miga.cc"
        )

        print("✅ 测试输入创建成功")
        print("✅ 工作流准备就绪")
        print("\n💡 提示: 可以运行完整测试:")
        print("   cd src && python auto_workflow_with_real_api.py --keywords '测试' --website 'https://www.miga.cc'")

        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "🔍" * 35)
    print("  自动化系统诊断工具")
    print("🔍" * 35)

    results = []

    # 运行所有检查
    results.append(("Python 版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("工作流导入", check_workflow_import()))
    results.append(("配置文件", check_config_files()))
    results.append(("环境变量", check_environment_variables()))
    results.append(("日志目录", check_logs_directory()))
    results.append(("快速测试", run_quick_test()))

    # 生成报告
    print_section("📊 诊断报告")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    print(f"\n📈 总体状态: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有检查通过！系统运行正常。")
        print("\n🚀 下一步:")
        print("   1. 在 GitHub Actions 中测试 workflow")
        print("   2. 查看日志确认运行结果")
        return 0
    else:
        print("\n⚠️  发现问题，请根据上面的提示进行修复。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
