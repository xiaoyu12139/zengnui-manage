from PySide6.QtWidgets import QMainWindow, QWidget
from plugins.ui_widget.main_window import Ui_MainWindow

class MainWindowView(QMainWindow):
    """
    主窗口视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()

    def setup_widget(self):
        """
        初始化界面
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm