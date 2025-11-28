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

class DashboardViewModel:
    """
    Dashboard视图模型类
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
    
    def get_quick_option_view(self):
        """
        获取 CardQuickOption 视图
        """
        return self._context.plugin_execute("card_quick_option","get_card_quick_option")
    
    def get_card_config_view(self):
        """
        获取 CardConfig 视图
        """
        return self._context.plugin_execute("card_config","get_card_config")