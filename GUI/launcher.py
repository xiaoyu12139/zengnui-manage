from core import Global
from utils import logger
import sys
import os
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor
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
    # 使用 Fusion 样式以确保样式表对控件绘制的控制更一致
    try:
        app.setStyle(QStyleFactory.create("Fusion"))
        logger.info("应用样式: Fusion")
    except Exception:
        pass
    # 先尝试从 Qt 资源加载 default.qss（:/qss/default.qss）
    try:
        # 导入资源模块以注册 qss 与图标资源（rc_* 在导入时会调用 qInitResources）
        from plugins.main_window_plugin.build import rc_qss  # noqa: F401
        from plugins.main_window_plugin.build import rc_icon  # noqa: F401
        qss_file = QFile(":/qss/default.qss")
        if qss_file.exists() and qss_file.open(QFile.ReadOnly):
            # readAll 返回 QByteArray，这里转为 str
            qss_text = bytes(qss_file.readAll()).decode("utf-8")
            app.setStyleSheet(qss_text)
            logger.info("加载资源样式: :/qss/default.qss")
            qss_file.close()
        else:
            logger.info("资源样式不存在或无法打开: :/qss/default.qss")
    except Exception as e:
        logger.error(f"加载资源样式失败: {e}")
    # 加载全局样式（QSS），如存在 default.css 则应用
    try:
        css_path = os.path.join(os.path.dirname(__file__), "resource", "css", "default.css")
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                # 附加到现有样式，允许 file-css 覆盖资源 qss 的局部设置（如滚动条图标）
                app.setStyleSheet(app.styleSheet() + "\n" + f.read())
            logger.info(f"加载文件样式: {css_path}")
        else:
            logger.info("未找到全局样式文件: resource/css/default.css")
    except Exception as e:
        logger.error(f"加载全局样式失败: {e}")
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