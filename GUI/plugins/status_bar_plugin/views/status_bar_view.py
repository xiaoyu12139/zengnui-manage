from PySide6.QtWidgets import QWidget
from ...ui_widget.main_window_plugin import Ui_StatusBarWidget

class StatusBarView(QWidget):
    """
    状态栏视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()
    
    def setup_widget(self):
        """
        初始化UI组件
        """
        self.ui = Ui_StatusBarWidget()
        self.ui.setupUi(self)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm