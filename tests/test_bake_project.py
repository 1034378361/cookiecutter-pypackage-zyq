#!/usr/bin/env python
"""测试cookiecutter-pypackage模板的核心功能。"""
import os
import sys
import subprocess
from pathlib import Path
import pytest
from contextlib import contextmanager
from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """
    在指定目录内执行代码块，然后返回到前一个工作目录。
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    在临时目录中创建项目，并提供进入项目目录的上下文管理器。
    在CI环境中保留临时目录用于调试，本地环境自动清理。
    """
    result = cookies.bake(*args, **kwargs)
    if result.exception is not None:
        # 如果bake出错，直接抛出异常，而不是返回失败的结果
        raise result.exception

    try:
        yield result
    finally:
        if os.environ.get('CI') != 'true':  # 仅在非CI环境中清理
            rmtree(str(result.project_path))


def run_command(command, cwd=None):
    """运行shell命令并返回结果"""
    return subprocess.run(
        command,
        shell=True,
        check=False,  # 不自动抛出异常
        capture_output=True,
        text=True,
        cwd=cwd
    )


class TestBasicFunctionality:
    """测试模板的基本功能。"""

    def test_project_directory_structure(self, cookies):
        """测试生成项目的目录结构。"""
        with bake_in_temp_dir(cookies) as result:
            # 核心目录和文件必须存在
            assert result.project_path.is_dir()
            assert (result.project_path / "src").is_dir()
            assert (result.project_path / "tests").is_dir()
            assert (result.project_path / "docs").is_dir()
            assert (result.project_path / "pyproject.toml").is_file()
            assert (result.project_path / "README.md").is_file()

    def test_python_version_config(self, cookies):
        """测试Python版本配置正确应用于所有相关文件。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"python_min_version": "3.9"}
        ) as result:
            # 检查pyproject.toml中的Python版本设置
            pyproject_content = (result.project_path / "pyproject.toml").read_text()
            assert 'python = ">=3.9"' in pyproject_content
            # 检查Dockerfile中的Python版本
            dockerfile_content = (result.project_path / "Dockerfile").read_text()
            assert 'FROM python:3.9-slim-bookworm' in dockerfile_content

    def test_license_generation(self, cookies):
        """测试许可证文件正确生成。"""
        # 测试MIT许可证
        with bake_in_temp_dir(
            cookies,
            extra_context={"open_source_license": "MIT license"}
        ) as result:
            license_file = result.project_path / "LICENSE"
            assert license_file.is_file()
            content = license_file.read_text()
            assert "MIT License" in content

        # 测试BSD许可证
        with bake_in_temp_dir(
            cookies,
            extra_context={"open_source_license": "BSD license"}
        ) as result:
            license_file = result.project_path / "LICENSE"
            assert license_file.is_file()
            content = license_file.read_text()
            assert "BSD " in content

    def test_no_license_option(self, cookies):
        """测试选择不开源时LICENSE文件不存在。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"open_source_license": "Not open source"}
        ) as result:
            assert not (result.project_path / "LICENSE").exists()

    def test_python_version_selection(self, cookies):
        """测试Python版本选择功能。"""
        # 测试选择特定Python版本
        with bake_in_temp_dir(
            cookies,
            extra_context={"python_version": "3.10"}
        ) as result:
            # 检查.python-version文件
            python_version_file = result.project_path / ".python-version"
            assert python_version_file.exists()
            assert "3.10" in python_version_file.read_text()

            # 检查pyproject.toml中的Python版本设置
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert 'py310' in content  # 在配置中使用的Python版本

            # 检查工作流文件中的版本列表
            workflows_dir = result.project_path / ".github" / "workflows"
            if workflows_dir.exists():
                test_workflow = workflows_dir / "test.yml"
                if test_workflow.exists():
                    workflow_content = test_workflow.read_text()
                    assert '"3.10"' in workflow_content  # 确保版本在矩阵中


class TestProjectConfiguration:
    """测试项目配置选项。"""

    def test_cli_options(self, cookies):
        """测试CLI选项正确应用。"""
        # 测试无CLI接口
        with bake_in_temp_dir(
            cookies,
            extra_context={"command_line_interface": "No command-line interface"}
        ) as result:
            assert not (result.project_path / "src" / "python_test" / "cli.py").exists()

        # 测试Typer CLI接口
        with bake_in_temp_dir(
            cookies,
            extra_context={
                "command_line_interface": "Typer",
                "project_slug": "cli_test"
            }
        ) as result:
            cli_file = result.project_path / "src" / "cli_test" / "cli.py"
            assert cli_file.exists()
            assert "import typer" in cli_file.read_text()

        # 测试Argparse CLI接口
        with bake_in_temp_dir(
            cookies,
            extra_context={
                "command_line_interface": "Argparse",
                "project_slug": "arg_test"
            }
        ) as result:
            cli_file = result.project_path / "src" / "arg_test" / "cli.py"
            assert cli_file.exists()
            assert "import argparse" in cli_file.read_text()

    def test_dependency_options(self, cookies):
        """测试可选依赖正确应用。"""
        # 测试包含Rich
        with bake_in_temp_dir(
            cookies,
            extra_context={"dependency_rich": "y"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            # 支持不同包管理器的依赖格式
            assert ('rich = ">=' in content or  # Poetry格式
                   '"rich>=' in content)        # PDM格式

        # 测试不包含Rich
        with bake_in_temp_dir(
            cookies,
            extra_context={"dependency_rich": "n"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert 'rich' not in content

        # 测试包含PyYAML
        with bake_in_temp_dir(
            cookies,
            extra_context={"dependency_pyyaml": "y"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert ('pyyaml = ">=' in content or  # Poetry格式
                   '"pyyaml>=' in content)       # PDM格式

        # 测试不包含PyYAML
        with bake_in_temp_dir(
            cookies,
            extra_context={"dependency_pyyaml": "n"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert 'pyyaml' not in content and 'PyYAML' not in content

    def test_package_manager_options(self, cookies):
        """测试包管理器选项正确应用。"""
        # 测试选择Poetry
        with bake_in_temp_dir(
            cookies,
            extra_context={"package_manager": "Poetry"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert '[tool.poetry]' in content
            assert 'poetry-core' in content

            # 检查Makefile是否使用poetry命令
            makefile = result.project_path / "Makefile"
            makefile_content = makefile.read_text()
            assert 'poetry run' in makefile_content

        # 测试选择PDM
        with bake_in_temp_dir(
            cookies,
            extra_context={"package_manager": "PDM"}
        ) as result:
            pyproject = result.project_path / "pyproject.toml"
            content = pyproject.read_text()
            assert '[project]' in content
            assert 'pdm-backend' in content

            # 检查Makefile是否使用pdm命令
            makefile = result.project_path / "Makefile"
            makefile_content = makefile.read_text()
            assert 'pdm run' in makefile_content


class TestGitHubIntegration:
    """测试GitHub集成功能。"""

    def test_github_actions_configuration(self, cookies):
        """测试GitHub Actions配置。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_github_actions": "y"}
        ) as result:
            actions_dir = result.project_path / ".github" / "workflows"
            assert actions_dir.is_dir()
            assert (actions_dir / "test.yml").is_file()
            assert (actions_dir / "publish.yml").is_file()

        with bake_in_temp_dir(
            cookies,
            extra_context={"include_github_actions": "n"}
        ) as result:
            actions_dir = result.project_path / ".github" / "workflows"
            assert not actions_dir.exists()

    def test_dependabot_configuration(self, cookies):
        """测试Dependabot配置。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_dependabot": "y"}
        ) as result:
            dependabot_file = result.project_path / ".github" / "dependabot.yml"
            assert dependabot_file.is_file()

        with bake_in_temp_dir(
            cookies,
            extra_context={"include_dependabot": "n"}
        ) as result:
            dependabot_file = result.project_path / ".github" / "dependabot.yml"
            assert not dependabot_file.exists()


class TestDockerSupport:
    """测试Docker支持。"""

    def test_dockerfile_generation(self, cookies):
        """测试Dockerfile生成。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_docker": "y"}
        ) as result:
            dockerfile = result.project_path / "Dockerfile"
            compose_file = result.project_path / "docker-compose.yml"
            assert dockerfile.is_file()
            assert compose_file.is_file()

        with bake_in_temp_dir(
            cookies,
            extra_context={"include_docker": "n"}
        ) as result:
            dockerfile = result.project_path / "Dockerfile"
            compose_file = result.project_path / "docker-compose.yml"
            assert not dockerfile.exists()
            assert not compose_file.exists()


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Make不支持Windows")
class TestMakeCommands:
    """测试Makefile命令（Unix环境）。"""

    def test_make_help(self, cookies):
        """测试make help命令。"""
        with bake_in_temp_dir(cookies) as result:
            with inside_dir(str(result.project_path)):
                output = run_command("make help")
                assert output.returncode == 0
                # 检查是否包含任意常见的目标，而不是寻找"help"文本
                assert "clean" in output.stdout or "lint" in output.stdout or "test" in output.stdout


class TestUtilsLibrary:
    """测试工具库功能。"""

    def test_utils_library_option(self, cookies):
        """测试工具库选项。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_utils_lib": "y", "project_slug": "with_utils"}
        ) as result:
            utils_dir = result.project_path / "src" / "with_utils" / "utils"
            assert utils_dir.is_dir()
            assert (utils_dir / "file_utils.py").is_file()

        with bake_in_temp_dir(
            cookies,
            extra_context={"include_utils_lib": "n", "project_slug": "no_utils"}
        ) as result:
            utils_dir = result.project_path / "src" / "no_utils" / "utils"
            assert not utils_dir.exists()

