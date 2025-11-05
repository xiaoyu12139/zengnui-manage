from PySide6.QtWidgets import QWidget
from core import Global

class SettingsView(QWidget):
    """
    设置视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
    
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
        
    def get_menu_name(self) -> str:
        return "Settings"
