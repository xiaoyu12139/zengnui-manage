# 内部包
from public import *
from command_alias import *
# 外部包
import click
from pathlib import Path

@click.command()
def update_all_configurations() -> None:
    """更新所有启动项目需要进行的配置
    """
    INFO("1.更新所有终端别名")
    reset_all_terminal_aliases(aggressive=True)
    run_command(["update-change-dir"], Path.home())
    run_command(["update-clash-proxy"], Path.home())
    SUCCESS("更新所有终端别名")