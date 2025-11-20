######import_start######
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
from ui_widget.dashboard_plugin import Ui_CardConfigWidget
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

class CardConfigView(QWidget):
    """
    CardConfig视图类
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
        self.ui = Ui_CardConfigWidget()
        self.ui.setupUi(self)
        
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm

    
    