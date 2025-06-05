# 使用指南

## 基础用法

导入 {{ cookiecutter.project_slug }} 包:

```python
import {{ cookiecutter.project_slug }}
```

获取版本号:

```python
print({{ cookiecutter.project_slug }}.__version__)
```

{% if cookiecutter.command_line_interface.lower() == 'typer' %}
## 命令行接口

{{ cookiecutter.project_slug }} 提供了命令行接口:

```bash
{{ cookiecutter.project_slug }} --help
```

{% endif %}

{% if cookiecutter.include_utils_lib == 'y' %}
## 工具函数

文件操作示例:

```python
from {{ cookiecutter.project_slug }}.utils.file_utils import ensure_dir, load_json, save_json

# 创建目录
data_dir = ensure_dir("./data")

# 保存和加载JSON
config = {"app_name": "my_app", "debug": True}
config_file = data_dir / "config.json"

save_json(config, config_file)
loaded_config = load_json(config_file)
```

数据处理示例:

```python
from {{ cookiecutter.project_slug }}.utils.data_utils import format_datetime, clean_text

# 格式化当前日期时间
now = format_datetime()
print(f"当前时间: {now}")

# 清理文本
text = "  这是一段   带有多余空格   的文本  "
clean = clean_text(text)
print(clean)  # "这是一段 带有多余空格 的文本"
```

日志配置示例:

```python
import logging
from {{ cookiecutter.project_slug }}.utils.logging_utils import setup_logger

# 创建日志记录器
logger = setup_logger(
    name="app_logger",
    level=logging.INFO,
    log_file="app.log"
)

# 记录日志
logger.info("应用启动")
logger.error("发生错误")
```

更多示例请参考 [工具库](utils.md) 页面。
{% endif %}

## 高级用法

根据你的项目需要添加更多示例...
