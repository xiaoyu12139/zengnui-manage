from core import Global
from utils import logger, get_qss
import sys
import os
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtCore import QFile


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
    # 设置应用名称和显示名称，影响托盘消息来源显示
    try:
        app.setApplicationName("ZengNUI Manage")
        app.setApplicationDisplayName("ZengNUI Manage")
        app.setOrganizationName("ZengNUI")
        app.setOrganizationDomain("zengnui.local")
    except Exception:
        pass
    # 在 Windows 平台设置 AppUserModelID，避免托盘通知显示为“python”
    try:
        if sys.platform.startswith("win"):
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "ZengNUI.Manage"
            )
    except Exception:
        # 不影响正常运行
        pass
    # 使用 Fusion 样式以确保样式表对控件绘制的控制更一致
    try:
        app.setStyle(QStyleFactory.create("Fusion"))
        logger.info("应用样式: Fusion")
    except Exception:
        pass
    # 尝试从 Qt 资源加载 default.qss（:/qss/default.qss）
    try:
        # 导入资源模块以注册 qss 与图标资源（rc_* 在导入时会调用 qInitResources）
        from plugins.main_window_plugin.build import rc_qss  # noqa: F401
        from plugins.main_window_plugin.build import rc_icon  # noqa: F401

        qss_content = get_qss(":/qss/default.qss")
        app.setStyleSheet(app.styleSheet() + "\n" + qss_content)
        # 设置应用窗口图标（影响 Windows 任务栏显示）
        try:
            app.setWindowIcon(QIcon(":/img/top_bar_plugin/z_logo.svg"))
            logger.info("已设置应用图标为 :/img/top_bar_plugin/z_logo.svg")
        except Exception as e:
            logger.error(f"设置应用图标失败: {e}")
    except Exception as e:
        logger.error(f"加载资源样式失败: {e}")
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
