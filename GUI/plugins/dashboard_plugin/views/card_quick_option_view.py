from PySide6.QtWidgets import QWidget
from ...ui_widget.dashboard_plugin import Ui_CardQuickOptionWidget
from PySide6.QtCore import Qt
from utils import set_style_sheet
from ..build.rc_qss import *

class CardQuickOptionView(QWidget):
    """
    卡片快捷操作视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
        # 应用 CardQuickOption 专用样式
        set_style_sheet(self, ":/qss/dashboard_plugin/card_quick_option.qss")
        self.setFixedWidth(230)
    
    def setup_widget(self):
        """
        设置用户界面
        """
        try:
            self.ui = Ui_CardQuickOptionWidget()
            self.ui.setupUi(self)
        except Exception as e:
            logger.error(f"Error setting up widget: {e}")
        
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
