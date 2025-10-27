from core import Global
from utils import logger
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication

def make_dark_palette(app: QApplication):
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(18, 20, 23))
    pal.setColor(QPalette.WindowText, QColor(234, 238, 243))
    pal.setColor(QPalette.Base, QColor(15, 18, 22))
    pal.setColor(QPalette.AlternateBase, QColor(27, 31, 38))
    pal.setColor(QPalette.ToolTipBase, QColor(27, 31, 38))
    pal.setColor(QPalette.ToolTipText, QColor(234, 238, 243))
    pal.setColor(QPalette.Text, QColor(234, 238, 243))
    pal.setColor(QPalette.Button, QColor(23, 26, 31))
    pal.setColor(QPalette.ButtonText, QColor(234, 238, 243))
    pal.setColor(QPalette.BrightText, QColor(255, 107, 107))
    pal.setColor(QPalette.Highlight, QColor(91, 124, 250))
    pal.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(pal)

def main():
    """
    主函数
    """
    # 创建应用实例
    app = QApplication(sys.argv)
    # 加载主窗口插件
    plugin_manager = Global().plugin_manager
    plugin_manager.load_plugin("main_window_plugin")
    # 启动软件命令
    command_manager = Global().command_manager
    command_manager.execute_command("startup")
    # 应用深色主题
    make_dark_palette(app)
    # 启动事件循环，保持窗口不退出
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())