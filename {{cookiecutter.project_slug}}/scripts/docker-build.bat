@echo off
REM Docker镜像构建脚本 - Windows版

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 定义变量
set IMAGE_NAME={{cookiecutter.project_slug}}
if "%1"=="" (
  set TAG=latest
) else (
  set TAG=%1
)

REM 显示构建信息
echo 正在构建 %IMAGE_NAME%:%TAG%...

REM 构建Docker镜像
docker build -t %IMAGE_NAME%:%TAG% .

REM 检查构建结果
if %ERRORLEVEL% EQU 0 (
  echo 成功构建镜像: %IMAGE_NAME%:%TAG%
  docker images | findstr "%IMAGE_NAME%"
) else (
  echo 构建失败!
  exit /b 1
)

echo 完成!
