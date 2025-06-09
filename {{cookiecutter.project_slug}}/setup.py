#!/usr/bin/env python3
"""
统一项目安装脚本 - 跨平台(Windows, macOS, Linux)版本

这个脚本提供以下功能:
1. 检测操作系统并打印环境信息
2. 创建和管理Python虚拟环境
3. 安装项目依赖(基础版或开发版)
4. 配置开发环境(git hooks, 工具链等)

设计原则:
- 最小依赖: 仅依赖Python标准库和pip
- 跨平台: 自动适配不同操作系统
- 无提示默认模式: 支持CI/CD环境使用
"""
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path

# 颜色代码
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
NC = '\033[0m'  # 无颜色

# 项目根目录(当前脚本所在目录)
PROJECT_ROOT = Path(__file__).parent.absolute()
VENV_PATH = PROJECT_ROOT / ".venv"

def should_use_color():
    """判断当前环境是否支持彩色输出."""
    # Windows可能需要通过环境变量或检测特定终端来判断
    if platform.system() == "Windows":
        # 检测是否在PowerShell或者启用了ANSI的cmd中
        return "WT_SESSION" in os.environ or "TERM" in os.environ or os.environ.get("ANSICON", "")
    return True

def print_color(message, color=GREEN):
    """输出彩色信息."""
    if should_use_color():
        print(f"{color}{message}{NC}")
    else:
        print(message)

def run_command(cmd, check=True, shell=True, cwd=None):
    """运行系统命令并返回结果."""
    try:
        print_color(f"执行命令: {cmd}", BLUE)

        # Windows特殊处理
        if platform.system() == "Windows" and isinstance(cmd, str):
            # 确保在Windows上也能正常运行复杂命令
            shell = True

        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            text=True,
            capture_output=True,
            cwd=cwd or PROJECT_ROOT
        )
        if result.stdout and result.stdout.strip():
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print_color(f"命令失败: {cmd}", RED)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print_color(f"错误: {e.stderr}", RED)
        if not check:
            return e
        sys.exit(1)

def is_venv_exists():
    """检查虚拟环境是否存在."""
    return VENV_PATH.exists()

def get_venv_python():
    """获取虚拟环境中Python解释器路径."""
    if platform.system() == "Windows":
        python_path = VENV_PATH / "Scripts" / "python.exe"
    else:
        python_path = VENV_PATH / "bin" / "python"

    return str(python_path) if python_path.exists() else None

def create_venv():
    """创建虚拟环境."""
    if is_venv_exists():
        print_color("虚拟环境已存在，跳过创建", YELLOW)
        return True

    try:
        print_color("创建虚拟环境...", GREEN)
        venv.create(VENV_PATH, with_pip=True)

        # 升级pip
        python_path = get_venv_python()
        run_command(f'"{python_path}" -m pip install --upgrade pip')

        print_color("虚拟环境创建成功！", GREEN)
        return True
    except Exception as e:
        print_color(f"创建虚拟环境失败: {e}", RED)
        return False

def install_dependencies(dev=False):
    """安装项目依赖."""
    python_path = get_venv_python()
    if not python_path:
        print_color("虚拟环境不存在，请先创建虚拟环境", RED)
        return False

    print_color(f"安装{'开发' if dev else '基础'}依赖...", GREEN)

    try:
        # 使用PDM或直接使用pip
        pdm_installed = shutil.which("pdm")
        if pdm_installed:
            run_command("pdm install" + (" -G dev" if dev else ""))
        else:
            extras = "[dev]" if dev else ""
            run_command(f'"{python_path}" -m pip install -e .{extras}')

        print_color("依赖安装完成！", GREEN)
        return True
    except Exception as e:
        print_color(f"安装依赖失败: {e}", RED)
        return False

def setup_dev_environment():
    """配置开发环境."""
    python_path = get_venv_python()
    if not python_path:
        print_color("虚拟环境不存在，请先创建虚拟环境", RED)
        return False

    print_color("配置开发环境...", GREEN)

    # 安装pre-commit钩子
    pre_commit_config = PROJECT_ROOT / ".pre-commit-config.yaml"
    if pre_commit_config.exists():
        run_command(f'"{python_path}" -m pip install pre-commit')
        # 使用Python路径直接运行避免shell兼容性问题
        run_command(f'"{python_path}" -m pre_commit install')

    print_color("开发环境配置完成！", GREEN)
    return True

def print_activation_help():
    """打印虚拟环境激活帮助信息."""
    venv_path = VENV_PATH

    if platform.system() == "Windows":
        activate_path = venv_path / "Scripts" / "activate"
        print_color("\n激活虚拟环境:", BLUE)
        print_color(f"    {venv_path}\\Scripts\\activate", YELLOW)
        print_color("或在PowerShell中:", BLUE)
        print_color(f"    . {venv_path}\\Scripts\\Activate.ps1", YELLOW)
    else:
        activate_path = venv_path / "bin" / "activate"
        print_color("\n激活虚拟环境:", BLUE)
        print_color(f"    source {activate_path}", YELLOW)

def print_next_steps():
    """打印后续步骤说明."""
    print_color("\n=== 后续步骤 ===", GREEN)
    print_activation_help()
    print_color("\n开发常用命令:", BLUE)
    print_color("    make lint      # 运行代码检查", YELLOW)
    print_color("    make test      # 运行测试", YELLOW)
    print_color("    make docs      # 生成文档", YELLOW)

def main():
    """主函数."""
    # 检测系统信息
    system = platform.system()
    python_version = platform.python_version()
    print_color(f"系统信息:", GREEN)
    print_color(f"  操作系统: {system} ({platform.platform()})", GREEN)
    print_color(f"  Python版本: {python_version}", GREEN)
    print()

    # 命令行参数处理
    args = sys.argv[1:]
    auto_mode = "--yes" in args or "-y" in args
    dev_mode = "--dev" in args or "-d" in args

    # 创建虚拟环境
    if auto_mode or input("创建虚拟环境? (y/n): ").lower() == "y":
        if not create_venv():
            return 1

    # 安装依赖
    if auto_mode or input("安装项目依赖? (y/n): ").lower() == "y":
        if not install_dependencies(dev=dev_mode):
            return 1

    # 配置开发环境
    if dev_mode and (auto_mode or input("配置开发环境? (y/n): ").lower() == "y"):
        if not setup_dev_environment():
            return 1

    # 打印后续步骤
    print_next_steps()
    return 0

if __name__ == "__main__":
    sys.exit(main())
