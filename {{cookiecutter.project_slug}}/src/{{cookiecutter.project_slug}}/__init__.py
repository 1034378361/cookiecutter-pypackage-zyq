"""Top-level package for {{ cookiecutter.project_name }}."""

import os
import logging

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = '{{ cookiecutter.email }}'

{% if cookiecutter.include_version_management == 'y' %}
# 版本管理
from ._version import get_version

# 如果环境变量设置了调试模式，添加提交哈希到版本号
__version__ = get_version(with_commit=os.environ.get('DEBUG', '').lower() in ('1', 'true'))
{% else %}
# 版本定义
__version__ = '{{ cookiecutter.version }}'
{% endif %}

# 配置基本日志
logging.basicConfig(
    level=logging.INFO if os.environ.get('DEBUG', '').lower() not in ('1', 'true') else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 导入工具函数
from . import utils
