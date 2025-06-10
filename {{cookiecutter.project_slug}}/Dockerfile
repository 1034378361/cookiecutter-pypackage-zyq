###############
# 构建阶段
###############
FROM python:{{cookiecutter.python_version}}-slim-bookworm AS builder

WORKDIR /app

# 设置构建环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1

# 安装构建依赖 - 仅安装必要的包
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 首先复制依赖文件，利用Docker缓存层
COPY pyproject.toml README.md ./

# 复制源代码
COPY src ./src/

# 安装依赖并构建wheel包
RUN pip wheel --no-deps --no-cache-dir --wheel-dir /app/wheels -e .

###############
# 最终运行阶段
###############
FROM python:{{cookiecutter.python_version}}-slim-bookworm

# 设置标签，提供镜像元数据
LABEL maintainer="{{cookiecutter.full_name}} <{{cookiecutter.email}}>" \
      name="{{cookiecutter.project_slug}}" \
      version="{{cookiecutter.version}}" \
      description="{{cookiecutter.project_short_description}}"

# 创建非root用户
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser

# 设置工作目录
WORKDIR /app

# 设置运行环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random

# 从构建阶段复制wheel包和必要文件
COPY --from=builder /app/wheels /app/wheels
COPY --from=builder /app/src ./src

# 安装应用并清理
RUN pip install --no-cache-dir /app/wheels/*.whl && \
    rm -rf /app/wheels && \
    find /usr/local -type d -name __pycache__ -exec rm -rf {} +

# 安全措施：设置正确的文件权限
RUN chown -R appuser:appgroup /app && \
    chmod -R 755 /app

# 切换到非root用户
USER appuser

# 健康检查 - 每30秒检查一次
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    {% if cookiecutter.command_line_interface.lower() != 'no command-line interface' %}
    CMD {{cookiecutter.project_slug}} --version || exit 1
    {% else %}
    CMD python -c "from {{cookiecutter.project_slug}} import __version__; print(__version__)" || exit 1
    {% endif %}

# 设置资源限制
ENV MALLOC_ARENA_MAX=2

# 容器启动命令
{% if cookiecutter.command_line_interface.lower() != 'no command-line interface' %}
ENTRYPOINT ["{{cookiecutter.project_slug}}"]
CMD ["--help"]
{% else %}
CMD ["python", "-c", "from {{cookiecutter.project_slug}} import __version__; print(f'{{cookiecutter.project_name}} v{__version__}')"]
{% endif %}
