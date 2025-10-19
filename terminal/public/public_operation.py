import subprocess
import click
from pathlib import Path
from typing import Tuple
from public.command import run_command
from typing import List
import click
import questionary
from public.logger import WARNING, INFO, ERROR, SUCCESS


def get_input(msg: str) -> Tuple[int, str]:
    """获取输入

    Args:
        msg (str): 提示信息

    Returns:
        Tuple[int, str]: 错误码，获取到的输入值
    """
    input_str = questionary.text("请输入新分支名：").ask()
    if not input_str:
        ERROR("分支名不能为空...")
        return -1, "error"
    return 0, input_str


def action_select(actions: List[str]) -> Tuple[any, List[str]]:
    """创建选择输入模式

    Args:
        actions (List[str]): 选择列表

    Returns:
        Tuple[any, List[str]]: action选中对象，选择列表
    """
    action = questionary.select(
        "请选择要执行的操作：",
        choices=actions,
    ).ask()
    return action, actions


def confirm_conitnue(msg: str) -> bool:
    """确认是否继续操作

    Args:
        msg (str): _description_

    Returns:
        bool: _description_
    """
    return questionary.confirm(msg).ask()
