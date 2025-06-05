"""
pytest配置文件，为cookiecutter-pypackage模板测试提供支持。
"""
import os
import shutil
import pytest
import subprocess
from pathlib import Path


@pytest.fixture
def cookies_context():
    """默认的cookiecutter上下文。"""
    return {
        "full_name": "测试用户",
        "email": "test@example.com",
        "github_username": "testuser",
        "project_name": "Python测试项目",
        "project_slug": "python_test",
        "project_short_description": "用于测试的Python项目",
        "pypi_username": "testuser",
        "version": "0.1.0",
        "python_min_version": "3.8",
        "use_pytest": "y",
        "include_github_actions": "y",
        "include_pre_commit": "y",
        "include_changelog_gen": "y",
        "include_devcontainer": "y",
        "include_dependabot": "y",
        "include_docker": "y",
        "command_line_interface": "Typer",
        "create_author_file": "y",
        "open_source_license": "MIT license",
        "dependency_rich": "y",
        "dependency_pyyaml": "y",
        "include_utils_lib": "y",
        "include_version_management": "y",
    }


def pytest_configure(config):
    """pytest配置函数。"""
    # 在CI环境中设置标志
    if os.environ.get("GITHUB_ACTIONS") == "true":
        os.environ["CI"] = "true"

    # 检查必要的命令是否可用
    _check_commands()


def _check_commands():
    """检查测试所需的命令是否可用。"""
    required_commands = []

    # 如果测试在非Windows平台上运行，检查make是否可用
    if not os.name == 'nt':  # 非Windows系统
        required_commands.append('make')

    for cmd in required_commands:
        if not shutil.which(cmd):
            pytest.skip(f"命令 {cmd} 不可用，相关测试将被跳过", allow_module_level=True)


@pytest.fixture
def git_mock(monkeypatch):
    """模拟git命令，用于测试版本管理功能。"""
    def mock_run(*args, **kwargs):
        # 模拟subprocess.run函数的返回
        class MockCompletedProcess:
            def __init__(self, returncode=0, stdout="", stderr=""):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        # 模拟git describe命令
        if 'describe' in args[0]:
            return MockCompletedProcess(stdout='v0.1.0')
        # 模拟git rev-parse命令
        elif 'rev-parse' in args[0]:
            return MockCompletedProcess(stdout='abc123')
        # 其他git命令
        else:
            return MockCompletedProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)
    return mock_run
