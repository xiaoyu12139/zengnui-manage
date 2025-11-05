from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt
from core import Global
from ...ui_widget.settings_plugin import Ui_SettingsWidget

class SettingsView(QWidget):
    """
    设置视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
    
    def setup_widget(self):
        """
        设置用户界面
        """
        self.ui = Ui_SettingsWidget()
        self.ui.setupUi(self)
        # self.setStyleSheet("background-color: red;")
        
    
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
        
    def get_menu_name(self) -> str:
        return "Settings"
