# Cookiecutter PyPackage

[![Updates](https://pyup.io/repos/github/audreyfeldroy/cookiecutter-pypackage/shield.svg)](https://pyup.io/repos/github/audreyfeldroy/cookiecutter-pypackage/)
[![Documentation Status](https://readthedocs.org/projects/cookiecutter-pypackage/badge/?version=latest)](https://cookiecutter-pypackage.readthedocs.io/en/latest/?badge=latest)
[![GitHub Actions](https://github.com/audreyfeldroy/cookiecutter-pypackage/actions/workflows/test.yml/badge.svg)](https://github.com/audreyfeldroy/cookiecutter-pypackage/actions/workflows/test.yml)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

* GitHub repo: <https://github.com/audreyfeldroy/cookiecutter-pypackage/>
* Documentation: <https://cookiecutter-pypackage.readthedocs.io/>
* Free software: BSD license
* Discord: <https://discord.gg/PWXJr3upUE>

## 特性

* 测试设置：支持 `pytest`
* GitHub Actions：配置完善的CI/CD流程
* Tox：轻松测试多个Python版本(3.8-3.12)
* 文档生成：支持MkDocs和Sphinx
* 版本管理：一键版本更新
* 自动发布：推送新标签时自动发布到PyPI
* 命令行接口：可选集成Click或Argparse
* 代码质量：预配置Black、Ruff、isort和mypy
* 跨平台：Windows、Linux和macOS支持

## 快速开始

安装最新版Cookiecutter（需要1.4.0或更高版本）:

```bash
pip install -U cookiecutter
```

生成Python包项目:

```bash
cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git
```

然后:

1. 创建代码库并提交代码
2. 安装开发依赖 (`pip install -e ".[dev]"`)
3. 在PyPI上注册你的项目
4. 添加GitHub Secrets进行自动发布
5. 设置Read the Docs账户和服务钩子
6. 推送新标签发布你的包
7. 激活你的项目依赖管理

更多详情，请参阅[cookiecutter-pypackage教程](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html)。

## 不完全符合你的需求？

别担心，你有以下选择：

### 类似的Cookiecutter模板

* [Nekroze/cookiecutter-pypackage](https://github.com/Nekroze/cookiecutter-pypackage): 严格的测试和文档设置
* [briggySmalls/cookiecutter-pypackage](https://github.com/briggySmalls/cookiecutter-pypackage): 使用Poetry进行包管理
* [waynerv/cookiecutter-pypackage](https://waynerv.github.io/cookiecutter-pypackage/): 集成Poetry、MkDocs、Pre-commit、Black和Mypy
* [zillionare/cookiecutter-pypackage](https://zillionare.github.io/cookiecutter-pypackage/): 包含Poetry、MkDocs和GitHub CI

你也可以查看此仓库的[网络](https://github.com/audreyr/cookiecutter-pypackage/network)和[家族树](https://github.com/audreyr/cookiecutter-pypackage/network/members)。

### 创建自己的版本

如果你有不同的设置偏好，欢迎fork这个项目创建自己的版本。

* 一旦你的版本可用，请将其添加到上面的类似模板列表中
* 你可以自由决定是否重命名你的fork/版本

### 提交Pull Request

我也欢迎Pull Request，特别是那些小型的、原子化的、能够改善包装体验的改进。
