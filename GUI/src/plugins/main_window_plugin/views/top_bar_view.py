######import_start######
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
# from ...ui_widget.top_bar_plugin import Ui_TopBar
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Slot


class TopBarView(QWidget):
    """
    TopBar视图类
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setup_widget()
        self._top_widget = self
        self._dragging = False
        self._drag_pos = None
        self._max_button_state = True
        set_style_sheet(self, ":/qss/top_bar_plugin/top_bar.qss")

    def setup_widget(self):
        """
        设置用户界面
        """
        self.ui = Ui_TopWidget()
        self.ui.setupUi(self)
        self.ui.btn_close.setIcon(QIcon(":/img/top_bar_plugin/close.svg"))
        self.ui.btn_close.setAutoRaise(True)
        self.ui.btn_close.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_close.setToolTip("关闭窗口")
        self.ui.btn_close.clicked.connect(self.on_btn_close_click)

        self.ui.btn_max.setIcon(QIcon(":/img/top_bar_plugin/maximize.svg"))
        self.ui.btn_max.setAutoRaise(True)
        self.ui.btn_max.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_max.setToolTip("最大化窗口")
        self.ui.btn_max.clicked.connect(self.on_btn_max_click)

        self.ui.btn_min.setIcon(QIcon(":/img/top_bar_plugin/minimize.svg"))
        self.ui.btn_min.setAutoRaise(True)
        self.ui.btn_min.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_min.setToolTip("最小化窗口")
        self.ui.btn_min.clicked.connect(self.on_btn_min_click)

        self.ui.btn_night.setIcon(QIcon(":/img/top_bar_plugin/theme.svg"))
        self.ui.btn_night.setAutoRaise(True)
        self.ui.btn_night.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_night.setToolTip("切换主题")
        self.ui.btn_night.clicked.connect(self.on_btn_night_click)

        self.ui.btn_diaginostics.setIcon(QIcon(":/img/top_bar_plugin/bell.svg"))
        self.ui.btn_diaginostics.setAutoRaise(True)
        self.ui.btn_diaginostics.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.btn_diaginostics.setToolTip("诊断")
        self.ui.btn_diaginostics.clicked.connect(self.on_btn_diaginostics_click)

        # 设置logo并按高度缩放
        self._logo_pix = QPixmap(":/img/top_bar_plugin/logo.png")
        self._update_logo_size()

        # 安装事件过滤器
        self.installEventFilter(self)

    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm

    def resizeEvent(self, event):
        # 顶部栏尺寸变化时，按高度重新缩放 logo
        self._update_logo_size()
        return super().resizeEvent(event)

    def _update_logo_size(self):
        # 将 logo 按 top_bar 内可用高度进行等比缩放
        if hasattr(self, "_logo_pix") and not self._logo_pix.isNull():
            target_h = self.ui.top_theme.height() or self.height()
            if target_h and target_h > 0:
                scaled = self._logo_pix.scaledToHeight(
                    int(target_h - 10), Qt.SmoothTransformation
                )
                self.ui.top_theme.setPixmap(scaled)

    def eventFilter(self, obj, event):
        if obj is getattr(self, "_top_widget"):
            if (
                event.type() == QEvent.MouseButtonPress
                and event.button() == Qt.LeftButton
            ):
                self._drag_pos = event.globalPosition().toPoint()
                self._dragging = True
                return True
            elif event.type() == QEvent.MouseMove and getattr(
                self, "_dragging", False
            ):
                delta = event.globalPosition().toPoint() - self._drag_pos
                Global().command_manager.execute_command(
                    "move_main_window", delta
                )
                self._drag_pos = event.globalPosition().toPoint()
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                self._dragging = False
                return True
            elif event.type() == QEvent.MouseButtonDblClick:
                # 顶栏双击最大化/还原
                # self._toggle_max_restore()
                return True
        return super().eventFilter(obj, event)

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

        if not self._max_button_state:
            self.ui.btn_max.setIcon(QIcon(":/img/top_bar_plugin/maximize.svg"))
            self.ui.btn_max.setToolTip("最大化窗口")
            Global().command_manager.execute_command(
                "maximize_main_window", self._max_button_state
            )
        else:
            self.ui.btn_max.setIcon(QIcon(":/img/top_bar_plugin/restore.svg"))
            self.ui.btn_max.setToolTip("还原窗口")
            Global().command_manager.execute_command(
                "maximize_main_window", self._max_button_state
            )
        self._max_button_state = not self._max_button_state

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
        Global().command_manager.execute_command("toggle_main_window_theme")

    @Slot()
    def on_btn_diaginostics_click(self):
        """
        诊断按钮点击事件
        """
        Global().command_manager.execute_command("diagnostics_main_window")
