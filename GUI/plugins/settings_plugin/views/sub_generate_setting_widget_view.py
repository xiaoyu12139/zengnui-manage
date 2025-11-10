from PySide6.QtWidgets import QWidget
from ...ui_widget.settings_plugin import Ui_SubGenerateSettingWidget
from PySide6.QtCore import Qt
from utils import set_style_sheet
from ..build.rc_qss import *
from core import Global
from utils import get_logger

logger = get_logger(f"SubGenerateSettingWidgetView")

class SubGenerateSettingWidgetView(QWidget):
    """
    SubGenerateSettingWidget 视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
        # 应用 sub_generate_setting_widget 专用样式
        # set_style_sheet(self, f":/qss/settings_plugin/sub_generate_setting_widget.qss")
    
    def setup_widget(self):
        """
        设置用户界面
        """
        try:
            self.ui = Ui_SubGenerateSettingWidget()
            self.ui.setupUi(self)
        except Exception as e:
            logger.error(f"Error setting up widget: {e}")
        
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
    
        