from PySide6.QtWidgets import QWidget
from ...ui_widget.dashboard_plugin import Ui_DashboardWidget
from PySide6.QtCore import Qt
from utils import set_style_sheet, get_logger
from ..build.rc_qss import *
from core import Global
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

logger = get_logger("DashboardView")

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
    
    def assemble_view(self):
        """
        装配视图，将 UI 元素与视图模型绑定
        """
        card_quick_option_view = Global().command_manager.execute_command("activate_card_quick_option_view")
        card_config_view = Global().command_manager.execute_command("activate_card_config_view")
        vlayout = QVBoxLayout(self.ui.contentWidget)
        vlayout.setContentsMargins(0, 0, 0, 0)
        # 第1行
        hlayout_1 = QHBoxLayout()
        hlayout_1.addWidget(card_quick_option_view)
        hlayout_1.addStretch()
        
        # 第2行
        hlayout_2 = QHBoxLayout()
        hlayout_2.addWidget(card_config_view)

        vlayout.addLayout(hlayout_1)
        vlayout.addLayout(hlayout_2)
        # 添加 Spacer 占用剩余空间
        vlayout.addStretch()