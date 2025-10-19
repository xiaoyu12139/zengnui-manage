from pathlib import Path
import subprocess
import click
import questionary
import sys
from typing import Tuple, List

# Windows 下阻止新窗口弹出（如不需要可删）
if sys.platform.startswith("win"):
    CREATE_NO_WINDOW = 0x08000000
    RUN_KWARGS = {"creationflags": CREATE_NO_WINDOW}
else:
    RUN_KWARGS = {}


def run_command(command: List[str], cwd: Path) -> Tuple[int, str]:
    """执行 命令。

    Args:
        command (str): 要执行的命令列表
        cwd (Path): 执行命令的工作目录

    Returns:
        int: 0 成功，-1 失败
        str: 输出结果
    """
    result_out = "null"
    result = subprocess.run(
        " ".join(command),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        shell=True,
        encoding="utf-8",
        **RUN_KWARGS,
    )
    result.check_returncode()
    result_out = result.stdout.strip()
    click.secho(f"✔ command: {' '.join(command)} @ {cwd}", fg="green")
    return 0, result_out
