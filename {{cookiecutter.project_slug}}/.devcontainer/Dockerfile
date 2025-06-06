FROM python:3.11

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive

# 自动换源为阿里云 + 安装系统依赖和常用调试工具
RUN codename=$(grep VERSION_CODENAME /etc/os-release | cut -d= -f2) && \
    echo "使用 codename: $codename" && \
    [ -f /etc/apt/sources.list ] || touch /etc/apt/sources.list && \
    rm -rf /etc/apt/sources.list.d/* && \
    echo "deb https://mirrors.aliyun.com/debian $codename main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security $codename-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian $codename-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian $codename-backports main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
        tzdata sudo git curl wget gcc g++ make build-essential \
        libffi-dev libbz2-dev zlib1g-dev libsqlite3-dev libreadline-dev \
        vim less net-tools iputils-ping \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 切换到普通用户
USER $USERNAME
WORKDIR /home/$USERNAME

# 设置 PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# 创建 .bashrc 并配置 PATH
RUN touch ~/.bashrc && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 确保权限
RUN chown -R $USERNAME:$USERNAME /home/$USERNAME


