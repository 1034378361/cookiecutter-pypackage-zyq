# API参考文档

本节包含了{{ cookiecutter.project_name }}的API参考文档。文档由代码注释自动生成。

## 模块概览

### 核心模块

::: {{ cookiecutter.project_slug }}

{% if cookiecutter.include_utils_lib == 'y' %}
### 工具函数

::: {{ cookiecutter.project_slug }}.utils
{% endif %}

{% if cookiecutter.command_line_interface.lower() == "typer" %}
### 命令行接口

::: {{ cookiecutter.project_slug }}.cli
{% endif %}

## 使用示例

```python
# 导入包
import {{ cookiecutter.project_slug }}

# 使用主要功能
# 示例代码
```
