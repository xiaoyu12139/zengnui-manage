import click
from public.logger import *
from public.check_terminal_type import get_terminal_type
from public.alias_manager import set_terminal_alias
import os
import tempfile
from pathlib import Path
import subprocess

@click.command()
def cli_proxy():
    """Clash Terminal Proxy
    """
    set_terminal_alias('clash', 'echo 1234', 'cmd')
    set_terminal_alias('clash', 'echo 1234', 'powershell')
    set_terminal_alias('clash', 'echo 1234', 'bash')
    


if __name__ == '__main__':
    cli_proxy()