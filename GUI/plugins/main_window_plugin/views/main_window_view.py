from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QDockWidget, QHBoxLayout, QLabel,
    QSplitter, QScrollArea, QVBoxLayout, QGraphicsDropShadowEffect
)
from ...ui_widget.main_window_plugin import Ui_MainWindow
from PySide6.QtCore import QPoint, Slot, QEvent, QTimer
from ..viewmodels import MainWindowViewModel
from utils import get_logger, set_style_sheet
from ..build.rc_qss import *

logger = get_logger("MainWindowView")

class MainWindowView(QMainWindow):
    """
    主窗口视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()
        set_style_sheet(self, ":/qss/main_window_plugin/main_window.qss")
        
    def setup_widget(self):
        """
        初始化界面
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ZengNUI Manage")
        self.resize(1200, 800)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        # 透明背景 + 阴影
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        try:
            self.setContentsMargins(12, 12, 12, 12)
        except Exception:
            pass
        self._apply_shadow()
        # 监听屏幕变化，跨屏时重建阴影并刷新
        try:
            if self.windowHandle() is not None:
                self.windowHandle().screenChanged.connect(self._on_screen_changed)
        except Exception:
            pass

        # 中心区域：左右分栏，左侧可滚动列表，右侧内容区
        # 水平分隔器
        splitter = QSplitter(Qt.Horizontal, self.ui.center_widget)
        splitter.setObjectName("centerSplitter")

        # 左侧：滚动区域 + 容器
        left_scroll = QScrollArea(splitter)
        left_scroll.setWidgetResizable(True)
        left_scroll.setObjectName("leftScroll")

        left_container = QWidget()
        left_container.setObjectName("leftContainer")
        left_vbox = QVBoxLayout(left_container)
        left_vbox.setContentsMargins(0, 0, 0, 0)
        left_vbox.setSpacing(6)
        left_vbox.setAlignment(Qt.AlignTop)

        # 暂时加入一些占位项示例（可移除或替换为真实项）
        for i in range(30):
            item = QWidget()
            item.setObjectName(f"leftItem{i}")
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(8, 6, 8, 6)
            item_layout.setSpacing(6)
            item_layout.addWidget(QLabel(f"项目 {i+1}"))
            left_vbox.addWidget(item)

        left_scroll.setWidget(left_container)

        # 右侧：内容占位
        right_content = QWidget(splitter)
        right_content.setObjectName("rightContent")
        right_vbox = QVBoxLayout(right_content)
        right_vbox.setContentsMargins(0, 0, 0, 0)
        right_vbox.setSpacing(0)
        right_vbox.addWidget(QLabel("内容区（占位）"))

        # 将分隔器放入 center_widget 的已有布局中（由 UI 定义）
        center_layout = self.ui.horizontalLayout
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addWidget(splitter)

        # 初始分配比例：左侧 1，右侧 3
        splitter.setSizes([300, 900])

        # 保存引用以便后续动态添加列表项
        self._left_container = left_container
        self._left_vbox = left_vbox
        self._right_content = right_content
        self._right_vbox = right_vbox

        left_scroll.setStyleSheet("""
        background-color: #3B3B3B;
        color: #FFFFFF;
        border: none;
        """)

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(None)
        self.ui.centralwidget.setGraphicsEffect(shadow)

    def _on_screen_changed(self, screen):
        # 屏幕变化后重建阴影并刷新，防止跨屏出现未重绘区域
        self._apply_shadow()
        self.ui.centralwidget.update()
        self.repaint()

    def changeEvent(self, event):
        # 捕获内部屏幕变化事件，延时重绘保证稳定
        if event.type() == QEvent.ScreenChangeInternal:
            QTimer.singleShot(0, lambda: (
                self._apply_shadow(),
                self.ui.centralwidget.update()
            ))
        return super().changeEvent(event)

    def moveEvent(self, event):
        # 移动时触发更新，减轻边缘透明区域的遗漏重绘
        try:
            self.ui.centralwidget.update()
        except Exception:
            pass
        return super().moveEvent(event)
        
    def set_top_widget(self, widget: QWidget):
        """
        设置顶部栏（使用 QMainWindow 的菜单栏区域）
        """
        top_layout = QHBoxLayout(self.ui.top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        top_layout.addWidget(widget)
        self.ui.top_widget.setStyleSheet("background-color: #2C2C2C;")

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
        bottom_layout = QHBoxLayout(self.ui.bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(widget)
        self.ui.bottom_widget.setStyleSheet("""
        background-color: #2C2C2C;
        color: #FFFFFF;
        """)

    def set_view_model(self, vm: MainWindowViewModel):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
        self.create_vm_sig_connect()

    def add_left_item(self, widget: QWidget):
        """
        在左侧滚动列表中新增一个 QWidget 项
        """
        if hasattr(self, "_left_vbox"):
            self._left_vbox.addWidget(widget)
    
    def create_vm_sig_connect(self):
        """
        创建视图模型信号连接
        """
        self.view_model.sig_move_main_window.connect(self.on_sig_move_main_window)
        self.view_model.sig_min_main_window.connect(self.on_sig_min_main_window)
        self.view_model.sig_max_main_window.connect(self.on_sig_max_main_window)
        self.view_model.sig_diagnostics_main_window.connect(self.on_sig_diagnostics_main_window)
        self.view_model.sig_toggle_main_window_theme.connect(self.on_sig_toggle_main_window_theme)
    
    @Slot()
    def on_sig_min_main_window(self):
        """
        最小化主窗口槽函数
        """
        self.showMinimized()

    @Slot(bool)
    def on_sig_max_main_window(self, maximize: bool):
        """
        最大化主窗口槽函数
        """
        if maximize:
            self.showMaximized()
        else:
            self.showNormal()
    
    @Slot()
    def on_sig_diagnostics_main_window(self):
        """
        诊断主窗口槽函数
        """
        logger.info("on_sig_diagnostics_main_window")
    
    @Slot()
    def on_sig_toggle_main_window_theme(self):
        """
        切换主窗口主题槽函数
        """
        logger.info("on_sig_toggle_main_window_theme")
    
    @Slot(object)
    def on_sig_move_main_window(self, pos: QPoint):
        """
        移动主窗口槽函数
        """
        # logger.info(f"move to: {pos}")
        self.move(self.pos() + pos)