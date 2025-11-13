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

class StatusBarViewModel:
    """
    StatusBar视图模型类
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