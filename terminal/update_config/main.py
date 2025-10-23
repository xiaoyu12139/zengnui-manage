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
    reset_all_terminal_aliases()
    INFO("更新别名目录")
    run_command(["update-change-dir"], Path.home())
    INFO("更新别名代理")
    run_command(["update-clash-proxy"], Path.home())
    SUCCESS("更新所有终端别名")
    WARNING("更新所有配置完成，请重启终端等")

if __name__ == "__main__":
    update_all_configurations()
