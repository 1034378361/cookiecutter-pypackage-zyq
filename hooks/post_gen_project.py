#!/usr/bin/env python
import os
import pathlib
import re
import stat

# 确保.gitattributes在Windows和Unix系统上都使用正确的行尾规范
def normalize_gitattributes():
    """确保.gitattributes文件使用规范的行尾。"""
    gitattributes = pathlib.Path('.gitattributes')
    if gitattributes.exists():
        # 读取内容
        content = gitattributes.read_text()
        # 替换所有换行符为LF (Unix风格)
        content = content.replace('\r\n', '\n')
        # 重写文件
        gitattributes.write_text(content)
        print("已规范化 .gitattributes 行尾")


# def restore_mkdocs_syntax():
#     """恢复MkDocs特殊语法，将HTML注释替换回原始语法。"""
#     # 要处理的文件列表
#     files_to_process = [
#         pathlib.Path('docs', 'history.md'),
#         pathlib.Path('docs', 'contributing.md'),
#         pathlib.Path('docs', 'api', 'index.md'),
#         pathlib.Path('docs', '_includes', 'history.md'),
#         pathlib.Path('docs', '_includes', 'contributing.md'),
#         pathlib.Path('docs', '_includes', 'index.md'),
#         pathlib.Path('docs', '_includes', 'changelog.md')
#     ]

#     # 替换模式
#     include_markdown_pattern = re.compile(
#         r'<!--\s*.*此处.*include-markdown\s*"([^"]+)".*\s*-->'
#     )

#     # 处理每个文件
#     for file_path in files_to_process:
#         if file_path.exists():
#             content = file_path.read_text()

#             # 替换include-markdown注释
#             content = include_markdown_pattern.sub(
#                 r'{% raw %}{{%\n  include-markdown "\1"\n%}}{% endraw %}',
#                 content
#             )


#             # 替换API文档中的:::注释
#             if 'api' in str(file_path):
#                 content = re.sub(
#                     r'<!--\s*.*此处.*MkDocs插件显示.*API文档:?\s*:::\s*([^\n]+)\s*-->',
#                     r'::: \1',
#                     content
#                 )

#             # 写入修改后的内容
#             file_path.write_text(content)
#             print(f"已恢复MkDocs语法: {file_path}")


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        pathlib.Path('AUTHORS.rst').unlink()
        pathlib.Path('docs', 'authors.rst').unlink()

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'cli.py').unlink()

    if '{{ cookiecutter.open_source_license }}' == 'Not open source':
        pathlib.Path('LICENSE').unlink()

    # 处理测试覆盖率配置
    if '{{ cookiecutter.use_pytest }}' != 'y':
        # 如果不使用pytest，移除pytest覆盖率配置
        pyproject_file = pathlib.Path('pyproject.toml')
        if pyproject_file.exists():
            content = pyproject_file.read_text()

            # 移除pytest.ini_options中的覆盖率相关配置
            lines = content.splitlines()
            filtered_lines = []
            skip_line = False
            for line in lines:
                if "# 测试覆盖率配置" in line:
                    skip_line = True
                elif skip_line and not line.strip().startswith('[tool.'):
                    continue
                elif skip_line and line.strip().startswith('[tool.'):
                    skip_line = False

                # 移除coverage.report部分
                if line.strip() == "[tool.coverage.report]":
                    skip_line = True
                elif skip_line and any(line.strip().startswith(x) for x in ["[tool.", "exclude_lines ="]):
                    skip_line = False

                if not skip_line:
                    filtered_lines.append(line)

            pyproject_file.write_text("\n".join(filtered_lines))

            # 如果有测试相关的GitHub Actions工作流，移除覆盖率配置
            test_workflow = pathlib.Path('.github', 'workflows', 'test.yml')
            if test_workflow.exists():
                content = test_workflow.read_text()
                content = content.replace('--cov=src --cov-report=term --cov-report=xml --cov-fail-under=85', '')
                test_workflow.write_text(content)
    else:
        # 使用pytest时，确保覆盖率阈值统一设置为85%
        coverage_threshold = "85"  # 默认覆盖率阈值

        # 更新tox.ini中的覆盖率阈值
        tox_file = pathlib.Path('tox.ini')
        if tox_file.exists():
            content = tox_file.read_text()
            content = re.sub(
                r'--cov-fail-under=\d+',
                f'--cov-fail-under={coverage_threshold}',
                content
            )
            tox_file.write_text(content)

        # 更新Makefile中的覆盖率阈值
        makefile = pathlib.Path('Makefile')
        if makefile.exists():
            content = makefile.read_text()
            content = re.sub(
                r'--cov-fail-under=\d+',
                f'--cov-fail-under={coverage_threshold}',
                content
            )
            makefile.write_text(content)

        # 更新pyproject.toml中的覆盖率阈值
        pyproject_file = pathlib.Path('pyproject.toml')
        if pyproject_file.exists():
            content = pyproject_file.read_text()
            content = re.sub(
                r'fail_under = \d+',
                f'fail_under = {coverage_threshold}',
                content
            )
            pyproject_file.write_text(content)

        # 更新GitHub Actions工作流中的覆盖率阈值
        test_workflow = pathlib.Path('.github', 'workflows', 'test.yml')
        if test_workflow.exists():
            content = test_workflow.read_text()
            content = re.sub(
                r'--cov-fail-under=\d+',
                f'--cov-fail-under={coverage_threshold}',
                content
            )
            test_workflow.write_text(content)

    # 根据选项决定是否保留工具函数库
    if '{{ cookiecutter.include_utils_lib }}' != 'y':
        utils_dir = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'utils')
        if utils_dir.exists():
            for file in utils_dir.glob('*.py'):
                file.unlink()
            utils_dir.rmdir()

    # 根据选项决定是否保留版本管理功能
    if '{{ cookiecutter.include_version_management }}' != 'y':
        version_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', '_version.py')
        if version_file.exists():
            version_file.unlink()

        # 修改__init__.py文件，使用简单的版本定义
        init_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', '__init__.py')
        content = init_file.read_text()
        content = content.replace(
            "# 版本管理\nfrom ._version import get_version\n__version__ = get_version()",
            "__version__ = '{{ cookiecutter.version }}'"
        )
        init_file.write_text(content)

    # 如果不使用GitHub Actions，移除相关文件
    if '{{ cookiecutter.include_github_actions }}' != 'y':
        workflows_dir = pathlib.Path('.github', 'workflows')
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob('*.yml'):
                workflow_file.unlink()
            workflows_dir.rmdir()

            # 如果.github目录为空，也删除
            github_dir = pathlib.Path('.github')
            if not any(github_dir.iterdir()):
                github_dir.rmdir()
    else:
        # 如果使用GitHub Actions，则移除Travis CI配置
        travis_file = pathlib.Path('.travis.yml')
        if travis_file.exists():
            travis_file.unlink()

    # 如果不使用pre-commit，移除相关文件
    if '{{ cookiecutter.include_pre_commit }}' != 'y':
        precommit_file = pathlib.Path('.pre-commit-config.yaml')
        if precommit_file.exists():
            precommit_file.unlink()

        # 移除pyproject.toml中的pre-commit相关配置
        pyproject_file = pathlib.Path('pyproject.toml')
        if pyproject_file.exists():
            content = pyproject_file.read_text()

            # 移除pre-commit相关依赖
            content = content.replace('"pre-commit>=3.6.0",  # git hooks\n', '')
            content = content.replace('"pydocstyle",  # docstring style checking\n', '')
            content = content.replace('"bandit>=1.8.3",  # security checks\n', '')
            content = content.replace('"types-PyYAML",  # PyYAML类型提示\n', '')

            # 移除安全扫描相关依赖
            content = content.replace('"safety",  # 依赖安全检查\n', '')

            # 移除pydocstyle, bandit和其他安全检查工具配置
            lines = content.splitlines()
            filtered_lines = []
            skip_section = False
            for line in lines:
                if any(line.startswith(s) for s in ["# Bandit", "# Pydocstyle", "[tool.bandit]"]):
                    skip_section = True
                elif skip_section and (line.startswith("[tool.") or (line.strip() == "" and len(filtered_lines) > 0 and filtered_lines[-1].strip() == "")):
                    skip_section = False

                if not skip_section:
                    filtered_lines.append(line)

            pyproject_file.write_text("\n".join(filtered_lines))

        # 修改GitHub Actions工作流，移除安全检查相关步骤
        workflows_dir = pathlib.Path('.github', 'workflows')
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob('*.yml'):
                if workflow_file.exists():
                    content = workflow_file.read_text()

                    # 移除安全检查相关步骤
                    if 'bandit' in content or 'safety check' in content:
                        lines = content.splitlines()
                        filtered_lines = []
                        skip_step = False
                        for line in lines:
                            if ('bandit' in line or 'safety check' in line) and 'name:' in line:
                                skip_step = True
                            elif skip_step and line.strip().startswith('-') and 'run:' not in line:
                                continue
                            elif skip_step and 'run:' in line:
                                skip_step = False
                                continue

                            if not skip_step:
                                filtered_lines.append(line)

                        workflow_file.write_text("\n".join(filtered_lines))

    # 如果不使用CHANGELOG自动生成，移除相关文件
    if '{{ cookiecutter.include_changelog_gen }}' != 'y':
        # 移除脚本
        changelog_script = pathlib.Path('scripts', 'generate_changelog.py')
        if changelog_script.exists():
            changelog_script.unlink()

        # 如果scripts目录为空，也删除它
        scripts_dir = pathlib.Path('scripts')
        scripts_init = pathlib.Path('scripts', '__init__.py')
        if scripts_init.exists():
            scripts_init.unlink()

        if scripts_dir.exists() and not any(scripts_dir.iterdir()):
            scripts_dir.rmdir()

        # 移除Makefile中的CHANGELOG相关命令
        makefile = pathlib.Path('Makefile')
        if makefile.exists():
            content = makefile.read_text()
            # 移除changelog相关的.PHONY行
            content = content.replace(' changelog changelog-init', '')

            # 移除changelog目标
            lines = content.splitlines()
            filtered_lines = []
            skip_line = False
            for line in lines:
                if line.startswith('changelog:') or line.startswith('changelog-init:'):
                    skip_line = True
                elif skip_line and not line.startswith('\t'):
                    skip_line = False

                if not skip_line:
                    filtered_lines.append(line)

            makefile.write_text("\n".join(filtered_lines))

        # 修改pyproject.toml，移除gitpython依赖
        pyproject_file = pathlib.Path('pyproject.toml')
        if pyproject_file.exists():
            content = pyproject_file.read_text()
            content = content.replace('"gitpython",  # git操作，用于changelog生成\n', '')
            pyproject_file.write_text(content)

        # 移除CHANGELOG.md文件
        changelog_file = pathlib.Path('CHANGELOG.md')
        if changelog_file.exists():
            changelog_file.unlink()

        # 移除GitHub Actions的changelog.yml文件
        changelog_workflow = pathlib.Path('.github', 'workflows', 'changelog.yml')
        if changelog_workflow.exists():
            changelog_workflow.unlink()

        # 修改publish.yml，移除对CHANGELOG脚本的依赖
        publish_workflow = pathlib.Path('.github', 'workflows', 'publish.yml')
        if publish_workflow.exists():
            content = publish_workflow.read_text()

            # 回退到原来的发布说明生成方式
            content = re.sub(
                r'# 使用我们的CHANGELOG脚本生成变更日志[\s\S]*?EOF" >> \$GITHUB_OUTPUT',
                '''# 生成发布说明
      id: generate_notes
      run: |
        # 查找最近两个标签
        {% raw %}CURRENT_TAG="v${{ steps.get_version.outputs.version }}"
        PREV_TAG=$(git tag --sort=-creatordate | grep -v "^${CURRENT_TAG}$" | head -n 1)

        # 如果没有之前的标签，使用第一个提交
        if [ -z "$PREV_TAG" ]; then
          PREV_TAG=$(git rev-list --max-parents=0 HEAD)
        fi

        # 生成变更日志
        echo "从 ${PREV_TAG} 到 ${CURRENT_TAG} 的变更：" > RELEASE_NOTES.md
        echo "" >> RELEASE_NOTES.md
        git log --pretty=format:"* %s (%h)" ${PREV_TAG}..HEAD >> RELEASE_NOTES.md

        # 将发布说明设为输出变量
        NOTES=$(cat RELEASE_NOTES.md)
        echo "release_notes<<EOF" >> $GITHUB_OUTPUT
        echo "$NOTES" >> $GITHUB_OUTPUT
        echo "EOF" >> $GITHUB_OUTPUT{% endraw %}''',
                content
            )

            # 移除gitpython依赖
            content = re.sub(
                r'pip install gitpython',
                '',
                content
            )

            # 修改输出变量引用
            content = content.replace(
                '{% raw %}release_notes: ${{ steps.get_changelog.outputs.release_notes }}{% endraw %}',
                '{% raw %}release_notes: ${{ steps.generate_notes.outputs.release_notes }}{% endraw %}'
            )


            publish_workflow.write_text(content)

    # 如果不使用开发容器配置，移除相关文件
    if '{{ cookiecutter.include_devcontainer }}' != 'y':
        devcontainer_dir = pathlib.Path('.devcontainer')
        if devcontainer_dir.exists():
            for file in devcontainer_dir.glob('*'):
                file.unlink()
            devcontainer_dir.rmdir()

    # 如果不使用Dependabot，移除配置文件
    if '{{ cookiecutter.include_dependabot }}' != 'y':
        dependabot_file = pathlib.Path('.github', 'dependabot.yml')
        if dependabot_file.exists():
            dependabot_file.unlink()
    else:
        # 确保.github目录存在
        github_dir = pathlib.Path('.github')
        if not github_dir.exists():
            github_dir.mkdir(exist_ok=True)
            print("已创建 .github 目录")

    # 如果不使用Docker支持，移除相关文件
    if '{{ cookiecutter.include_docker }}' != 'y':
        # 移除Dockerfile
        dockerfile = pathlib.Path('Dockerfile')
        if dockerfile.exists():
            dockerfile.unlink()

        # 移除docker-compose.yml
        docker_compose = pathlib.Path('docker-compose.yml')
        if docker_compose.exists():
            docker_compose.unlink()

        # 移除Docker相关脚本
        docker_scripts = [
            pathlib.Path('scripts', 'docker-build.sh'),
            pathlib.Path('scripts', 'docker-run.sh'),
            pathlib.Path('scripts', 'docker-build.bat'),
            pathlib.Path('scripts', 'docker-run.bat')
        ]

        for script in docker_scripts:
            if script.exists():
                script.unlink()

        # 移除Docker文档
        docker_doc = pathlib.Path('docs', 'docker.md')
        if docker_doc.exists():
            docker_doc.unlink()

        # 更新README.rst，移除Docker相关内容
        readme = pathlib.Path('README.rst')
        if readme.exists():
            content = readme.read_text()

            # 移除Docker支持部分
            content = re.sub(
                r'\* Docker支持:[\s\S]*?完整的部署文档\n\n',
                '',
                content
            )

            readme.write_text(content)
    else:
        # 如果保留Docker支持，确保Shell脚本可执行
        shell_scripts = [
            pathlib.Path('scripts', 'docker-build.sh'),
            pathlib.Path('scripts', 'docker-run.sh')
        ]

        for script in shell_scripts:
            if script.exists():
                # 添加可执行权限(Unix系统)
                if os.name != 'nt':  # 非Windows
                    current = os.stat(script)
                    os.chmod(script, current.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # 如果ruff.toml为空，则删除它
    ruff_config = pathlib.Path('ruff.toml')
    if ruff_config.exists() and ruff_config.stat().st_size == 0:
        ruff_config.unlink()

    # 规范化.gitattributes行尾
    normalize_gitattributes()

    # 处理Cursor规则文件
    if '{{ cookiecutter.include_cursor_rules|default("n") }}' != 'y':
        cursor_rules_dir = pathlib.Path('.cursor', 'rules')
        if cursor_rules_dir.exists():
            for file in cursor_rules_dir.glob('*'):
                file.unlink()
            cursor_rules_dir.rmdir()

            # 如果.cursor目录为空，也删除它
            cursor_dir = pathlib.Path('.cursor')
            if not any(cursor_dir.iterdir()):
                cursor_dir.rmdir()

    # 恢复MkDocs特殊语法
    # restore_mkdocs_syntax()
