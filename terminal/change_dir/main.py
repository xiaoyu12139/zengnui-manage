from pathlib import Path
from public.logger import *
from public.public_operation import *
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

    # 3. 创建 PowerShell 模块
    INFO("创建 PowerShell 模块...")
    success, module_path, error = create_powershell_module(
        "DirectorySwitch", directories, aliases
    )

    if not success:
        ERROR(f"模块创建失败: {error}")
        return

    SUCCESS(f"✓ PowerShell 模块已创建: {module_path}")

    # 4. 测试模块（使用帮助别名）
    INFO("测试模块...")
    test_success, test_output = test_powershell_module("DirectorySwitch", aliases['help'])

    if test_success:
        SUCCESS("✓ 模块测试成功")
        INFO("现在你可以使用以下命令:")
        for key, cfg in directories.items():
            alias = aliases.get(key, key)
            INFO(f"  {alias} - 切换到 {cfg.get(LABEL_DESC)}")
        INFO(f"  {aliases['help']} - 显示帮助信息")
        INFO("")
        INFO("示例用法: powershell -Command 'Import-Module DirectorySwitch; ds-help'")
    else:
        WARNING(f"模块测试失败: {test_output}")

    # 5. 创建并测试 CMD 宏（DOSKEY）
    INFO("创建 CMD 宏...")
    cmd_success, cmd_dir, cmd_error = create_cmd_macros("DirectorySwitch", directories, aliases)
    if not cmd_success:
        ERROR(f"CMD 宏创建失败: {cmd_error}")
    else:
        SUCCESS(f"✓ CMD 宏已创建: {cmd_dir}")
        INFO("测试 CMD 宏...")
        cmd_test_success, cmd_test_output = test_cmd_macros("DirectorySwitch", aliases['help'])
        if cmd_test_success:
            SUCCESS("✓ CMD 宏测试成功")
            INFO("在 CMD 中使用方法:")
            INFO(f"  call \"{cmd_dir / 'load.cmd'}\"  加载宏到当前会话")
            for key, cfg in directories.items():
                alias = aliases.get(key, key)
                INFO(f"  {alias} - 切换到 {cfg.get(LABEL_DESC)}")
            INFO(f"  {aliases['help']} - 显示帮助信息")

            # 启用 CMD 自动加载宏（AutoRun），使新开 CMD 会话自动拥有别名
            INFO("启用 CMD 自动加载（AutoRun）...")
            auto_success, auto_msg = enable_cmd_autoload_macros("DirectorySwitch")
            if auto_success:
                SUCCESS("✓ 已配置 CMD AutoRun 自动加载宏。新开 CMD 会话会自动拥有上述别名。")
            else:
                WARNING(f"自动加载设置失败: {auto_msg}")
                INFO("你可以继续使用手动加载脚本，或稍后再运行命令以重试。")
        else:
            WARNING(f"CMD 宏测试失败: {cmd_test_output}")