# {{ cookiecutter.project_name }} 文档

{{ cookiecutter.project_short_description }}

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
{% if cookiecutter.include_utils_lib == 'y' %}- [工具库](utils.md) - 项目提供的工具函数{% endif %}
{% if cookiecutter.include_version_management == 'y' %}- [版本管理](version.md) - 版本管理方法{% endif %}
- [开发指南](developer_guide.md) - 参与项目开发
{% if cookiecutter.include_dependabot == 'y' %}- [Dependabot](dependabot.md) - 依赖管理{% endif %}
{% if cookiecutter.include_docker == 'y' %}- [Docker](docker.md) - Docker相关指南{% endif %}
- [API参考](api/index.md) - 详细API文档
- [贡献指南](contributing.md) - 如何贡献代码
- [更新日志](history.md) - 项目变更历史
