# API参考文档

本节包含了{{ cookiecutter.project_name }}的API参考文档。文档由代码注释自动生成。

## 模块概览

### 核心模块

<!--
在生成的项目中，此处将使用MkDocs插件显示模块API文档:
::: {{ cookiecutter.project_slug }}
-->

{% if cookiecutter.include_utils_lib == 'y' %}
### 工具函数

<!--
在生成的项目中，此处将使用MkDocs插件显示工具函数API文档:
::: {{ cookiecutter.project_slug }}.utils
-->
{% endif %}

{% if cookiecutter.command_line_interface.lower() == "typer" %}
### 命令行接口

<!--
在生成的项目中，此处将使用MkDocs插件显示CLI API文档:
::: {{ cookiecutter.project_slug }}.cli
-->
{% endif %}

## 使用示例

```python
# 导入包
import {{ cookiecutter.project_slug }}

# 使用主要功能
# 示例代码
```
