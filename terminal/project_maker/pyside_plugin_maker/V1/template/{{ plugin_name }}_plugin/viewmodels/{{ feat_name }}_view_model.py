{{ placeholder_import_start }}
{{ placeholder_constructor_start }}
{{ placeholder_constructor_end }}
{{ placeholder_ui_start }}
{{ placeholder_ui_end }}
{{ placeholder_view_start }}
{{ placeholder_view_end }}
{{ placeholder_viewmodel_start }}
{{ placeholder_viewmodel_end }}
{{ placeholder_import_end }}

class {{ FeatName }}ViewModel(QObject):
    """
    {{ FeatName }}视图模型类
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