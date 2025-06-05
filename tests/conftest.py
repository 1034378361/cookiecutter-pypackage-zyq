"""
pytest配置。
"""
import os
import pytest


@pytest.fixture
def cookies_context():
    """测试使用的默认上下文。"""
    return {
        "full_name": "测试用户",
        "email": "test@example.com",
        "github_username": "testuser",
        "project_name": "Python测试项目",
        "project_slug": "python_test",
        "project_short_description": "用于测试的Python项目",
        "version": "0.1.0",
        "python_min_version": "3.8",
        "use_pytest": "y",
        "command_line_interface": "Typer",
        "create_author_file": "y",
        "open_source_license": "MIT license",
    }


def pytest_configure(config):
    """设置测试环境。"""
    # 在CI环境中设置标志
    if os.environ.get("GITHUB_ACTIONS") == "true":
        os.environ["CI"] = "true"
