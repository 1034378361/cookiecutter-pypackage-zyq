#!/usr/bin/env python
"""测试CI/CD配置。"""
import yaml
from pathlib import Path

# 导入共用的测试辅助函数
from test_bake_project import bake_in_temp_dir


class TestPreCommit:
    """测试pre-commit配置。"""

    def test_pre_commit_config(self, cookies):
        """测试pre-commit配置文件生成。"""
        # 测试包含pre-commit
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_pre_commit": "y"}
        ) as result:
            precommit_file = result.project_path / ".pre-commit-config.yaml"
            assert precommit_file.exists()
            # 验证YAML格式正确
            config = yaml.safe_load(precommit_file.read_text())
            assert "repos" in config
            # 应该至少有一些常见的hooks
            hook_ids = []
            for repo in config["repos"]:
                for hook in repo.get("hooks", []):
                    hook_ids.append(hook.get("id"))

            # 验证必要的hooks存在
            required_hooks = ["check-yaml", "black", "ruff-check"]
            for hook in required_hooks:
                assert any(h for h in hook_ids if hook in h), f"没有找到预期的hook: {hook}"

        # 测试不包含pre-commit
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_pre_commit": "n"}
        ) as result:
            precommit_file = result.project_path / ".pre-commit-config.yaml"
            assert not precommit_file.exists()


class TestGitHubActions:
    """测试GitHub Actions配置。"""

    def test_github_actions_test_workflow(self, cookies):
        """测试GitHub Actions测试工作流配置。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_github_actions": "y"}
        ) as result:
            test_workflow = result.project_path / ".github" / "workflows" / "test.yml"
            assert test_workflow.exists()

            # 验证YAML格式正确
            config = yaml.safe_load(test_workflow.read_text())
            assert "jobs" in config
            assert "test" in config["jobs"]

            # 验证关键步骤存在
            steps = [s.get("name", "") for s in config["jobs"]["test"]["steps"]]
            assert any("Python" in s for s in steps), "没有找到设置Python的步骤"
            assert any("依赖" in s for s in steps), "没有找到安装依赖的步骤"
            assert any("测试" in s for s in steps), "没有找到运行测试的步骤"

    def test_github_actions_publish_workflow(self, cookies):
        """测试GitHub Actions发布工作流配置。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"include_github_actions": "y"}
        ) as result:
            publish_workflow = result.project_path / ".github" / "workflows" / "publish.yml"
            assert publish_workflow.exists()

            # 验证YAML格式正确
            config = yaml.safe_load(publish_workflow.read_text())
            assert "jobs" in config
            assert "deploy" in config["jobs"]

            # 验证触发条件包含标签
            assert "tags" in config.get("on", {}).get("push", {})

            # 验证关键步骤存在
            steps = []
            for job in config["jobs"].values():
                for step in job.get("steps", []):
                    steps.append(step.get("name", ""))

            assert any("构建" in s for s in steps), "没有找到构建包的步骤"
            assert any("PyPI" in s for s in steps), "没有找到发布到PyPI的步骤"


class TestCoverageConfig:
    """测试覆盖率配置。"""

    def test_coverage_config(self, cookies):
        """测试覆盖率配置。"""
        with bake_in_temp_dir(
            cookies,
            extra_context={"use_pytest": "y"}
        ) as result:
            pyproject_file = result.project_path / "pyproject.toml"
            content = pyproject_file.read_text()

            # 验证覆盖率配置存在
            assert "coverage.report" in content
            assert "fail_under" in content

            # 验证各工作流中的覆盖率阈值
            if (result.project_path / ".github" / "workflows" / "test.yml").exists():
                test_workflow = result.project_path / ".github" / "workflows" / "test.yml"
                workflow_content = test_workflow.read_text()
                assert "--cov-fail-under" in workflow_content
