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

或者下载 [压缩包](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/archive/master.zip)：

```bash
curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master
```

获取源码后，您可以使用Poetry安装它：

```bash
cd {{ cookiecutter.project_slug }}
poetry install
```

## 开发安装

如果您想参与 {{ cookiecutter.project_name }} 的开发，可以安装带有开发依赖的版本：

```bash
git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
cd {{ cookiecutter.project_slug }}
poetry install --with dev
```
