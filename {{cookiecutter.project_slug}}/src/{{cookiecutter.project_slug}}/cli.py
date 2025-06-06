"""Console script for {{cookiecutter.project_slug}}."""
import {{cookiecutter.project_slug}}

{% if cookiecutter.command_line_interface == 'Typer' %}
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for {{cookiecutter.project_slug}}."""
    console.print("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")



if __name__ == "__main__":
    app()
    # 此文件实现了{{cookiecutter.project_slug}}的命令行接口
    # 使用Typer库构建CLI应用程序，提供友好的命令行体验
    #
    # 主要功能:
    # - app = typer.Typer(): 创建Typer应用实例
    # - @app.command()装饰器: 将函数注册为CLI命令
    # - main(): 主命令函数，当前仅显示占位消息
    # - console = Console(): 使用Rich库创建控制台对象，用于美化输出
    #
    # 使用方法:
    # 1. 直接运行模块: python -m {{cookiecutter.project_slug}}.cli
    # 2. 安装后使用入口点: {{cookiecutter.project_slug}}
    #
    # 扩展方法:
    # - 添加新命令: 使用@app.command()装饰新函数
    # - 添加子命令: 创建子Typer实例并挂载到主app
    # - 添加参数: 使用typer.Argument()和typer.Option()
{% elif cookiecutter.command_line_interface == 'Argparse' %}
import argparse
import sys


def main():
    """Console script for {{cookiecutter.project_slug}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
    # 此文件实现了{{cookiecutter.project_slug}}的命令行接口
    # 使用标准库argparse构建CLI应用程序
    #
    # 主要功能:
    # - parser = argparse.ArgumentParser(): 创建命令行参数解析器
    # - main(): 主函数，解析命令行参数并执行
    #
    # 使用方法:
    # 1. 直接运行模块: python -m {{cookiecutter.project_slug}}.cli
    # 2. 安装后使用入口点: {{cookiecutter.project_slug}}
    #
    # 扩展方法:
    # - 添加新参数: 使用parser.add_argument()
    # - 添加子命令: 使用parser.add_subparsers()
{% endif %}
