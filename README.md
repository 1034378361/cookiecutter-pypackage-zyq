# Cookiecutter PyPackage ZYQ 模板

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![测试](https://github.com/1034378361/cookiecutter-pypackage-zyq/actions/workflows/test.yml/badge.svg)](https://github.com/1034378361/cookiecutter-pypackage-zyq/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 [Cookiecutter](https://github.com/cookiecutter/cookiecutter) 的现代化 Python 包模板，提供完整的开发工具链和最佳实践。

## 特性

* 📦 **现代包结构**：使用 `src` 布局，增强包安全性
* 🧪 **自动化测试**：预配置的 pytest 和代码覆盖率检查
* 🔍 **类型检查**：集成 mypy 和类型覆盖率报告
* 📝 **代码质量**：集成 Black、isort、Ruff 和 pre-commit
* 📄 **自动文档**：使用 Sphinx 生成文档并发布到 GitHub Pages
* 🚀 **CI/CD 流程**：配置完善的 GitHub Actions 工作流
* 🛠️ **多种项目类型**：支持标准库、CLI 工具、Web 服务、数据科学项目
* 🔄 **自动发布**：自动化发布到 PyPI 和更新 CHANGELOG

## 快速开始

### 前提条件

* Python 3.8+
* [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

### 安装

使用 pip 安装 Cookiecutter：

```bash
pip install cookiecutter
```

### 使用方法

使用此模板创建新项目：

```bash
cookiecutter https://github.com/1034378361/cookiecutter-pypackage-zyq
```

或者从本地使用：

```bash
cookiecutter /path/to/cookiecutter-pypackage-zyq
```

### 配置选项

| 选项                      | 描述                                       | 默认值                      |
|--------------------------|-------------------------------------------|----------------------------|
| project_name             | 项目名称                                    | Python Package             |
| project_slug             | 包名（用于导入）                             | python_package             |
| project_short_description| 项目简短描述                                | 一个现代化的Python包         |
| github_username          | GitHub用户名                               | username                   |
| full_name                | 作者全名                                    | Your Name                  |
| email                    | 作者邮箱                                    | your.email@example.com     |
| version                  | 初始版本                                    | 0.1.0                      |
| open_source_license      | 开源许可证                                  | MIT license                |
| project_type             | 项目类型                                    | Standard Library           |
| command_line_interface   | 命令行接口框架                               | Typer                      |

## 项目结构

生成的项目具有以下结构：

```
my_package/
├── .github/
│   └── workflows/          # GitHub Actions 工作流配置
├── docs/                   # 项目文档
├── scripts/                # 辅助脚本
├── src/                    # 源代码目录
│   └── my_package/         # 包源码
│       ├── utils/          # 工具函数
│       ├── __init__.py     # 包初始化
│       ├── _version.py     # 版本信息
│       └── cli.py          # 命令行接口
├── tests/                  # 测试目录
│   ├── conftest.py         # pytest 配置
│   └── test_*.py           # 测试模块
├── .gitignore              # Git 忽略配置
├── .pre-commit-config.yaml # pre-commit 配置
├── CHANGELOG.md            # 变更日志
├── LICENSE                 # 许可证文件
├── Makefile                # 常用命令
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 开发工作流

生成的项目支持以下开发工作流：

1. **本地开发**：安装开发依赖 `pip install -e ".[dev]"`
2. **代码质量检查**：使用 `make lint` 运行代码检查
3. **测试**：使用 `make test` 运行测试
4. **文档**：使用 `make docs` 生成文档
5. **发布**：通过推送新标签触发自动发布

## 贡献指南

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多信息。

## 致谢

此项目基于 [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) 的工作，融合了多种现代 Python 开发实践。

## 许可证

MIT许可证
