#!/bin/bash
# Docker镜像构建脚本

# 确保在项目根目录下运行
cd "$(dirname "$0")/.." || exit

# 定义变量
IMAGE_NAME="{{cookiecutter.project_slug}}"
TAG="${1:-latest}"  # 使用第一个参数作为标签，默认为latest

# 显示构建信息
echo "正在构建 $IMAGE_NAME:$TAG..."

# 构建Docker镜像
docker build -t "$IMAGE_NAME:$TAG" .

# 检查构建结果
if [ $? -eq 0 ]; then
    echo "成功构建镜像: $IMAGE_NAME:$TAG"
    docker images | grep "$IMAGE_NAME" | grep "$TAG"
else
    echo "构建失败!"
    exit 1
fi
