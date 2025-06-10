#!/usr/bin/env python
import os
import pathlib
import re
import stat
import subprocess
import shutil
import sys

def print_colored(message, color="reset"):
    """打印彩色文本"""
    colors = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m"
    }
    # 使用colors.get(color, colors['reset'])获取指定颜色代码，如果不存在则使用默认颜色
    # 在消息前后添加颜色代码和重置代码，实现彩色输出
    # 在支持ANSI颜色的终端（如Linux/macOS终端、Windows的PowerShell或CMD）中可以输出彩色文本
    # 但在某些环境（如某些CI/CD系统、重定向到文件时）可能不支持颜色
    print(f"{colors.get(color, colors['reset'])}{message}{colors['reset']}")

def error(message):
    """打印错误信息"""
    print_colored(f"错误: {message}", "red")
    
def warning(message):
    """打印警告信息"""
    print_colored(f"警告: {message}", "yellow")
    
def success(message):
    """打印成功信息"""
    print_colored(f"成功: {message}", "green")
    
def info(message):
    """打印信息"""
    print_colored(f"信息: {message}", "blue")

def configure_dependencies():
    """根据项目类型配置依赖"""
    import re
    
    project_type = "{{ cookiecutter.project_type }}"
    cli_interface = "{{ cookiecutter.command_line_interface }}"
    # 使用绝对路径确保在任何工作目录下都能找到pyproject.toml
    pyproject_path = os.path.join(os.getcwd(), "pyproject.toml")
    
    # 创建备份
    backup_path = f"{pyproject_path}.bak"
    try:
        shutil.copy2(pyproject_path, backup_path)
        info(f"已创建配置文件备份: {backup_path}")
    except Exception as e:
        warning(f"创建配置备份失败: {str(e)}")
    
    # 读取原始文件
    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 保存处理前的内容以便对比
    original_content = content
    
    try:
        # 1. 处理核心依赖部分
        # 查找dependencies列表部分
        dependencies_section = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if dependencies_section:
            # 获取依赖列表内容
            deps_list_content = dependencies_section.group(1)
            # 将内容分割成单独的依赖项
            deps_lines = [line.strip() for line in deps_list_content.split(',') if line.strip()]
            
            # 筛选依赖项
            filtered_deps = []
            for dep in deps_lines:
                dep_cleaned = dep.strip()
                
                # 移除不需要的依赖
                if project_type != "Web Service" and any(pkg in dep_cleaned for pkg in ["fastapi", "uvicorn", "pydantic"]):
                    continue
                if project_type != "Data Science" and any(pkg in dep_cleaned for pkg in ["numpy", "pandas", "matplotlib", "scikit-learn"]):
                    continue
                if cli_interface == "No command-line interface" and "typer" in dep_cleaned:
                    continue
                if cli_interface == "Argparse" and "typer" in dep_cleaned:
                    continue
                
                # 保留有效的依赖
                filtered_deps.append(dep_cleaned)
            
            # 重新构建依赖列表
            new_deps_content = ",\n    ".join(filtered_deps)
            new_deps_section = f"dependencies = [\n    {new_deps_content}\n]"
            
            # 替换原始依赖部分
            content = content.replace(dependencies_section.group(0), new_deps_section)
        
        # 2. 重新构建可选依赖部分
        # 找到optional-dependencies部分的开始
        optional_deps_section = re.search(r'^\[project\.optional-dependencies\].*?(?=^\[|\Z)', content, re.DOTALL | re.MULTILINE)
        
        if optional_deps_section:
            # 提取当前dev部分的内容
            dev_deps_match = re.search(r'dev\s*=\s*\[(.*?)\]', optional_deps_section.group(0), re.DOTALL)
            dev_deps = dev_deps_match.group(1) if dev_deps_match else ""
            
            # 创建新的可选依赖内容
            new_optional_deps = "[project.optional-dependencies]\ndev = [" + dev_deps + "]\n\n"
            
            # 添加特定项目类型的依赖组
            if project_type == "Web Service":
                new_optional_deps += """# Web Service 特定依赖
web = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
]

"""
            
            if project_type == "Data Science":
                new_optional_deps += """# Data Science 特定依赖
data = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "scikit-learn>=1.3.0",
]

"""
            
            # 添加特定项目类型的开发依赖组
            if project_type == "Web Service":
                web_dev_match = re.search(r'web-dev\s*=\s*\[(.*?)\]', optional_deps_section.group(0), re.DOTALL)
                if web_dev_match:
                    web_dev_deps = web_dev_match.group(1)
                    new_optional_deps += "web-dev = [" + web_dev_deps + "]\n\n"
            
            if project_type == "Data Science":
                data_dev_match = re.search(r'data-dev\s*=\s*\[(.*?)\]', optional_deps_section.group(0), re.DOTALL)
                if data_dev_match:
                    data_dev_deps = data_dev_match.group(1)
                    new_optional_deps += "data-dev = [" + data_dev_deps + "]\n\n"
            
            if project_type == "CLI Tool":
                cli_dev_match = re.search(r'cli-dev\s*=\s*\[(.*?)\]', optional_deps_section.group(0), re.DOTALL)
                if cli_dev_match:
                    cli_dev_deps = cli_dev_match.group(1)
                    new_optional_deps += "cli-dev = [" + cli_dev_deps + "]\n\n"
            
            # 构建full-dev依赖
            active_dev_groups = ["dev"]
            if project_type == "Web Service":
                active_dev_groups.append("web-dev")
            elif project_type == "Data Science":
                active_dev_groups.append("data-dev")
            elif project_type == "CLI Tool":
                active_dev_groups.append("cli-dev")
                
            new_optional_deps += f"""full-dev = [
    {', '.join([f'"{group}"' for group in active_dev_groups])}
]
"""
            
            # 替换可选依赖部分
            content = content.replace(optional_deps_section.group(0), new_optional_deps)
    
    except Exception as e:
        warning(f"处理依赖时出错: {str(e)}")
        warning("尝试使用备份文件恢复原始配置")
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, pyproject_path)
                info("已恢复原始配置")
            return
        except Exception as restore_error:
            error(f"恢复备份失败: {str(restore_error)}")
            return
    
    # 仅当内容有变化时写入文件
    if content != original_content:
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        changes = []
        if project_type in ["Web Service", "Data Science"]:
            changes.append(f"项目类型({project_type})")
        if cli_interface != "Typer":
            changes.append(f"命令行接口({cli_interface})")
            
        if changes:
            info(f"已根据{' 和 '.join(changes)}配置依赖")
        else:
            info("已配置项目依赖")
    else:
        info("依赖配置未发生变化")

def normalize_gitattributes():
    """确保.gitattributes文件使用规范的行尾。"""
    gitattributes = pathlib.Path('.gitattributes')
    if gitattributes.exists():
        # 读取内容
        content = gitattributes.read_text()
        # 替换所有换行符为LF (Unix风格)
        content = content.replace('\r\n', '\n')
        # 重写文件
        gitattributes.write_text(content)
        info("已规范化 .gitattributes 行尾")

def check_pyenv_installed():
    """检查pyenv是否已安装"""
    try:
        # 尝试执行pyenv命令
        subprocess.run(["pyenv", "--version"],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_pdm_installed():
    """检查PDM是否已安装"""
    try:
        # 尝试执行pdm命令
        subprocess.run(["pdm", "--version"],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def create_python_version_file():
    """创建.python-version文件用于pyenv"""
    python_version = "{{ cookiecutter.python_version }}"
    # 如果python_version是列表，取第一个元素
    if isinstance(python_version, list):
        python_version = python_version[0]
    with open('.python-version', 'w') as f:
        f.write(python_version + '\n')
    info(f"已创建.python-version文件，指定Python版本: {python_version}")

def is_git_repo(path: str) -> bool:
    """检查指定路径是否为git仓库"""
    return (pathlib.Path(path) / ".git").is_dir()

def setup_project_by_type():
    """根据项目类型设置项目结构"""
    project_type = "{{ cookiecutter.project_type }}"
    info(f"正在设置项目类型: {project_type}")
    
    # 处理命令行接口
    cli_interface = "{{ cookiecutter.command_line_interface }}"
    if cli_interface == "No command-line interface":
        cli_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'cli.py')
        if cli_file.exists():
            cli_file.unlink()
            info("已移除cli.py文件 (不使用命令行接口)")
    else:
        info(f"使用 {cli_interface} 作为命令行接口")
    
    # 处理项目类型特定设置
    if project_type == "Standard Library":
        info("设置标准库项目结构")
        # 标准库项目默认结构保持不变
        
        # 清理非标准库项目特定文件
        app_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'app.py')
        if app_file.exists():
            app_file.unlink()
            
        data_analysis_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'data_analysis.py')
        if data_analysis_file.exists():
            data_analysis_file.unlink()
    
    elif project_type == "CLI Tool":
        info("设置命令行工具项目结构")
        # 确保cli.py存在
        if cli_interface == "No command-line interface":
            warning("CLI工具项目建议使用命令行接口，但您选择了不使用命令行接口")
        
        # 清理非CLI工具特定文件
        app_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'app.py')
        if app_file.exists():
            app_file.unlink()
            
        data_analysis_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'data_analysis.py')
        if data_analysis_file.exists():
            data_analysis_file.unlink()
            
        # 创建examples目录
        examples_dir = pathlib.Path('examples')
        examples_dir.mkdir(exist_ok=True)
        
        # 创建示例文件
        example_file = examples_dir / 'cli_example.py'
        with open(example_file, 'w') as f:
            f.write('''"""CLI工具使用示例。"""
import sys
from pathlib import Path

# 将项目根目录添加到PATH中，以便导入包
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from {{ cookiecutter.project_slug }}.cli import main

if __name__ == "__main__":
    sys.exit(main())
''')
        info("已创建CLI工具示例文件")
    
    elif project_type == "Web Service":
        info("设置Web服务项目结构")
        # 确保app.py存在，已在模板中创建
        
        # 清理非Web服务特定文件
        data_analysis_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'data_analysis.py')
        if data_analysis_file.exists():
            data_analysis_file.unlink()
        
        # 在docs中添加API文档目录
        api_docs_dir = pathlib.Path('docs', 'api')
        api_docs_dir.mkdir(exist_ok=True, parents=True)
        
        # 创建API端点文档文件
        endpoint_doc = api_docs_dir / 'endpoints.md'
        with open(endpoint_doc, 'w') as f:
            f.write('''# API端点文档

## 基础端点

### GET /

返回API欢迎信息。

**响应**:
```json
{
  "message": "欢迎使用 {{ cookiecutter.project_name }} API",
  "version": "x.y.z"
}
```

### GET /health

健康检查端点，用于监控系统。

**响应**:
```json
{
  "status": "healthy"
}
```

### GET /info

返回API详细信息。

**响应**:
```json
{
  "name": "{{ cookiecutter.project_name }}",
  "description": "{{ cookiecutter.project_short_description }}",
  "version": "x.y.z",
  "author": "{{ cookiecutter.full_name }}",
  "endpoints": ["/", "/health", "/info"]
}
```
''')
        info("已创建API文档")
    
    elif project_type == "Data Science":
        info("设置数据科学项目结构")
        
        # 创建数据目录结构
        data_dir = pathlib.Path('data')
        data_dir.mkdir(exist_ok=True)
        
        for subdir in ['raw', 'processed', 'external']:
            (data_dir / subdir).mkdir(exist_ok=True)
        
        # 创建notebooks目录
        notebooks_dir = pathlib.Path('notebooks')
        notebooks_dir.mkdir(exist_ok=True)
        
        # 创建示例notebook
        example_notebook = notebooks_dir / 'exploration.ipynb'
        with open(example_notebook, 'w') as f:
            f.write('''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# {{ cookiecutter.project_name }} - 数据探索\\n\\n此Notebook用于数据探索和分析。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 导入核心库\\nimport pandas as pd\\nimport numpy as np\\nimport matplotlib.pyplot as plt\\nimport seaborn as sns\\n\\n# 设置可视化样式\\nplt.style.use('ggplot')\\nsns.set_theme()\\n\\n# 导入项目包\\nfrom {{ cookiecutter.project_slug }}.data_analysis import *"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 载入数据\\n\\n首先，让我们载入示例数据集。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 使用项目的data_analysis模块加载数据\\n# df = load_dataset('path/to/your/data.csv')\\n\\n# 这里使用内置数据集作为示例\\nfrom sklearn.datasets import load_iris\\niris = load_iris()\\ndf = pd.DataFrame(iris.data, columns=iris.feature_names)\\ndf['target'] = iris.target\\ndf.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 数据分析\\n\\n使用项目中的分析函数进行数据探索。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 分析数据集\\nstats = analyze_dataset(df)\\n\\n# 显示基本统计信息\\nprint(f\"行数: {stats['rows']}\\n列数: {stats['columns']}\\n\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 生成可视化\\n# 注意：在实际使用中，你需要传入一个有效的输出目录\\noutput_dir = Path('./output')\\noutput_dir.mkdir(exist_ok=True)\\n\\n# 创建可视化\\n# 注意：在notebook中，我们直接在notebook中显示图表\\n\\n# 相关性热图\\nplt.figure(figsize=(10, 8))\\nsns.heatmap(df.corr(), annot=True, cmap='coolwarm')\\nplt.title('特征相关性热图')\\nplt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 模型训练\\n\\n使用项目中的模型训练函数进行训练。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 训练简单模型\\nmodel_data = train_model(\\n    df=df,\\n    target_column='target',\\n    feature_columns=None,  # 使用所有数值列作为特征\\n    test_size=0.2,\\n    random_state=42\\n)\\n\\n# 显示模型评估指标\\nprint(\"模型评估指标:\\n\")\\nfor metric, value in model_data['metrics'].items():\\n    if metric != 'feature_importance':\\n        print(f\"{metric}: {value:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 显示特征重要性\\nfeature_imp = pd.Series(model_data['metrics']['feature_importance'], index=model_data['feature_columns'])\\nfeature_imp.sort_values(ascending=False, inplace=True)\\n\\nplt.figure(figsize=(10, 6))\\nsns.barplot(x=feature_imp, y=feature_imp.index)\\nplt.title('特征重要性')\\nplt.tight_layout()\\nplt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}''')
        info("已创建数据科学目录结构和示例notebook")
        
        # 创建README.md以便在数据目录中提供指南
        data_readme = data_dir / 'README.md'
        with open(data_readme, 'w') as f:
            f.write('''# 数据目录

此目录用于存放项目相关数据。

## 目录结构

- `raw/`: 存放原始数据
- `processed/`: 存放处理后的数据
- `external/`: 存放来自外部源的数据

## 数据文件

请在此目录中存放数据文件，但不要将大型数据文件提交到Git仓库。
建议在`.gitignore`中添加数据文件的忽略规则，并在文档中说明如何获取数据。
''')
    
    elif project_type == "Custom":
        info("设置自定义项目结构 (最小化)")
        # 只保留最基本的结构，清理所有特定项目类型的文件
        app_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'app.py')
        if app_file.exists():
            app_file.unlink()
            
        data_analysis_file = pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'data_analysis.py')
        if data_analysis_file.exists():
            data_analysis_file.unlink()
    
    # 许可证处理
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        license_file = pathlib.Path('LICENSE')
        if license_file.exists():
            license_file.unlink()
            info("已移除LICENSE文件 (不使用开源许可证)")
    else:
        info(f"使用开源许可证: {{ cookiecutter.open_source_license }}")

if __name__ == '__main__':
    print_colored("\n===================== 创建成功 =====================", "green")
    success("开始项目后处理...")

    # 根据项目类型设置项目
    setup_project_by_type()

    # 优化项目依赖
    try:
        configure_dependencies()
        success("已根据项目类型和命令行接口选择优化项目依赖")
    except Exception as e:
        warning(f"配置依赖时出错: {str(e)}")
        warning("请手动检查并调整pyproject.toml文件中的依赖")

    # 规范化.gitattributes行尾
    normalize_gitattributes()

    # 初始化git仓库
    if shutil.which("git") is None:
        warning("未检测到git，请先安装Git后再使用本项目的版本控制功能\n")
    elif not is_git_repo(os.getcwd()):
        try:
            subprocess.run(["git", "init", "-b", "main"], check=True)
            success("已初始化git仓库\n")
        except Exception as e:
            warning(f"初始化git仓库失败: {e}\n")
    else:
        info("当前目录已是git仓库，跳过初始化\n")

    # 创建.python-version文件
    create_python_version_file()

    # 检测pyenv是否安装
    if not check_pyenv_installed():
        warning("未检测到pyenv安装")
        warning("为获得最佳体验，建议安装pyenv管理Python版本")
        warning("安装指南: https://github.com/pyenv/pyenv#installation")
        selected_version = "{{ cookiecutter.python_version }}"
        if isinstance(selected_version, list):
            selected_version = selected_version[0]
        warning(f"安装完成后，请在项目目录运行: pyenv install {selected_version}\n")
    else:
        selected_version = "{{ cookiecutter.python_version }}"
        if isinstance(selected_version, list):
            selected_version = selected_version[0]
        info(f"pyenv已安装，您可以运行: pyenv install {selected_version}\n")

    # 检测PDM是否安装
    pdm_installed = check_pdm_installed()
    # 在pre_gen_project.py中已经显示了警告，这里只提供安装指导
    warning("本项目使用PDM进行依赖管理")
    info("使用以下方式一键安装PDM环境：")
    info("   - Linux/macOS: 执行1. dos2unix ./scripts/init.sh")
    info("   - Linux/macOS: 执行2. ./scripts/init.sh")
    info("   - Windows: 双击运行 run_init.bat")
    info("   - 任何系统: python init.py")
    info("详细文档请访问: https://pdm.fming.dev/latest/#installation\n")
    info("PDM已安装，项目可以直接使用PDM进行依赖管理\n")

    # 项目创建完成提示
    success("项目 {{ cookiecutter.project_name }} 创建成功!")
    success(f"项目路径: {os.path.abspath('.')}")
    success("接下来，建议执行:")
    print_colored(f"  1. cd {{ cookiecutter.project_slug }}", "cyan")
    if not pdm_installed:
        print_colored("  2. 根据您的系统运行相应的初始化脚本(run_init.bat/init.sh/init.py)", "cyan")
        print_colored("  3. pdm install -d  # 安装所有依赖（包括开发依赖）", "cyan")
        print_colored("  4. 开始开发吧!", "cyan")
    else:
        print_colored("  2. pdm install -d  # 安装所有依赖（包括开发依赖）", "cyan")
        print_colored("  3. 开始开发吧!", "cyan")
    
    print_colored("\n项目类型：{{ cookiecutter.project_type }}", "purple")
    print_colored("命令行接口：{{ cookiecutter.command_line_interface }}", "purple")
    print_colored(f"Python版本：{{ cookiecutter.python_version }}", "purple")
