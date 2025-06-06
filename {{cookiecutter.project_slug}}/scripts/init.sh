#!/bin/bash
set -e

# export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

log() { echo -e "\033[1;32m[init] $1\033[0m"; }

# 初始化git仓库（如未初始化）
if [ ! -d .git ]; then
  log "初始化git仓库..."
  git init
fi

# 安装poetry
if ! command -v poetry &> /dev/null; then
  log "安装poetry..."
  pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple poetry
  log "poetry安装完成"
else
  log "poetry已安装，跳过。"
fi

log "配置poetry国内源和并行加速..."
# 配置poetry国内源和并行加速
poetry config repositories.aliyun https://mirrors.aliyun.com/pypi/simple/
poetry config installer.parallel true
log "poetry配置完成"

# 安装pre-commit
if ! command -v pre-commit &> /dev/null; then
  log "安装pre-commit..."
  pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple pre-commit
  log "pre-commit安装完成"
else
  log "pre-commit已安装，跳过。"
fi

# 安装项目依赖
if [ -f pyproject.toml ]; then
  log "检测到pyproject.toml，使用poetry安装依赖..."
  poetry install --no-interaction --with dev
  log "项目依赖安装完成"
elif [ -f requirements.txt ]; then
  log "检测到requirements.txt，使用pip安装依赖..."
  pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
  log "项目依赖安装完成"
else
  log "未检测到依赖文件，跳过依赖安装。"
fi

# 安装并激活pre-commit钩子
if [ -f .pre-commit-config.yaml ]; then
  log "检测到.pre-commit-config.yaml，激活pre-commit钩子..."
  pre-commit install
  pre-commit autoupdate
  log "pre-commit钩子安装完成"
else
  log "未检测到.pre-commit-config.yaml，跳过pre-commit钩子安装。"
fi

# 自动生成.env（如有模板）
if [ -f .env.example ] && [ ! -f .env ]; then
  log "检测到.env.example，自动生成.env"
  cp .env.example .env
  log ".env文件生成完成"
else
  log "未检测到.env.example，跳过.env文件生成。"
fi

log "容器开发环境初始化完成！"