from PySide6.QtWidgets import QWidget
from ...ui_widget.dashboard_plugin import Ui_DashboardWidget
from PySide6.QtCore import Qt
from utils import set_style_sheet
from ..build.rc_qss import *

class DashboardView(QWidget):
    """
    仪表盘视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
        # 应用 Dashboard 专用样式
        set_style_sheet(self, ":/qss/dashboard_plugin/dashboard.qss")
    
    def setup_widget(self):
        """
        设置用户界面
        """
        try:
            self.ui = Ui_DashboardWidget()
            self.ui.setupUi(self)
        except Exception as e:
            logger.error(f"Error setting up widget: {e}")
        
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
    
    def get_menu_name(self) -> str:
        return "Dashboard"
