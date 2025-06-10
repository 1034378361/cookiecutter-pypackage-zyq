@echo off
echo 正在启动项目初始化...

rem 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装或不在PATH中，请先安装Python！
    exit /b 1
)

rem 运行Python初始化脚本
python "%~dp0init.py"

if %errorlevel% neq 0 (
    echo 初始化失败，请检查错误信息。
    exit /b %errorlevel%
)

echo 初始化完成！
