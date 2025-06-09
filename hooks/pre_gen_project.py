#!/usr/bin/env python
import re
import sys
import os
import platform
import shutil
import subprocess
from pathlib import Path


def print_colored(message, color="reset"):
    """打印彩色文本"""
    colors = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m"
    }
    print(f"{colors.get(color, colors['reset'])}{message}{colors['reset']}")


def error(message):
    """打印错误消息并退出进程"""
    print_colored(f"错误: {message}", "red")
    sys.exit(1)


def warning(message):
    """打印警告消息"""
    print_colored(f"警告: {message}", "yellow")


def success(message):
    """打印成功消息"""
    print_colored(f"成功: {message}", "green")


def info(message):
    """打印信息消息"""
    print_colored(f"信息: {message}", "blue")


def validate_project_slug():
    """验证项目标识符是否符合Python模块命名规范"""
    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
    module_name = '{{ cookiecutter.project_slug}}'

    if not re.match(MODULE_REGEX, module_name):
        error(f"项目标识符 '{module_name}' 不是有效的Python模块名。")
        error("请使用下划线(_)替代连字符(-)，并确保以字母开头。")
    else:
        info(f"项目标识符 '{module_name}' 验证通过。")


def validate_project_name():
    """验证项目名称是否包含特殊字符"""
    project_name = '{{ cookiecutter.project_name }}'
    if re.search(r'[^\w\s-]', project_name):
        warning(f"项目名称 '{project_name}' 包含特殊字符，可能导致某些工具或平台出现问题。")
    else:
        info(f"项目名称 '{project_name}' 验证通过。")


def check_target_directory():
    """检查目标目录是否已存在"""
    module_name = '{{ cookiecutter.project_slug}}'
    target_dir = Path(os.getcwd()) / module_name
    if target_dir.exists():
        warning(f"目标目录 '{target_dir}' 已存在。项目生成可能会覆盖现有文件。")


def check_python_environment():
    """检查Python环境"""
    try:
        python_command = 'python' if platform.system() == 'Windows' else 'python3'
        python_version_str = subprocess.check_output(
            [python_command, '--version'],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        ).strip()
        info(f"检测到Python版本: {python_version_str}")
        return python_command
    except (subprocess.SubprocessError, FileNotFoundError):
        warning("无法检测本地Python版本，请确保您的环境中安装了Python。")
        return None


def validate_python_version():
    """验证选择的Python版本是否符合最低要求"""
    selected_version = "{{ cookiecutter.python_version }}"
    # 处理列表类型的版本选择
    if isinstance(selected_version, list):
        info(f"从版本列表中选择的Python版本: {', '.join(selected_version)}")
        selected_version = selected_version[0]  # 取第一个作为默认值
    
    # 最低版本设为3.8
    min_version = "3.8"
    
    try:
        # 将版本字符串转换为元组以便比较
        min_version_tuple = tuple(map(int, min_version.split('.')))
        selected_version_tuple = tuple(map(int, str(selected_version).split('.')))

        if selected_version_tuple < min_version_tuple:
            error(f"选择的Python版本 {selected_version} 低于最小版本要求 {min_version}。")
            error("请选择更高版本。")
        else:
            info(f"选择的Python版本 {selected_version} 符合要求。")
    except ValueError:
        warning(f"无法验证Python版本 (最小: {min_version}，已选: {selected_version})。")
        warning("请确保选择的版本不低于最小版本要求。")


def check_project_type_requirements(python_command):
    """根据项目类型检查相关要求"""
    project_type = "{{ cookiecutter.project_type }}"
    cli_type = "{{ cookiecutter.command_line_interface }}"
    
    info(f"项目类型: {project_type}")
    
    if project_type == "CLI Tool":
        info(f"CLI工具项目，选择的CLI框架: {cli_type}")
        if cli_type == "No command-line interface":
            warning("CLI工具项目通常应该包含命令行接口。您选择了不使用命令行接口，请确认这符合您的需求。")
        
        if cli_type == "Typer" and python_command:
            try:
                subprocess.check_call(
                    [python_command, '-c', 'import typer'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                info("Typer库已安装在当前环境中。")
            except subprocess.SubprocessError:
                warning("未检测到Typer库。项目生成后，您需要安装它: pip install typer")

    elif project_type == "Web Service":
        info("Web服务项目验证...")
        # 可以在这里添加Web服务项目特有的检查
    
    elif project_type == "Data Science":
        info("数据科学项目验证...")
        # 可以在这里添加数据科学项目特有的检查


def check_git_availability():
    """检查Git是否可用"""
    try:
        git_version = subprocess.check_output(
            ['git', '--version'],
            universal_newlines=True,
            stderr=subprocess.DEVNULL
        ).strip()
        info(f"检测到Git: {git_version}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        warning("未检测到Git。建议安装Git进行版本控制。")
        warning("Git下载地址: https://git-scm.com/downloads")
        return False


def check_license_choice():
    """检查许可证选择"""
    license_choice = "{{ cookiecutter.open_source_license }}"
    if license_choice == "Not open source":
        warning("您选择了不使用开源许可证。请确保了解这对代码分发的影响。")
    else:
        info(f"已选择开源许可证: {license_choice}")


def check_required_tools():
    """检查其他必要工具的可用性"""
    # 检查make命令 (在Windows上不常用，但在Unix系统上常用)
    if platform.system() != 'Windows':
        try:
            subprocess.check_call(['make', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            info("检测到make工具可用。")
        except (subprocess.SubprocessError, FileNotFoundError):
            warning("未检测到make工具。部分项目命令可能无法使用。")
    
    # 检查PDM可用性
    try:
        pdm_version = subprocess.check_output(['pdm', '--version'], universal_newlines=True, stderr=subprocess.DEVNULL).strip()
        info(f"检测到PDM: {pdm_version}")
    except (subprocess.SubprocessError, FileNotFoundError):
        warning("未检测到PDM包管理器。项目依赖管理将需要PDM。")
        warning("PDM安装指南: https://pdm.fming.dev/latest/#installation")


if __name__ == '__main__':
    print_colored("\n==================== 项目前置验证 ====================", "cyan")
    
    # 验证项目名称和标识符
    validate_project_slug()
    validate_project_name()
    
    # 检查目标目录
    check_target_directory()
    
    # 检查Python环境
    python_command = check_python_environment()
    
    # 验证Python版本
    validate_python_version()
    
    # 检查项目类型要求
    check_project_type_requirements(python_command)
    
    # 检查Git可用性
    check_git_availability()
    
    # 检查许可证选择
    check_license_choice()
    
    # 检查其他必要工具
    check_required_tools()
    
    print_colored("\n==================== 验证完成 ====================", "green")
    success("项目前置验证通过！即将开始生成项目...")
    print("")
