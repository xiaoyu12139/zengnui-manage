from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from .app_logging import get_logger

logger = get_logger("StyleSheet Utils")

def get_qss(qss_name: str) -> str:
    """
    获取QSS样式表

    Args:
        qss_name (str): QSS文件名, ":/qss/top_bar_plugin/top_bar.qss"
    
    Returns:
        str: QSS样式表
    """
    qss_text = ""
    qss_file = QFile(qss_name)
    if qss_file.exists() and qss_file.open(QFile.ReadOnly):
        # readAll 返回 QByteArray，这里转为 str
        qss_text = bytes(qss_file.readAll()).decode("utf-8")
        logger.info(f"加载资源样式: {qss_name}")
        qss_file.close()
    else:
        logger.info(f"资源样式不存在或无法打开: {qss_name}")
    return qss_text

def set_style_sheet(obj: QWidget, qss_name: str):
    """
    设置应用样式表

    Args:
        obj (QWidget): 要设置样式表的对象
        qss_name (str): QSS文件名, ":/qss/top_bar_plugin/top_bar.qss"
    """
    qss_text = get_qss(qss_name)
    obj.setStyleSheet(qss_text)
