# 内部包
from public import *
from .ops_add_plugin_feat import add_plugin_feat
from .ops_del_plugin_feat import del_plugin_feat
from .ops_create_plugin import create_plugin
# 外部包
import click
import questionary
from pathlib import Path

def cli_create_plugin():
    """
    创建插件
    """
    plugin_name = questionary.text("请输入插件名称：").ask()
    feat_name = questionary.text("请输入组件名称：").ask()
    plugin_dir = questionary.text("请输入插件目录：").ask()
    if not plugin_dir:
        # 将plugin_dir设置为执行命令时所在的目录
        plugin_dir = Path.cwd()
        INFO(f"将插件目录设置为：{plugin_dir}")
    create_plugin(Path(plugin_dir), plugin_name, feat_name)

def cli_add_component():
    """
    添加组件
    """
    plugin_name = questionary.text("请输入插件名称：").ask()
    feat_name = questionary.text("请输入组件名称：").ask()
    plugin_dir = questionary.text("请输入插件目录：").ask()
    if not plugin_dir:
        # 将plugin_dir设置为执行命令时所在的目录
        plugin_dir = Path.cwd()
        INFO(f"将插件目录设置为：{plugin_dir}")
    add_plugin_feat(Path(plugin_dir), plugin_name, feat_name)

def cli_delete_plugin():
    """
    删除插件
    """
    plugin_name = questionary.text("请输入插件名称：").ask()
    feat_name = questionary.text("请输入组件名称：").ask()
    plugin_dir = questionary.text("请输入插件目录：").ask()
    if not plugin_dir:
        # 将plugin_dir设置为执行命令时所在的目录
        plugin_dir = Path.cwd()
        INFO(f"将插件目录设置为：{plugin_dir}")
    del_plugin_feat(Path(plugin_dir), plugin_name, feat_name)

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
        cli_create_plugin()
    elif choice == "添加组件":
        cli_add_component()
    elif choice == "删除插件":
        cli_delete_plugin()


if __name__ == "__main__":
    main()