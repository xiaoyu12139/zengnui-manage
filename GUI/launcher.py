from core import Global
from utils import logger
from pathlib import Path

def main():
    """
    主函数
    """
    # 加载主窗口插件
    plugin_manager = Global().plugin_manager
    plugin_manager.load_plugin("main_window_plugin")
    # 启动软件命令
    command_manager = Global().command_manager
    command_manager.execute_command("startup")


if __name__ == "__main__":
    main()