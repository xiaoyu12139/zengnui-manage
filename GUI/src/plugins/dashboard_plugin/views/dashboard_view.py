######import_start######
from utils import get_logger, set_style_sheet

######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
from ui_widget.dashboard_plugin import Ui_DashboardWidget
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

logger = get_logger("DashboardView")


class DashboardView(QWidget):
    """
    Dashboard视图类
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
        # 应用 Dashboard 专用样式
        set_style_sheet(self, ":/dashboard_plugin/style/dashboard.qss")

    def setup_widget(self):
        """
        设置用户界面
        """
        self.ui = Ui_DashboardWidget()
        self.ui.setupUi(self)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm

    def get_menu_name(self) -> str:
        return "Dashboard"

    
    def dashboard_init(self):
        """
        初始化 Dashboard 视图
        """
        vlayout = QVBoxLayout(self.ui.page)
        vlayout.setContentsMargins(0, 0, 0, 0)
        #获取子视图
        card_quick_option_view = self.view_model.get_quick_option_view()
        card_config_view = self.view_model.get_card_config_view()
        # 第1行
        hlayout_1 = QHBoxLayout()
        hlayout_1.addWidget(card_quick_option_view)
        hlayout_1.addStretch()
        vlayout.addLayout(hlayout_1)
        # 第2行
        hlayout_2 = QHBoxLayout()
        hlayout_2.addWidget(card_config_view)
        vlayout.addLayout(hlayout_2)
        # 添加 Spacer 占用剩余空间
        vlayout.addStretch()
