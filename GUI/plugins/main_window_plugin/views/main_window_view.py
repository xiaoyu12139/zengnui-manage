from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QDockWidget
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

    def set_top_widget(self, widget: QWidget):
        """
        设置顶部栏（使用 QMainWindow 的菜单栏区域）
        """
        self.setMenuWidget(widget)

    def set_diagnostic_widget(self, widget: QWidget):
        """
        设置诊断停靠区（右侧 Dock）
        """
        dock = QDockWidget("消息与诊断", self)
        dock.setWidget(widget)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def set_status_bar_widget(self, widget: QWidget):
        """
        将状态栏视图加入到 QStatusBar 的永久区域
        """
        self.statusBar().addPermanentWidget(widget)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm