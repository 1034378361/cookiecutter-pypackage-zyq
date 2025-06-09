# {{ cookiecutter.display_name }}

{% if cookiecutter.open_source_license != 'Not open source' -%}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})

{% if cookiecutter.include_github_actions == 'y' -%}
[![Tests](https://github.com/{{ cookiecutter.__gh_slug }}/actions/workflows/test.yml/badge.svg)](https://github.com/{{ cookiecutter.__gh_slug }}/actions/workflows/test.yml)
{% endif -%}

[![文档](https://img.shields.io/badge/文档-GitHub_Pages-blue)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/)

{% if cookiecutter.add_pyup_badge == 'y' -%}
[![Updates](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{% endif -%}
{% endif %}

{{ cookiecutter.project_short_description }}

{% if cookiecutter.open_source_license != 'Not open source' -%}
* 开源协议: {{ cookiecutter.open_source_license }}
* 文档: [https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})
{% endif %}

## 特性

* 现代化依赖管理:
  * 使用PDM管理依赖和构建
  * 精确依赖版本锁定
  * 分组依赖管理
  * 简化发布流程

{% if cookiecutter.include_github_actions == 'y' -%}
* GitHub Actions CI: 自动测试、代码风格检查
* GitHub 自动发布: 通过标签发布到PyPI
{% endif %}

{% if cookiecutter.include_utils_lib == 'y' -%}
* 内置工具库:
  * 文件处理工具 (JSON/YAML/Pickle)
  * 数据处理工具 (字符串、日期、字典处理)
  * 日志工具 (控制台/文件/轮转日志)
{% endif %}

{% if cookiecutter.include_version_management == 'y' -%}
* 智能版本管理:
  * 自动从Git标签读取版本
  * 支持开发和分发版本管理
{% endif %}

{% if cookiecutter.command_line_interface.lower() == 'typer' -%}
* 命令行工具: 基于Typer的命令行接口
{% elif cookiecutter.command_line_interface.lower() == 'argparse' -%}
* 命令行工具: 基于Argparse的命令行接口
{% endif %}

{% if cookiecutter.include_pre_commit == 'y' -%}
* 代码质量工具:
  * Pre-commit钩子自动检查代码风格和质量
  * 集成Black/isort/ruff/mypy/bandit等工具
  * 自动类型检查与报告:
    * CI中独立的类型检查流程
    * 每周自动生成类型覆盖率报告
    * 严格的类型验证确保代码健壮性
  * 测试覆盖率要求:
    * 配置最低覆盖率阈值(85%)
    * CI流程中强制检查覆盖率
    * 生成HTML和XML格式覆盖率报告
{% endif %}

{% if cookiecutter.include_changelog_gen == 'y' -%}
* 自动化变更日志:
  * 从git提交历史自动生成CHANGELOG
  * 根据约定式提交格式分类变更
  * 支持增量更新和完整历史生成
  * GitHub Actions自动更新:
    * 推送标签时自动更新
    * 合并PR时自动更新
    * 支持手动触发
  * 与发布流程集成:
    * 发布到PyPI时自动生成发布说明
    * GitHub Release说明自动使用CHANGELOG内容
{% endif %}

{% if cookiecutter.include_devcontainer == 'y' -%}
* 开发容器配置:
  * 标准化开发环境，确保一致性体验
  * VS Code开发容器支持
  * 预配置Python开发工具和扩展
  * 无需手动配置即可开始开发
{% endif %}

{% if cookiecutter.include_dependabot == 'y' -%}
* 依赖自动更新:
  * GitHub Dependabot集成
  * 自动检测并更新过期依赖
  * 智能分组相关依赖更新
  * 维护Python包、GitHub Actions和Docker镜像
{% endif %}

* Docker支持:
  * 多阶段构建优化的应用镜像
  * Docker Compose配置
  * 方便的构建和运行脚本
  * 完整的部署文档

## 快速开始

### 环境设置

本项目提供了便捷的环境设置脚本，可根据不同操作系统安装必要的开发工具：

#### Linux/macOS 用户

使用提供的安装脚本：

```bash
# 安装pyenv和PDM
./install.sh
```

#### Windows 用户

使用PowerShell脚本：

```powershell
# 以管理员权限运行安装脚本
./setup-windows.ps1
```

或者使用Makefile：

```bash
# 安装pyenv-win
make install-pyenv

# 安装PDM
make pdm-install

# 一键安装所有开发工具
make setup
```

### 安装

手动安装PDM依赖管理工具：

```bash
# Linux/macOS
curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://pdm.fming.dev/install-pdm.py -UseBasicParsing).Content | py -
```

安装本项目：

```bash
# 安装项目及其依赖
pdm install

# 安装开发依赖
pdm install -dG dev
```

### 使用

```python
from {{ cookiecutter.project_slug }} import somefunction

# 使用示例
result = somefunction()
```

### 开发

```bash
# 运行测试
pdm run pytest

# 代码格式化
pdm run make format

# 代码检查
pdm run make lint
```

## 功能列表

* TODO

## 贡献者

本项目使用 [Cookiecutter](https://github.com/audreyr/cookiecutter) 和 [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) 项目模板修改后创建。
