######import_start######
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class TopBarViewModel:
    """
    TopBar视图模型类
    """
    def __init__(self, context):
        super().__init__()
        self._context = context
    
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
        self._context.plugin_execute("main_window","close_main_window")
    
    def minimize_main_window(self):
        """
        最小化主窗口
        """
        self._context.plugin_execute("main_window","minimize_main_window")
    
    def maximize_main_window(self, maximize: bool):
        """
        最大化主窗口
        """
        self._context.plugin_execute("main_window","maximize_main_window", maximize)
    
    def move_main_window(self, delta):
        """
        移动主窗口
        """
        self._context.plugin_execute("main_window", "move_main_window", delta)
    
