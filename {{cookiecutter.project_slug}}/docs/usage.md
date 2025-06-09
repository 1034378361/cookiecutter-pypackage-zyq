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

## 开发工作流

本项目使用现代化的开发工作流，包含以下关键组件:

### 1. 代码质量控制

项目使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码质量检查和格式化:

```bash
# 检查代码质量
make lint

# 格式化代码
make format
```

### 2. 测试

使用 pytest 运行测试:

```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_specific.py

# 生成覆盖率报告
make coverage
```

### 3. 文档

使用 MkDocs 构建文档:

```bash
# 构建文档
make docs

# 启动文档服务器（实时预览）
make servedocs
```

### 4. 版本发布

更新版本并发布:

```bash
# 1. 更新版本号
# 在 src/{{ cookiecutter.project_slug }}/_version.py 中修改版本号

# 2. 创建标签
git tag v0.1.0

# 3. 推送标签
git push --tags

# 4. GitHub Actions会自动构建并发布到PyPI
```

### 5. Docker支持

使用Docker进行开发和测试:

```bash
# 构建Docker镜像
make docker-build

# 运行Docker容器
make docker-run
```

## Makefile命令汇总

项目提供了以下Makefile命令:

| 命令 | 描述 |
|------|------|
| `make help` | 显示帮助信息 |
| `make clean` | 清理构建产物和缓存 |
| `make lint` | 检查代码质量 |
| `make format` | 格式化代码 |
| `make test` | 运行测试 |
| `make coverage` | 生成覆盖率报告 |
| `make docs` | 构建文档 |
| `make servedocs` | 启动文档服务器 |
| `make dist` | 构建分发包 |
| `make install` | 安装包 |
| `make dev-install` | 安装包和开发依赖 |
| `make venv` | 创建虚拟环境 |
| `make docker-build` | 构建Docker镜像 |
| `make docker-run` | 运行Docker容器 |

## 高级用法

根据你的项目需要添加更多示例...
