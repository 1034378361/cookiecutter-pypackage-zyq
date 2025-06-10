# {{ cookiecutter.project_name }}

[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})
[![测试状态](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/test.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/test.yml)
[![文档状态](https://img.shields.io/badge/文档-最新-blue)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/)
[![代码覆盖率](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})

{{ cookiecutter.project_short_description }}

## 概述

{{ cookiecutter.project_name }} 是一个现代化的 Python 项目，旨在提供高质量、类型安全的代码库。本文档提供了项目的详细说明、安装指南和使用示例。

## 项目特性

* 完整的类型注解支持
* 全面的测试覆盖
* 详细的API文档
{% if cookiecutter.command_line_interface != "No command-line interface" %}* 友好的命令行界面{% endif %}
{% if cookiecutter.project_type == "Web Service" %}* 容器化部署支持{% endif %}
* 符合PEP标准的代码风格

## 安装指南

### 从PyPI安装

```bash
pip install {{ cookiecutter.project_slug }}
```

### 从源码安装

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
pip install -e ".[dev]"
```

{% if cookiecutter.project_type == "Web Service" %}
### 使用Docker

```bash
# 构建Docker镜像
docker-compose build

# 运行容器
docker-compose up -d
```
{% endif %}

## 使用示例

```python
from {{ cookiecutter.project_slug }} import example_function

# 使用示例
result = example_function()
print(result)
```

{% if cookiecutter.command_line_interface != "No command-line interface" %}
## 命令行使用

安装后，您可以直接使用命令行工具:

```bash
# 显示帮助信息
{{ cookiecutter.project_slug }} --help

# 运行主要功能
{{ cookiecutter.project_slug }} run

# 查看版本
{{ cookiecutter.project_slug }} --version
```
{% endif %}

## 项目结构

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.project_slug }}/
│       ├── __init__.py
│       ├── _version.py
{% if cookiecutter.command_line_interface != "No command-line interface" %}│       ├── cli.py{% endif %}
│       └── utils/
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── docs/
├── .github/workflows/
└── pyproject.toml
```

## 许可证

{{ cookiecutter.open_source_license }}

## 项目概述

{{ cookiecutter.project_name }} 是一个Python项目，旨在{% if cookiecutter.project_short_description %}{{ cookiecutter.project_short_description | lower }}{% else %}提供高质量的功能和工具{% endif %}。

## 快速开始

安装包：

```bash
pip install {{ cookiecutter.project_slug }}
```

基本用法：

```python
import {{ cookiecutter.project_slug }}

# 使用示例代码
```

## 目录

- [安装说明](installation.md) - 详细安装指南
- [使用指南](usage.md) - 如何使用此项目
- [统一安装脚本](setup_script.md) - setup.py脚本说明
- [项目结构](project_structure.md) - 项目目录结构说明
- [工具库](utils.md) - 项目提供的工具函数
- [版本管理](version.md) - 版本管理方法
- [开发指南](developer_guide.md) - 参与项目开发
- [Dependabot](dependabot.md) - 依赖管理
- [Docker](docker.md) - Docker相关指南
- [API参考](api/index.md) - 详细API文档
- [贡献指南](contributing.md) - 如何贡献代码
- [更新日志](history.md) - 项目变更历史
