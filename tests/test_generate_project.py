"""测试模板能否正常生成项目。

此测试模块验证cookiecutter模板能否正确生成项目，并检查关键文件和结构。
"""

import os
import shutil
from pathlib import Path
import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def cleanup():
    """测试结束后清理生成的测试项目。"""
    yield
    # 测试后清理
    if os.path.exists("测试项目"):
        shutil.rmtree("测试项目")
    if os.path.exists("test_project"):
        shutil.rmtree("test_project")


def test_bake_project(cleanup):
    """测试基本项目生成功能。"""
    result = cookiecutter(
        template=".",
        no_input=True,
        extra_context={
            "project_name": "测试项目",
            "project_slug": "test_project",
            "full_name": "测试用户",
            "email": "test@example.com",
            "github_username": "testuser",
            "version": "0.1.0",
            "use_pytest": "y",
            "command_line_interface": "Typer",
            "create_author_file": "y",
            "open_source_license": "MIT license",
        },
    )

    # 验证项目是否成功生成
    assert os.path.isdir(result)

    # 检查生成的关键文件
    expected_files = [
        "README.md",
        "pyproject.toml",
        "src/test_project/__init__.py",
        "tests/__init__.py",
        "tests/test_test_project.py",
    ]

    for file in expected_files:
        file_path = os.path.join(result, file)
        assert os.path.exists(file_path), f"{file} 未生成"


def test_project_directory_structure(cleanup):
    """测试生成的项目目录结构是否符合预期。"""
    result = cookiecutter(
        template=".",
        no_input=True,
        extra_context={"project_slug": "test_project"},
    )

    # 验证目录结构
    expected_directories = [
        "src/test_project",
        "tests",
        "docs",
    ]

    for directory in expected_directories:
        dir_path = os.path.join(result, directory)
        assert os.path.isdir(dir_path), f"{directory} 目录未生成"


def test_cli_functionality(cleanup):
    """测试CLI选项是否正确配置。"""
    # 测试选择CLI选项时
    result = cookiecutter(
        template=".",
        no_input=True,
        extra_context={
            "project_slug": "test_project",
            "command_line_interface": "Typer"
        },
    )

    # 验证CLI文件生成
    cli_file = os.path.join(result, "src/test_project/cli.py")
    assert os.path.exists(cli_file), "CLI文件未生成"

    # 验证pyproject.toml中包含CLI配置
    pyproject_file = os.path.join(result, "pyproject.toml")
    with open(pyproject_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "typer" in content, "typer依赖未在pyproject.toml中配置"