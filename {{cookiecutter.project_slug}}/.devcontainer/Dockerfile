FROM centos:7.5.1804

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# 安装基本工具
RUN yum update -y \
    && yum install -y \
    gcc \
    gcc-c++ \
    make \
    wget \
    curl \
    git \
    sudo \
    which \
    bzip2-devel \
    openssl-devel \
    libffi-devel \
    zlib-devel \
    xz-devel \
    sqlite-devel \
    readline-devel

# 安装Python {{cookiecutter.python_min_version}}
# 注意：指定使用3.10.6版本
RUN cd /tmp \
    && wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz \
    && tar xzf Python-3.10.6.tgz \
    && cd Python-3.10.6 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && ln -sf /usr/local/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/local/bin/pip3.10 /usr/bin/pip3 \
    && rm -rf /tmp/Python-3.10.6*

# 创建非root用户
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 设置Python环境
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir pytest pytest-cov \
    && pip3 install --no-cache-dir black isort ruff mypy sphinx sphinx-rtd-theme \
    {% if cookiecutter.include_pre_commit == 'y' %}pre-commit bandit{% endif %} \
    {% if cookiecutter.include_changelog_gen == 'y' %}gitpython{% endif %}

# 创建工作目录
WORKDIR /workspace

# 设置默认用户为非root
USER $USERNAME

# 设置环境变量
ENV PYTHONPATH=/workspace
ENV PATH=$PATH:/home/$USERNAME/.local/bin
