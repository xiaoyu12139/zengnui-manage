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
