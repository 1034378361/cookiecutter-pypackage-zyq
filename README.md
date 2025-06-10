# Python包项目模板

[![更新状态](https://pyup.io/repos/github/1034378361/cookiecutter-pypackage/shield.svg)](https://pyup.io/repos/github/1034378361/cookiecutter-pypackage/)
[![文档状态](https://readthedocs.org/projects/cookiecutter-pypackage/badge/?version=latest)](https://cookiecutter-pypackage.readthedocs.io/en/latest/?badge=latest)
[![GitHub Actions](https://github.com/1034378361/cookiecutter-pypackage/actions/workflows/test.yml/badge.svg)](https://github.com/1034378361/cookiecutter-pypackage/actions/workflows/test.yml)

基于[Cookiecutter](https://github.com/cookiecutter/cookiecutter)的Python包项目模板。

* GitHub仓库: <https://github.com/1034378361/cookiecutter-pypackage-zyq/>
* 文档: <https://cookiecutter-pypackage-zyq.readthedocs.io/>
* 开源协议: BSD协议

## 特性

* 测试设置：完整支持`pytest`测试框架
* GitHub Actions：配置完善的CI/CD流程，自动化测试和部署
* Tox：轻松测试多个Python版本(3.8-3.12)
* 文档生成：支持MkDocs和Sphinx两种文档生成工具
* 版本管理：一键版本更新机制
* 自动发布：推送新标签时自动发布到PyPI
* 命令行接口：可选集成Typer、Click或Argparse
* 代码质量：预配置Black、Ruff、isort和mypy等工具
* 跨平台：完全支持Windows、Linux和macOS
* Docker支持：内置Dockerfile和docker-compose配置
* 类型检查：内置mypy配置，支持静态类型检查
* 依赖管理：根据项目类型智能选择依赖

## 快速开始

安装最新版Cookiecutter（需要1.4.0或更高版本）:

```bash
pip install -U cookiecutter
```

生成Python包项目:

```bash
cookiecutter https://github.com/yourusername/cookiecutter-pypackage-zyq.git
```

然后:

1. 创建代码库并提交代码 (`git init && git add . && git commit -m "初始化项目"`)
2. 安装开发依赖 (`pip install -e ".[dev]"`)
3. 在PyPI上注册你的项目
4. 添加GitHub Secrets进行自动发布
5. 设置Read the Docs账户和服务钩子
6. 推送新标签发布你的包 (`git tag v0.1.0 && git push --tags`)
7. 激活你的项目依赖管理

## 项目配置选项

创建项目时，你可以配置以下选项：

* `project_name`: 项目名称
* `project_slug`: 项目标识符（用于包名）
* `project_description`: 项目简短描述
* `project_type`: 项目类型（CLI、Web、数据科学等）
* `python_version`: 支持的Python最低版本
* `use_docker`: 是否包含Docker配置
* `include_cli`: 是否包含命令行接口
* `cli_framework`: 选择CLI框架（Typer、Click、Argparse）
* `documentation_tool`: 文档工具（MkDocs或Sphinx）
* `license`: 项目许可证

## 不完全符合你的需求？

以下是一些选择：

### 类似的Cookiecutter模板

* [Nekroze/cookiecutter-pypackage](https://github.com/Nekroze/cookiecutter-pypackage): 严格的测试和文档设置
* [briggySmalls/cookiecutter-pypackage](https://github.com/briggySmalls/cookiecutter-pypackage): 使用Poetry进行包管理
* [waynerv/cookiecutter-pypackage](https://waynerv.github.io/cookiecutter-pypackage/): 集成Poetry、MkDocs、Pre-commit、Black和Mypy
* [zillionare/cookiecutter-pypackage](https://zillionare.github.io/cookiecutter-pypackage/): 包含Poetry、MkDocs和GitHub CI

### 创建自己的版本

如果你有不同的设置偏好，欢迎fork这个项目创建自己的版本。

* 一旦你的版本可用，请将其添加到上面的类似模板列表中
* 你可以自由决定是否重命名你的fork/版本

### 提交Pull Request

欢迎提交Pull Request，特别是那些小型的、原子化的、能够改善用户体验的改进。
