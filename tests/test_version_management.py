#!/usr/bin/env python
"""测试版本管理功能。"""
import os
import sys
import importlib.util
from pathlib import Path
import pytest

# 导入共用的测试辅助函数
from test_bake_project import bake_in_temp_dir, inside_dir


class TestVersionManagement:
    """测试版本管理功能。"""

    def test_version_module_generation(self, cookies):
        """测试版本管理模块的生成。"""
        # 测试包含版本管理功能
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_version_management": "y", "project_slug": "version_test"}
        ) as result:
            version_file = result.project_path / "src" / "version_test" / "_version.py"
            assert version_file.exists()
            assert "get_version" in version_file.read_text()

        # 测试不包含版本管理功能
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_version_management": "n", "project_slug": "no_version_test"}
        ) as result:
            version_file = result.project_path / "src" / "no_version_test" / "_version.py"
            assert not version_file.exists()
            # 在不包含版本管理时，应该直接在__init__.py中定义版本
            init_file = result.project_path / "src" / "no_version_test" / "__init__.py"
            init_content = init_file.read_text()
            assert "__version__ = " in init_content
            assert "from ._version import" not in init_content

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Unix路径处理")
    def test_version_import(self, cookies, git_mock):
        """测试版本导入功能。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_version_management": "y", "project_slug": "version_import_test"}
        ) as result:
            # 尝试导入版本模块
            with inside_dir(str(result.project_path)):
                # 动态导入版本模块
                module_path = result.project_path / "src" / "version_import_test" / "_version.py"
                spec = importlib.util.spec_from_file_location("_version", module_path)
                version_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(version_module)

                # 测试版本获取函数
                version = version_module.get_version()
                assert isinstance(version, str)
                assert version == "0.1.0"  # 默认版本

                # 测试带有commit hash的版本
                version_with_commit = version_module.get_version(with_commit=True)
                assert '+' in version_with_commit  # 应包含commit hash

    def test_version_environment_override(self, cookies, git_mock, monkeypatch):
        """测试环境变量覆盖版本功能。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_version_management": "y", "project_slug": "env_version_test"}
        ) as result:
            # 设置环境变量
            monkeypatch.setenv("ENV_VERSION_TEST_VERSION", "1.2.3")

            # 动态导入版本模块
            module_path = result.project_path / "src" / "env_version_test" / "_version.py"
            spec = importlib.util.spec_from_file_location("_version", module_path)
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)

            # 测试环境变量覆盖
            version = version_module.get_version()
            assert version == "1.2.3"  # 应该使用环境变量的版本
