from core import Global
from utils import get_logger
from PySide6.QtCore import Signal, QPoint, QObject

logger = get_logger("MainWindowViewModel")

class MainWindowViewModel(QObject):
    """
    主窗口视图模型类
    """

    sig_move_main_window = Signal(object)
    sig_min_main_window = Signal()
    sig_max_main_window = Signal(bool)
    sig_diagnostics_main_window = Signal()
    sig_toggle_main_window_theme = Signal()

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
    
    def close_main_window(self):
        """
        关闭主窗口
        """
        logger.info("close_main_window")
        Global().views_manager.close(self._win_id)
    
    def move_main_window(self, pos: QPoint):
        """
        移动主窗口
        """
        # logger.info(f"move_main_window: {pos}")
        self.sig_move_main_window.emit(pos)

    def toggle_main_window_theme(self):
        """
        切换主窗口主题
        """
        logger.info("toggle_main_window_theme")
        self.sig_toggle_main_window_theme.emit()
    
    def diagnostics_main_window(self):
        """
        诊断主窗口
        """
        logger.info("diagnostics_main_window")
        self.sig_diagnostics_main_window.emit()
    
    def minimize_main_window(self):
        """
        最小化主窗口
        """
        logger.info("minimize_main_window")
        self.sig_min_main_window.emit()
    
    def maximize_main_window(self, maximize: bool):
        """
        最大化主窗口
        """
        logger.info("maximize_main_window")
        self.sig_max_main_window.emit(maximize)