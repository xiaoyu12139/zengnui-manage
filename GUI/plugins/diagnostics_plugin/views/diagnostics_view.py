from PySide6.QtWidgets import QWidget
from ...ui_widget.diagnostics_plugin_widget import Ui_DiagnosticsWidget

class DiagnosticsView(QWidget):
    """
    诊断视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()
    
    def setup_widget(self):
        """
        初始化UI组件
        """
        self.ui = Ui_DiagnosticsWidget()
        self.ui.setupUi(self)
    
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm