# 安装指南

本文档提供了{{ cookiecutter.project_name }}的多种安装方法和环境配置说明。

## 系统要求

* Python {{ cookiecutter.requires_python if cookiecutter.requires_python is defined else '3.8' }}或更高版本
* pip 21.0或更高版本（推荐）

## 从PyPI安装（推荐）

最简单的安装方法是使用pip从PyPI安装：

```bash
pip install {{ cookiecutter.project_slug }}
```

这将安装{{ cookiecutter.project_name }}的最新稳定版本。

## 从源码安装

如果您需要最新的开发版本或想要参与项目开发，可以从源码安装：

```bash
# 克隆仓库
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# 安装基本包
pip install -e .

# 安装开发依赖（如果要进行开发）
pip install -e ".[dev]"
```

## 使用虚拟环境（推荐）

为避免依赖冲突，推荐在虚拟环境中安装：

### 使用venv

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Linux/macOS）
source venv/bin/activate

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装
pip install {{ cookiecutter.project_slug }}
```

### 使用conda

```bash
# 创建conda环境
conda create -n {{ cookiecutter.project_slug }} python={{ cookiecutter.requires_python if cookiecutter.requires_python is defined else '3.8' }}
conda activate {{ cookiecutter.project_slug }}

# 安装
pip install {{ cookiecutter.project_slug }}
```

## 特定版本安装

安装特定版本：

```bash
pip install {{ cookiecutter.project_slug }}==0.1.0
```

安装最新的开发版：

```bash
pip install --pre {{ cookiecutter.project_slug }}
```

## 离线安装

对于无法访问互联网的环境，可以下载wheel包进行离线安装：

1. 在有网络连接的环境中下载wheel包：

```bash
pip download {{ cookiecutter.project_slug }} -d ./packages
```

2. 将packages目录复制到目标环境并安装：

```bash
pip install --no-index --find-links=./packages {{ cookiecutter.project_slug }}
```

{% if cookiecutter.project_type == "Web Service" %}
## 使用Docker

如果您使用Docker，我们提供了预配置的Dockerfile和docker-compose.yml：

```bash
# 构建Docker镜像
docker-compose build

# 运行容器
docker-compose up -d
```

您也可以直接使用预构建的镜像：

```bash
docker pull {{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}:latest
docker run -p 8000:8000 {{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}:latest
```
{% endif %}

## 验证安装

安装完成后，您可以验证安装是否成功：

```bash
python -c "import {{ cookiecutter.project_slug }}; print({{ cookiecutter.project_slug }}.__version__)"
```

{% if cookiecutter.command_line_interface != "No command-line interface" %}
或者通过命令行工具检查：

```bash
{{ cookiecutter.project_slug }} --version
```
{% endif %}

## 依赖说明

{{ cookiecutter.project_name }}依赖以下主要库：

* 核心依赖：自动安装
{% if cookiecutter.command_line_interface == "Typer" %}  * Typer: 命令行接口{% elif cookiecutter.command_line_interface == "Argparse" %}  * Argparse: 命令行接口（Python标准库）{% endif %}
  * typing-extensions: 增强的类型支持

* 可选依赖：需要额外安装
  * 开发依赖：`pip install {{ cookiecutter.project_slug }}[dev]`
  * 文档依赖：`pip install {{ cookiecutter.project_slug }}[docs]`
  * 测试依赖：`pip install {{ cookiecutter.project_slug }}[test]`

## 常见问题

### 依赖冲突

如果遇到依赖冲突，尝试以下方法：

```bash
# 在隔离环境中安装
pip install --isolated {{ cookiecutter.project_slug }}

# 或强制重新安装依赖
pip install --upgrade --force-reinstall {{ cookiecutter.project_slug }}
```

### 权限问题

如果遇到权限问题，尝试：

```bash
# Linux/macOS
pip install --user {{ cookiecutter.project_slug }}

# 或使用管理员权限
sudo pip install {{ cookiecutter.project_slug }}
```

### 安装特定Python版本

如果需要为特定Python版本安装：

```bash
python3.9 -m pip install {{ cookiecutter.project_slug }}
```

## 开发环境设置

如果您计划参与项目开发，请按照以下步骤设置开发环境：

1. 克隆仓库并安装开发依赖：

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
pip install -e ".[dev]"
```

2. 安装pre-commit钩子：

```bash
pre-commit install
```

3. 运行测试确认环境设置正确：

```bash
pytest
```

现在您已准备好开始开发！

### 安装 GitHub CLI (gh)

如果您需要使用 GitHub CLI 工具（如 `gh` 命令），可以按照以下步骤在 Ubuntu/Debian 系统上安装：
```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
        && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```


### 删除 GitHub Workflows 历史记录

如果需要删除 GitHub 仓库中的 workflows 运行历史，可以使用 [gh-actions-delete-runs](https://github.com/rokroskar/gh-actions-delete-runs) 工具。以下是在本地快速删除所有 workflow 运行历史的命令（需已安装 [GitHub CLI](https://cli.github.com/) 并登录）：

```bash
$repoFull = "1034378361/test_template"
gh run list --limit 1000 --json databaseId -q '.[].databaseId' | % { gh api --method DELETE repos/$repoFull/actions/runs/$_ }
```
