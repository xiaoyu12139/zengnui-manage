from core import Global
from utils import get_logger
from PySide6.QtCore import Signal, QPoint, QObject
from PySide6.QtWidgets import QWidget

logger = get_logger(f"SubGenerateSettingWidgetViewModel")

class SubGenerateSettingWidgetViewModel(QObject):
    """
    SubGenerateSettingWidget 视图模型类
    """

    def __init__(self, context):
        super().__init__()
        self._context = context
        self._win_id = ""
        self._view_id = ""
    
    def set_window_id(self, win_id: str, view_id):
        """
        设置主窗口ID
        """
        self._win_id = win_id
        self._view_id = view_id
    