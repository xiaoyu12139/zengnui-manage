from core import Global
from utils import get_logger

logger = get_logger("MainWindowViewModel")

class MainWindowViewModel:
    """
    主窗口视图模型类
    """
    def __init__(self, context):
        self._context = context
        self._win_id = ""
        self._view_id = ""
    
    def set_window_id(self, win_id: str, view_id):
        """
        设置主窗口ID
        """
        self._win_id = win_id
        self._view_id = view_id
    
    def close_main_window(self):
        """
        关闭主窗口
        """
        logger.info("close_main_window")
        Global().views_manager.close(self._win_id)
