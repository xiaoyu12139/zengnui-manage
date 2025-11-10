from PySide6.QtCore import Qt, QPoint, Slot, QEvent, QTimer
from PySide6.QtGui import QColor, QMouseEvent, QCursor, QIcon, QAction
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QDockWidget, QHBoxLayout, QLabel,
    QSplitter, QScrollArea, QVBoxLayout, QGraphicsDropShadowEffect,
    QSizeGrip, QSystemTrayIcon, QMenu
)
from ...ui_widget.main_window_plugin import Ui_MainWindow
from ..viewmodels import MainWindowViewModel
from utils import get_logger, set_style_sheet
from ..build.rc_qss import *
from ..build.rc_xml import *
from utils.xml_ops import get_menu_list
from core import Global

logger = get_logger("MainWindowView")

class MenuItemWidget(QWidget):
    """
    左侧菜单项小部件
    """
    current_selected_item = None
    current_hover_item = None

    def __init__(self, menu_name: str, view_id: str, main_window_view_id: str, parent: QWidget = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        item_layout = QHBoxLayout(self)
        item_layout.setContentsMargins(10, 5, 10, 5)
        item_widget = QWidget(self)
        # 用于 QSS 选择器与 :hover 的对象名与属性
        item_widget.setObjectName("menuItem")
        item_widget.setAttribute(Qt.WA_Hover, True)
        item_widget.setAttribute(Qt.WA_StyledBackground, True)
        item_widget.setMouseTracking(True)
        item_layout.addWidget(item_widget)
        inner_layout = QHBoxLayout(item_widget)
        inner_layout.setContentsMargins(8, 10, 8, 10)
        label = QLabel(menu_name)
        label.setObjectName("menuItemLabel")
        label.setAttribute(Qt.WA_StyledBackground, True)
        # 使标签本身可以响应 :hover 选择器
        label.setAttribute(Qt.WA_Hover, True)
        label.setMouseTracking(True)
        inner_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)
        # 颜色改为代码控制：基础、悬停、选中
        self._base_color = "#A1A1AA"
        self._hover_color = "#EAEFF3"
        self._selected_color = "#FFFFFF"
        # 默认未选中时使用基础颜色
        label.setStyleSheet(f"color: {self._base_color};")

        item_widget.setProperty("selected", False)
        self.view_widget_id = view_id
        self.main_window_view_id = main_window_view_id

        self._item_widget = item_widget
        self._label = label
        # 安装事件过滤器以处理悬停与离开
        self._item_widget.installEventFilter(self)
        self._label.installEventFilter(self)
        self._is_selected = False
    
    def set_select(self, is_select: bool):
        """
        设置选中状态
        """
        self._is_selected = bool(is_select)
        if is_select:
            # 标记选中并将文字改为选中颜色
            self._item_widget.setProperty("selected", True)
            self._item_widget.style().unpolish(self._item_widget)
            self._item_widget.style().polish(self._item_widget)
            self._label.setStyleSheet(f"color: {self._selected_color};")
            MenuItemWidget.current_selected_item = self
            try:
                Global().views_manager.fill_widget_with_execution(self.main_window_view_id, self.view_widget_id, "show_menu_pane")
            except Exception:
                pass
        else:
            # 取消选中恢复为基础颜色
            self._item_widget.setProperty("selected", False)
            self._item_widget.style().unpolish(self._item_widget)
            self._item_widget.style().polish(self._item_widget)
            self._label.setStyleSheet(f"color: {self._base_color};")
    
    # 点击事件
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if MenuItemWidget.current_selected_item is not None:
                MenuItemWidget.current_selected_item.set_select(False)
            MenuItemWidget.current_selected_item = self
            self.set_select(True)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        # 悬停颜色在事件过滤器里处理，这里保持默认
        return super().mouseMoveEvent(event)

    def eventFilter(self, obj, event):
        # 通过事件过滤器处理悬停颜色切换
        if obj is self._item_widget or obj is self._label:
            et = event.type()
            if et in (QEvent.Enter, QEvent.HoverEnter):
                if not self._is_selected:
                    self._label.setStyleSheet(f"color: {self._hover_color};")
            elif et in (QEvent.Leave, QEvent.HoverLeave):
                if not self._is_selected:
                    self._label.setStyleSheet(f"color: {self._base_color};")
        return super().eventFilter(obj, event)


class MainWindowView(QMainWindow):
    """
    主窗口视图类
    """
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.menu_list = get_menu_list(":/xml/menu.xml")
        self.menu_list = []
        self.setup_widget()
        set_style_sheet(self, ":/qss/main_window_plugin/main_window.qss")
        self.menu_widget_list = []

        # 初始化自定义边缘拖拽缩放行为
        self._resize_margin = 8
        self._resizing = False
        self._resize_dir = None  # 'left','right','top','bottom','tl','tr','bl','br'
        self._press_pos_global = QPoint()
        self._start_geom = self.geometry()
        try:
            # 同时在主窗口层面启用鼠标跟踪，保证边缘（含内容边距区域）可命中
            self.setMouseTracking(True)
        except Exception:
            pass
        # 初始化系统托盘图标与菜单
        try:
            self._tray = QSystemTrayIcon(QIcon(":/img/top_bar_plugin/z_logo.svg"), self)
            self._tray.setToolTip("ZengNUI Manage")
            tray_menu = QMenu()
            act_show = QAction("显示窗口", self)
            act_exit = QAction("退出", self)
            tray_menu.addAction(act_show)
            tray_menu.addSeparator()
            tray_menu.addAction(act_exit)
            self._tray.setContextMenu(tray_menu)
            act_show.triggered.connect(self._restore_from_tray)
            act_exit.triggered.connect(self._exit_app)
            self._tray.activated.connect(self._on_tray_activated)
            self._tray.show()
        except Exception:
            self._tray = None
        
    def setup_widget(self):
        """
        初始化界面
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ZengNUI Manage")
        self.resize(MainWindowView.WINDOW_WIDTH, MainWindowView.WINDOW_HEIGHT)
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
        left_scroll.setMinimumWidth(123)

        left_container = QWidget()
        left_container.setObjectName("leftContainer")
        left_vbox = QVBoxLayout(left_container)
        left_vbox.setContentsMargins(0, 10, 0, 0)
        left_vbox.setSpacing(0)
        left_vbox.setAlignment(Qt.AlignTop)

        # 暂时加入一些占位项示例（可移除或替换为真实项）
        if self.menu_list:
            for menu_name in self.menu_list:
                item = MenuItemWidget(menu_name)
                left_vbox.addWidget(item)

        left_scroll.setWidget(left_container)

        # 右侧：内容占位
        right_scroll = QScrollArea(splitter)
        right_scroll.setWidgetResizable(True)
        right_scroll.setObjectName("rightScroll")

        right_content = QWidget()
        right_content.setObjectName("rightContent")
        right_vbox = QVBoxLayout(right_content)
        right_vbox.setContentsMargins(0, 0, 0, 0)
        right_vbox.setSpacing(0)
        right_vbox.addWidget(QLabel("内容区（占位）"))

        right_scroll.setWidget(right_content)

        # 将分隔器放入 center_widget 的已有布局中（由 UI 定义）
        center_layout = self.ui.horizontalLayout
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        center_layout.addWidget(splitter)

        # 初始分配比例：左侧 1，右侧 3
        splitter.setSizes([123, MainWindowView.WINDOW_WIDTH-123])

        # 保存引用以便后续动态添加列表项
        self._left_container = left_container
        self._left_vbox = left_vbox
        self._right_content = right_content
        self._right_vbox = right_vbox

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

    def _on_tray_activated(self, reason):
        # 单击或双击托盘图标显示窗口
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self._restore_from_tray()

    def _restore_from_tray(self):
        self.showNormal()
        try:
            self.activateWindow()
        except Exception:
            pass

    def _exit_app(self):
        # 托盘菜单退出时真正关闭应用
        try:
            if self._tray:
                self._tray.hide()
        except Exception:
            pass
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()

    def closeEvent(self, event):
        # 点击关闭时，隐藏到系统托盘而不退出
        if hasattr(self, "_tray") and self._tray is not None:
            event.ignore()
            self.hide()
            try:
                # 提示气泡（可选）
                self._tray.showMessage(
                    "ZengNUI Manage",
                    "应用已最小化到托盘，右键托盘图标可退出",
                    QSystemTrayIcon.Information,
                    3000,
                )
            except Exception:
                pass
        else:
            return super().closeEvent(event)
        return None
    
    # 主窗口层面的命中检测（相对于 QMainWindow 自身坐标）
    def _hit_test_window(self, pos: QPoint):
        r = self.rect()
        m = self._resize_margin
        left = pos.x() <= m
        right = pos.x() >= r.width() - m
        top = pos.y() <= m
        bottom = pos.y() >= r.height() - m
        if left and top:
            return 'tl'
        if right and top:
            return 'tr'
        if left and bottom:
            return 'bl'
        if right and bottom:
            return 'br'
        if left:
            return 'left'
        if right:
            return 'right'
        if top:
            return 'top'
        if bottom:
            return 'bottom'
        return None

    def _update_cursor_window(self, edge: Optional[str]):
        if edge in ('left', 'right'):
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif edge in ('top', 'bottom'):
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif edge in ('tl', 'br'):
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif edge in ('tr', 'bl'):
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    # 执行缩放
    def _perform_resize(self, global_pos: QPoint):
        if not self._resizing or self.isMaximized():
            return
        delta = global_pos - self._press_pos_global
        g = self._start_geom
        min_w = max(1, self.minimumSize().width())
        min_h = max(1, self.minimumSize().height())

        new_x, new_y = g.x(), g.y()
        new_w, new_h = g.width(), g.height()

        if self._resize_dir in ('left', 'tl', 'bl'):
            new_w = max(min_w, g.width() - delta.x())
            new_x = g.x() + (g.width() - new_w)
        if self._resize_dir in ('right', 'tr', 'br'):
            new_w = max(min_w, g.width() + delta.x())
        if self._resize_dir in ('top', 'tl', 'tr'):
            new_h = max(min_h, g.height() - delta.y())
            new_y = g.y() + (g.height() - new_h)
        if self._resize_dir in ('bottom', 'bl', 'br'):
            new_h = max(min_h, g.height() + delta.y())

        self.setGeometry(new_x, new_y, new_w, new_h)

    # 主窗口层面的鼠标事件：保证边缘（包括内容边距区域）也能缩放
    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            if self._resizing:
                self._perform_resize(event.globalPosition().toPoint())
            else:
                edge = self._hit_test_window(event.position().toPoint())
                self._update_cursor_window(edge)
        except Exception:
            pass
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton and not self.isMaximized():
                edge = self._hit_test_window(event.position().toPoint())
                if edge:
                    self._resizing = True
                    self._resize_dir = edge
                    self._press_pos_global = event.globalPosition().toPoint()
                    self._start_geom = self.geometry()
                    return
        except Exception:
            pass
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton and self._resizing:
                self._resizing = False
                self._resize_dir = None
                return
        except Exception:
            pass
        return super().mouseReleaseEvent(event)
        
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
        bottom_layout = self.ui.bottom_widget.layout()
        if bottom_layout is None:
            bottom_layout = QHBoxLayout(self.ui.bottom_widget)
            bottom_layout.setContentsMargins(0, 0, 0, 0)
            bottom_layout.setSpacing(0)
        bottom_layout.addWidget(widget)
        self.ui.bottom_widget.setStyleSheet("""
        background-color: #2C2C2C;
        color: #FFFFFF;
        """)
    
    def show_menu_pane(self, pane_widget: QWidget):
        """
        显示菜单项对应的面板到右侧内容区域
        """
        # 清空右侧内容区域, 将box中的控件移除但不删除
        for i in reversed(range(self._right_vbox.count())): 
            widget = self._right_vbox.itemAt(i).widget()
            if widget:
                self._right_vbox.removeWidget(widget)
                widget.hide()
        # 添加新面板
        self._right_vbox.addWidget(pane_widget)
        pane_widget.show()
        
    def set_view_model(self, vm: MainWindowViewModel):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
        self.create_vm_sig_connect()

    def create_vm_sig_connect(self):
        """
        创建视图模型信号连接
        """
        self.view_model.sig_move_main_window.connect(self.on_sig_move_main_window)
        self.view_model.sig_min_main_window.connect(self.on_sig_min_main_window)
        self.view_model.sig_max_main_window.connect(self.on_sig_max_main_window)
        self.view_model.sig_diagnostics_main_window.connect(self.on_sig_diagnostics_main_window)
        self.view_model.sig_toggle_main_window_theme.connect(self.on_sig_toggle_main_window_theme)
        self.view_model.sig_register_menu_pane.connect(self.on_sig_register_menu_pane)
        self.view_model.sig_init_main_window.connect(self.on_sig_init_main_window)
    
    @Slot()
    def on_sig_init_main_window(self):
        """
        初始化主窗口槽函数
        """
        logger.info("on_sig_init_main_window")
        self.menu_widget_list[0].set_select(True)

    @Slot(object, str)
    def on_sig_register_menu_pane(self, menu_pane: QWidget, pane_view_id: str):
        """
        注册主窗口菜单面板槽函数    
        """
        logger.info("on_sig_register_menu_pane")
        if not self.menu_list:
            if hasattr(menu_pane, "get_menu_name"):
                menu_name = menu_pane.get_menu_name()
                menu_item_widget = MenuItemWidget(menu_name, pane_view_id, self.view_model._win_id)
                self._left_vbox.addWidget(menu_item_widget)
                self.menu_widget_list.append(menu_item_widget)
    
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