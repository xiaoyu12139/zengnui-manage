from core import Global
from utils import logger

def main():
    """
    主函数
    """
    # 加载主窗口插件
    plugin_controller = Global().plugin_controller
    plugin_controller.load_plugin("main_window_plugin")
    # 启动软件命令
    command_controller = Global().command_controller
    # command_controller.execute_command("startup")


if __name__ == "__main__":
    main()