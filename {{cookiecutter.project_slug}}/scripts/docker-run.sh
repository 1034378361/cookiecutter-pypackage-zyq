#!/bin/bash
# Docker容器运行脚本

# 确保在项目根目录下运行
cd "$(dirname "$0")/.." || exit

# 定义变量
IMAGE_NAME="{{cookiecutter.project_slug}}"
TAG="${1:-latest}"  # 使用第一个参数作为标签，默认为latest
CONTAINER_NAME="{{cookiecutter.project_slug}}-instance"

# 检查镜像是否存在
if ! docker images "$IMAGE_NAME:$TAG" | grep -q "$IMAGE_NAME"; then
    echo "镜像 $IMAGE_NAME:$TAG 不存在，正在构建..."
    ./scripts/docker-build.sh "$TAG"
fi

# 检查是否有同名容器在运行
if docker ps -a | grep -q "$CONTAINER_NAME"; then
    echo "发现同名容器，正在停止并移除..."
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1
fi

# 创建数据和配置目录(如果不存在)
mkdir -p ./data
mkdir -p ./config

# 运行Docker容器
echo "正在启动容器 $CONTAINER_NAME 使用镜像 $IMAGE_NAME:$TAG..."
docker run -it --name "$CONTAINER_NAME" \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/config:/app/config" \
    "$IMAGE_NAME:$TAG" "$@"

# 显示容器状态
echo "容器状态:"
docker ps -a | grep "$CONTAINER_NAME"
