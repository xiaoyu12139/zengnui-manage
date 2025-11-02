from PySide6.QtWidgets import QWidget
from ...ui_widget.main_window_plugin import Ui_TopWidget
from PySide6.QtGui import QIcon
from ..build.rc_icon import *
from PySide6.QtCore import Slot
from core import Global
from PySide6.QtCore import Qt



class TopBarView(QWidget):
    """
    顶部栏视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()
        
    def setup_widget(self):
        """
        初始化UI组件
        """
        self.ui = Ui_TopWidget()
        self.ui.setupUi(self)
        self.ui.btn_close.setIcon(QIcon(":/top_bar_plugin/close.svg"))
        self.ui.btn_close.setAutoRaise(True)
        self.ui.btn_close.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_close.setToolTip("关闭窗口")
        self.ui.btn_close.clicked.connect(self.on_btn_close_click)

        self.ui.btn_max.setIcon(QIcon(":/top_bar_plugin/maximize.svg"))
        self.ui.btn_max.setAutoRaise(True)
        self.ui.btn_max.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_max.setToolTip("最大化窗口")
        self.ui.btn_max.clicked.connect(self.on_btn_max_click)
        
        self.ui.btn_min.setIcon(QIcon(":/top_bar_plugin/minimize.svg"))
        self.ui.btn_min.setAutoRaise(True)  
        self.ui.btn_min.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_min.setToolTip("最小化窗口")
        self.ui.btn_min.clicked.connect(self.on_btn_min_click)
        
        self.ui.btn_night.setIcon(QIcon(":/top_bar_plugin/theme.svg"))
        self.ui.btn_night.setAutoRaise(True)
        self.ui.btn_night.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_night.setToolTip("切换主题")
        self.ui.btn_night.clicked.connect(self.on_btn_night_click)  
        
        self.ui.btn_diaginostics.setIcon(QIcon(":/top_bar_plugin/bell.svg"))
        self.ui.btn_diaginostics.setAutoRaise(True)
        self.ui.btn_diaginostics.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_diaginostics.setToolTip("诊断")
        self.ui.btn_diaginostics.clicked.connect(self.on_btn_diaginostics_click)

    
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
    
    @Slot()
    def on_btn_close_click(self):
        """
        关闭窗口按钮点击事件
        """
        Global().command_manager.execute_command("close_main_window")
    
    @Slot()
    def on_btn_max_click(self):
        """
        最大化窗口按钮点击事件
        """
        Global().command_manager.execute_command("maximize_main_window")
    
    @Slot()
    def on_btn_min_click(self):
        """
        最小化窗口按钮点击事件
        """
        Global().command_manager.execute_command("minimize_main_window")
    
    @Slot()
    def on_btn_night_click(self):
        """
        切换主题按钮点击事件
        """
        Global().command_manager.execute_command("toggle_theme")
    
    @Slot()
    def on_btn_diaginostics_click(self):
        """
        诊断按钮点击事件
        """
        Global().command_manager.execute_command("diagnostics")
    
    