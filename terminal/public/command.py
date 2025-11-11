# 内部库
from .logger import *
# 外部库
from pathlib import Path
import subprocess
import click
import sys
import locale
from typing import Tuple, List, Dict, Any

# Windows 下阻止新窗口弹出（如不需要可删）
if sys.platform.startswith("win"):
    CREATE_NO_WINDOW = 0x08000000
    run_kwargs = {
        "creationflags": CREATE_NO_WINDOW,
        # 使用系统首选编码以避免控制台输出的乱码和解码错误
        "encoding": locale.getpreferredencoding(False),
        # 容错处理，避免 UnicodeDecodeError 导致线程异常
        "errors": "replace",
    }
else:
    run_kwargs = {
        # 非 Windows 默认使用 UTF-8（大多数 POSIX 系统）
        "encoding": "utf-8",
        "errors": "replace",
    }
RUN_KWARGS: Dict[str, Any] = run_kwargs


def run_command(command: List[str], cwd: Path) -> Tuple[int, str]:
    """执行 命令。

    Args:
        command (str): 要执行的命令列表
        cwd (Path): 执行命令的工作目录

    Returns:
        int: 0 成功，-1 失败
        str: 输出结果
    """
    try:
        result_out = "null"
        command_str = " ".join(command)
        result = subprocess.run(
            command_str,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            shell=True,
            **RUN_KWARGS,
        )
        result.check_returncode()
        result_out = (result.stdout or "").strip()
        click.secho(f"✔ command: {' '.join(command)} @ {cwd}", fg="green")
        return 0, result_out
    except Exception as e:
        ERROR(f"command: {' '.join(command)} @ {cwd} 执行失败, 错误信息: {e}")
        return -1, ""
