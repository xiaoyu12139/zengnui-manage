class MainWindowViewModel:
    """
    主窗口视图模型类
    """
    def __init__(self, context):
        self._context = context
        self._window_id = ""
    
    def set_window_id(self, window_id: str):
        """
        设置主窗口ID
        """
        self._window_id = window_id