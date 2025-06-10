# {{ cookiecutter.project_name }}

[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})
[![测试](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/test.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/test.yml)
[![文档](https://img.shields.io/badge/文档-GitHub_Pages-blue)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/)
{% if cookiecutter.include_coverage_badge == "y" -%}
[![代码覆盖率](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
{%- endif %}

{{ cookiecutter.project_short_description }}

* 开源协议: {{ cookiecutter.open_source_license }}
* 文档: [https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }})

## 特性

* 现代化Python包结构:
  * 使用`src`布局，提高包安全性
  * 完整的类型注解支持
  * 模块化设计，易于扩展

* 自动化测试与CI:
  * 基于pytest的测试框架
  * GitHub Actions持续集成
  * 自动测试、代码风格检查
  * 自动发布到PyPI

{% if cookiecutter.include_mypy == "y" -%}
* 类型检查:
  * 严格的mypy类型验证
  * 类型覆盖率报告
  * 预配置的类型检查设置
{%- endif %}

{% if cookiecutter.include_cli == "y" -%}
* 命令行接口:
  * 基于{{ cookiecutter.cli_framework }}的命令行工具
  * 自动生成帮助文档
  * 命令补全支持
  * 友好的错误提示
{%- endif %}

* 代码质量工具:
  * 预配置的pre-commit钩子
  * 代码格式化(Black, isort)
  * 代码质量检查(Ruff)
  * 安全性检查(Bandit)

* 完整的开发工具链:
  * 可重现的开发环境
  * 一致的代码风格
  * 自动化文档生成
  * 版本管理工具

{% if cookiecutter.use_docker == "y" -%}
* Docker支持:
  * 优化的Dockerfile
  * Docker Compose配置
  * 多阶段构建流程
  * 生产环境就绪配置
{%- endif %}

## 快速开始

### 安装

{% if cookiecutter.use_docker == "y" -%}
#### 使用Docker

```bash
# 构建Docker镜像
docker-compose build

# 运行容器
docker-compose up -d
```

#### 手动安装
{%- endif %}

从PyPI安装:

```bash
pip install {{ cookiecutter.project_slug }}
```

从源码安装:

```bash
# 克隆仓库
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# 安装项目及其依赖
pip install -e ".[dev]"
```

### 使用示例

```python
from {{ cookiecutter.project_slug }} import example_function

# 使用示例
result = example_function()
print(result)
```

{% if cookiecutter.include_cli == "y" -%}
### 命令行使用

安装后，可以直接使用命令行工具:

```bash
# 显示帮助信息
{{ cookiecutter.project_slug }} --help

# 运行主要功能
{{ cookiecutter.project_slug }} run

# 查看版本
{{ cookiecutter.project_slug }} --version
```
{%- endif %}

## 开发

### 环境设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 安装pre-commit钩子
pre-commit install
```

### 常用命令

```bash
# 运行测试
pytest

# 生成测试覆盖率报告
pytest --cov={{ cookiecutter.project_slug }}

# 代码格式化
make format

# 代码质量检查
make lint

{% if cookiecutter.include_mypy == "y" -%}
# 类型检查
make type-check
{%- endif %}

# 构建文档
make docs
```

## 发布流程

1. 更新版本号（在src/{{ cookiecutter.project_slug }}/_version.py中）
2. 提交所有更改
3. 创建新标签: `git tag v0.1.0`
4. 推送标签: `git push --tags`

GitHub Actions将自动构建并发布到PyPI。

## 贡献指南

欢迎贡献！请查看[CONTRIBUTING.rst](CONTRIBUTING.rst)了解如何参与项目开发。

## 更新日志

查看[CHANGELOG.md](CHANGELOG.md)了解版本历史和更新内容。
