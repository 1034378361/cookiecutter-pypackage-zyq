@echo off
REM Docker容器运行脚本 - Windows版

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 定义变量
set IMAGE_NAME={{cookiecutter.project_slug}}
if "%1"=="" (
  set TAG=latest
) else (
  set TAG=%1
)
set CONTAINER_NAME={{cookiecutter.project_slug}}-instance

REM 检查镜像是否存在
docker images %IMAGE_NAME%:%TAG% | findstr "%IMAGE_NAME%" > nul
if %ERRORLEVEL% NEQ 0 (
  echo 镜像 %IMAGE_NAME%:%TAG% 不存在，正在构建...
  call scripts\docker-build.bat %TAG%
)

REM 检查是否有同名容器在运行
docker ps -a | findstr "%CONTAINER_NAME%" > nul
if %ERRORLEVEL% EQU 0 (
  echo 发现同名容器，正在停止并移除...
  docker stop %CONTAINER_NAME% > nul 2>&1
  docker rm %CONTAINER_NAME% > nul 2>&1
)

REM 创建数据和配置目录(如果不存在)
if not exist data mkdir data
if not exist config mkdir config

REM 运行Docker容器
echo 正在启动容器 %CONTAINER_NAME% 使用镜像 %IMAGE_NAME%:%TAG%...
docker run -it --name %CONTAINER_NAME% ^
    -v "%CD%\data:/app/data" ^
    -v "%CD%\config:/app/config" ^
    %IMAGE_NAME%:%TAG% %2 %3 %4 %5 %6 %7 %8 %9

REM 显示容器状态
echo 容器状态:
docker ps -a | findstr "%CONTAINER_NAME%"
