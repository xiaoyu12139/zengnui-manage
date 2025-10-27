from PySide6.QtWidgets import QWidget

class StatusBarView(QWidget):
    """
    状态栏视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm