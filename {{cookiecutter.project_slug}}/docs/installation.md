# 安装指南

## 稳定版本

要安装 {{ cookiecutter.project_name }}，请在终端中运行以下命令：

```bash
pip install {{ cookiecutter.project_slug }}
```

这是安装 {{ cookiecutter.project_name }} 的首选方法，因为它将始终安装最新的稳定版本。

如果您还没有安装 [pip](https://pip.pypa.io)，可以参考 [Python安装指南](http://docs.python-guide.org/en/latest/starting/installation/) 获取帮助。

## 从源码安装

{{ cookiecutter.project_name }} 的源代码可以从 [GitHub仓库](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}) 下载。

您可以克隆公共仓库：

```bash
git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
```

获取源码后，您可以使用统一安装脚本来设置您的环境：

```bash
cd {{ cookiecutter.project_slug }}
python setup.py
```

这个脚本会自动:

1. 检测您的操作系统和Python版本
2. 创建虚拟环境
3. 安装项目依赖
4. 配置开发环境

您可以使用以下选项：

- 使用 `--dev` 选项安装开发依赖：

  ```bash
  python setup.py --dev
  ```

- 使用 `--yes` 或 `-y` 选项自动确认所有提示：

  ```bash
  python setup.py --yes
  ```

## 使用Makefile

项目还提供了Makefile，可以使用以下命令进行安装：

```bash
# 安装基本版本
make install

# 安装开发版本
make dev-install

# 创建虚拟环境并安装开发依赖
make venv
```

## 环境激活

安装完成后，您需要激活虚拟环境：

### Windows

```bash
# CMD
.venv\Scripts\activate.bat

# PowerShell
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source .venv/bin/activate
```

激活环境后，您可以开始使用{{ cookiecutter.project_name }}进行开发。

## Docker安装

项目也支持使用Docker进行开发和测试：

```bash
# 构建Docker镜像
make docker-build

# 运行Docker容器
make docker-run
```
