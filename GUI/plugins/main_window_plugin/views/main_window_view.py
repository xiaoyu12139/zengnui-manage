from PySide6.QtWidgets import QWidget
from plugins.ui_widget.main_window import Ui_MainWindow

class MainWindowView(QWidget):
    """
    主窗口视图类
    """
    def __init__(self):
        self.setup_widget()

    def setup_widget(self):
        """
        初始化界面
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)