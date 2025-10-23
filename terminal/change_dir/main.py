from pathlib import Path
from public.logger import *
from public.public_operation import *
from public.alias_manager import set_terminal_alias
import json
from .change_dir_powershel_utils import *
from .change_dir_cmd_utils import *
import click

# 脚本文件所在目录
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

# json中的label
LABEL_DIR = "directories"
LABEL_PATH = 'path'
LABEL_DESC = 'desc'

def config():
    """读取配置文件返回json对象

    Returns:
        dict: 返回json字符串转的dict
    """
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            json_obj = json.load(f)
    return json_obj

@click.command()
def main():
    """功能入口
    """
    # 1. 读取配置文件
    INFO("读取配置文件...")
    config_json = config()

    directories = config_json.get(LABEL_DIR, {})
    if not isinstance(directories, dict) or not directories:
        ERROR("配置文件中未找到有效的目录配置 'directories'")
        return

    for key, value in directories.items():
        INFO(f"name: {key} dir: {value.get(LABEL_PATH)} desc: {value.get(LABEL_DESC)}")

    # 2. 生成别名配置（默认别名为目录键名，并提供帮助别名）
    aliases = {key: key for key in directories.keys()}
    aliases['help'] = 'ds-help'

    # 3.创建 powershell 目录切换
    INFO("更新 powershell 目录切换...")
    for key,value in directories.items():
        # operator = f"cd {value.get(LABEL_PATH)}"
        operator = f"""
        $OldDir = Get-Location
        Set-Location {value.get(LABEL_PATH)}
        Write-Host "✓ Switched to {value.get(LABEL_PATH)}: $TargetDir" -ForegroundColor Green
        Write-Host "  (from: $OldDir)" -ForegroundColor Gray
        """
        error_state, error_msg = set_terminal_alias(key, operator, "powershell")
        if error_state:
            SUCCESS(f"设置 alias: {key} path: {value.get(LABEL_PATH)} 成功设置目录别名切换.")
    # 4.创建 cmd 目录切换
    INFO("更新 cmd 目录切换...")
    for key, value in directories.items():
        operator = f'cd /d "{value.get(LABEL_PATH)}" $T echo Switched to "{value.get(LABEL_PATH)}"'
        error_state, error_msg = set_terminal_alias(key, operator, "cmd")
        if error_state:
            SUCCESS(f"设置 alias: {key} path: {value.get(LABEL_PATH)} 成功设置目录别名切换.{error_msg}" )
    # 5.创建 git bash 目录切换
    INFO("更新 git bash 目录切换...")
    for key, value in directories.items():
        bash_path = value.get(LABEL_PATH).replace("\\", "/").replace(":", "")
        bash_path = f'"/{bash_path}"'
        operator = f'prev="$PWD"; cd "{bash_path}" && echo "Switched to {bash_path}" && echo && echo "(from: $prev)"'
        error_state, error_msg = set_terminal_alias(key, operator, "bash")
        if error_state:
            SUCCESS(f"设置 alias: {key} path: {value.get(LABEL_PATH)} 成功设置目录别名切换.")
   