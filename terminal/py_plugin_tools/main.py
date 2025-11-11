# 内部包
from public import *
# 外部包
import click
import questionary

@click.command()
def main():
    choice = questionary.select(
        "请选择操作：",
        choices=[
            "创建插件",
            "添加组件",
            "删除插件",
            "退出"
        ]
    ).ask()
    if choice == "创建插件":
        ...
    elif choice == "添加组件":
        ...
    elif choice == "删除插件":
        ...


if __name__ == "__main__":
    main()