import sys
import importlib.util
import traceback
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget,
    QDockWidget, QTextEdit, QStatusBar, QFrame, QToolButton
)
from pathlib import Path
from PySide6.QtWidgets import QSplitter, QSizePolicy, QScrollArea


def make_dark_palette(app: QApplication):
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(18, 20, 23))
    pal.setColor(QPalette.WindowText, QColor(234, 238, 243))
    pal.setColor(QPalette.Base, QColor(15, 18, 22))
    pal.setColor(QPalette.AlternateBase, QColor(27, 31, 38))
    pal.setColor(QPalette.ToolTipBase, QColor(27, 31, 38))
    pal.setColor(QPalette.ToolTipText, QColor(234, 238, 243))
    pal.setColor(QPalette.Text, QColor(234, 238, 243))
    pal.setColor(QPalette.Button, QColor(23, 26, 31))
    pal.setColor(QPalette.ButtonText, QColor(234, 238, 243))
    pal.setColor(QPalette.BrightText, QColor(255, 107, 107))
    pal.setColor(QPalette.Highlight, QColor(91, 124, 250))
    pal.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(pal)


def card(title: str) -> QFrame:
    f = QFrame()
    f.setObjectName("card")
    v = QVBoxLayout(f)
    v.setContentsMargins(14, 12, 14, 12)
    v.setSpacing(8)
    h = QLabel(title)
    h.setObjectName("cardTitle")
    v.addWidget(h)
    return f


def row(left: QWidget, right_ops: QWidget) -> QFrame:
    r = QFrame()
    r.setObjectName("row")
    layout = QHBoxLayout(r)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)
    layout.addWidget(left, 1)
    layout.addWidget(right_ops, 0)
    return r


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZengNUI Manage")
        self.resize(1200, 800)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        self.plugins_root = Path(__file__).parent / "plugins"
        # 扫描插件（类约定）
        self._plugins = self._scan_plugins()
        # 页面插件映射（nav_name → 插件实例）
        self._page_plugins = {}

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 顶部栏由插件提供（zone='top'）
        top_w = self._build_top_plugin()
        if top_w is not None:
            root_layout.addWidget(top_w)
        else:
            # Fallback: 简易顶栏
            top = QWidget()
            top.setObjectName("top")
            tl = QHBoxLayout(top)
            tl.setContentsMargins(18, 12, 18, 12)
            tl.setSpacing(12)
            brand = QLabel("ZengNUI Manage")
            brand.setObjectName("brand")
            tl.addWidget(brand)
            root_layout.addWidget(top)

        # 主体区域容器
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # 左侧导航
        nav = QListWidget()
        nav.setObjectName("nav")
        nav.setMinimumWidth(200)
        nav.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 主工作区（Stacked）
        pages = QStackedWidget()
        # 使页面容器随窗口自适应扩展
        pages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 保存引用以便在插件/顶栏中进行跳转
        self._nav = nav
        self._pages = pages

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(nav)
        splitter.addWidget(pages)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([240, 960])

        body_layout.addWidget(splitter, 1)
        root_layout.addWidget(body, 1)

        # 状态栏
        status = QStatusBar()
        status.showMessage("准备就绪 · 类插件加载")
        self.setStatusBar(status)

        self.setCentralWidget(root)
        # 启用边缘命中与拖动缩放
        self.setMouseTracking(True)
        root.setMouseTracking(True)
        root.installEventFilter(self)
        self._resize_margin = 6
        self._apply_style()

        # 挂载页面插件（zone='page' 且配置了 nav_name）
        self._populate_page_plugins(nav, pages)
        nav.currentRowChanged.connect(pages.setCurrentIndex)
        # 构建右侧 Dock 插件（如：消息与诊断）
        self._build_dock_plugins()
        # 安装全局缩放事件过滤器到所有部件
        self._wire_resize_filters()

    def _scan_plugins(self):
        items = []
        if not self.plugins_root.exists():
            return items
        for p in sorted(self.plugins_root.iterdir()):
            if not p.is_dir():
                continue
            main_py = p / "main.py"
            if not main_py.exists():
                continue
            try:
                spec = importlib.util.spec_from_file_location(f"plugin_{p.name}", str(main_py))
                if spec is None or spec.loader is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # 约定：寻找带有 zone 属性且包含 build(self, main) 的类
                cls_candidates = []
                for cname, obj in module.__dict__.items():
                    try:
                        if isinstance(obj, type) and hasattr(obj, "zone") and callable(getattr(obj, "build", None)):
                            cls_candidates.append(obj)
                    except Exception:
                        pass
                if not cls_candidates:
                    continue
                # 使用首个候选类
                cls = cls_candidates[0]
                inst = cls()
                # 记录 zone/nav_name
                zone = getattr(inst, "zone", None)
                nav_name = getattr(inst, "nav_name", None)
                items.append({"dir": p.name, "inst": inst, "zone": zone, "nav_name": nav_name})
            except Exception:
                traceback.print_exc()
                continue
        return items

    def _build_top_plugin(self) -> QWidget | None:
        for item in self._plugins:
            if item.get("zone") == "top":
                try:
                    w = item["inst"].build(self)
                    # 允许插件触发拖拽注册；也可在插件内部调用 set_drag_widget
                    return w if isinstance(w, QWidget) else None
                except Exception:
                    traceback.print_exc()
        return None

    def _populate_page_plugins(self, nav: QListWidget, pages: QStackedWidget):
        plugins_loaded = []
        for item in self._plugins:
            if item.get("zone") != "page":
                continue
            nav_name = item.get("nav_name")
            if not nav_name:
                # 未配置目录名则不显示
                continue
            try:
                w = item["inst"].build(self)
                if not isinstance(w, QWidget):
                    continue
                page = QWidget()
                # 页面自适应扩展
                page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                v = QVBoxLayout(page)
                v.setContentsMargins(18, 18, 18, 18)
                v.setSpacing(12)
                title = QLabel(nav_name)
                title.setObjectName("pageTitle")
                v.addWidget(title)
                sa = QScrollArea()
                sa.setWidget(w)
                sa.setWidgetResizable(True)
                sa.setFrameShape(QFrame.NoFrame)
                sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                # 让滚动区域占满剩余空间
                sa.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                v.addWidget(sa, 1)
                
                if nav_name == "消息与诊断":
                    # 特殊处理：将消息与诊断固定到最左边（导航第一个）
                    pages.insertWidget(0, page)
                    nav.insertItem(0, QListWidgetItem(nav_name))
                else:
                    pages.addWidget(page)
                    nav.addItem(QListWidgetItem(nav_name))
                    plugins_loaded.append(nav_name)
                    # 记录页面插件实例，便于特殊处理（如 Diagnostics）
                    self._page_plugins[nav_name] = item["inst"]
            except Exception:
                traceback.print_exc()
        if not plugins_loaded:
            pages.addWidget(self._placeholder_widget("未发现页面插件。请在 GUI/plugins 下创建包含 zone='page' 的类 Plugin"))
            nav.addItem(QListWidgetItem("占位页"))
        nav.setCurrentRow(0)

    def _create_plugin_widget(self, plugin_name: str, main_path: Path) -> QWidget:
        return self._placeholder_widget("已弃用：请使用类插件约定（zone/build/nav_name）")

    def _placeholder_widget(self, msg: str) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(18, 18, 18, 18)
        v.setSpacing(10)
        t = QLabel("插件页面")
        t.setObjectName("pageTitle")
        v.addWidget(t)
        info = QLabel(msg)
        info.setObjectName("meta")
        v.addWidget(info)
        return w

    def _icon(self, name: str) -> QIcon:
        p = Path(__file__).parent / "resource" / "img" / name
        return QIcon(str(p))

    def _toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
            if hasattr(self, "_btn_max"):
                self._btn_max.setIcon(self._icon("maximize.svg"))
        else:
            self.showMaximized()
            if hasattr(self, "_btn_max"):
                self._btn_max.setIcon(self._icon("restore.svg"))

    def eventFilter(self, obj, event):
        if obj is getattr(self, "_top_widget", None):
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self._drag_pos = event.globalPosition().toPoint()
                self._dragging = True
                return True
            elif event.type() == QEvent.MouseMove and getattr(self, "_dragging", False):
                delta = event.globalPosition().toPoint() - self._drag_pos
                self.move(self.pos() + delta)
                self._drag_pos = event.globalPosition().toPoint()
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                self._dragging = False
                return True
            elif event.type() == QEvent.MouseButtonDblClick:
                # 顶栏双击最大化/还原
                self._toggle_max_restore()
                return True
        else:
            # 中央区域边缘命中与拖动缩放
            if event.type() == QEvent.MouseMove:
                if getattr(self, "_resizing", False):
                    self._perform_resize(event.globalPosition().toPoint())
                    return True
                pos = event.position().toPoint()
                try:
                    pos = obj.mapTo(self, pos)
                except Exception:
                    pass
                dirn = self._hit_test_resize(pos)
                self._update_cursor_for_dir(dirn)
                return False
            elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                pos = event.position().toPoint()
                try:
                    pos = obj.mapTo(self, pos)
                except Exception:
                    pass
                dirn = self._hit_test_resize(pos)
                if dirn:
                    self._resizing = True
                    self._resize_dir = dirn
                    self._resize_start_geo = self.geometry()
                    self._resize_start_pos = event.globalPosition().toPoint()
                    return True
            elif event.type() == QEvent.MouseButtonRelease:
                if getattr(self, "_resizing", False):
                    self._resizing = False
                    return True
        return super().eventFilter(obj, event)

    def _update_cursor_for_dir(self, dirn: str | None):
        # 根据命中方向更新光标样式
        if not dirn:
            self.unsetCursor()
            return
        if dirn in ("left", "right"):
            self.setCursor(Qt.SizeHorCursor)
        elif dirn in ("top", "bottom"):
            self.setCursor(Qt.SizeVerCursor)
        elif dirn in ("top_left", "bottom_right"):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.SizeBDiagCursor)

    def _hit_test_resize(self, pos) -> str | None:
        # 计算鼠标相对窗口的位置，判断是否命中边缘/角落
        m = getattr(self, "_resize_margin", 6)
        r = self.rect()
        x, y = pos.x(), pos.y()
        left = x <= m
        right = x >= r.width() - m
        top = y <= m
        bottom = y >= r.height() - m
        if top and left:
            return "top_left"
        if top and right:
            return "top_right"
        if bottom and left:
            return "bottom_left"
        if bottom and right:
            return "bottom_right"
        if left:
            return "left"
        if right:
            return "right"
        if top:
            return "top"
        if bottom:
            return "bottom"
        return None

    def _perform_resize(self, global_pos):
        # 根据拖动方向与位移调整窗口几何
        start_geo = getattr(self, "_resize_start_geo", self.geometry())
        start_pos = getattr(self, "_resize_start_pos", self.pos())
        dirn = getattr(self, "_resize_dir", None)
        if not dirn:
            return
        dx = global_pos.x() - start_pos.x()
        dy = global_pos.y() - start_pos.y()
        # 最小尺寸约束
        min_w = max(self.minimumWidth(), 200)
        min_h = max(self.minimumHeight(), 150)
        g = start_geo
        x, y, w, h = g.x(), g.y(), g.width(), g.height()
        if dirn in ("right", "top_right", "bottom_right"):
            w = max(min_w, w + dx)
        if dirn in ("bottom", "bottom_left", "bottom_right"):
            h = max(min_h, h + dy)
        if dirn in ("left", "top_left", "bottom_left"):
            new_w = max(min_w, w - dx)
            new_x = x + (w - new_w)
            w, x = new_w, new_x
        if dirn in ("top", "top_left", "top_right"):
            new_h = max(min_h, h - dy)
            new_y = y + (h - new_h)
            h, y = new_h, new_y
        self.setGeometry(x, y, w, h)

    def set_drag_widget(self, w: QWidget):
        # 注册顶栏为拖动区域，并安装事件过滤器
        try:
            if hasattr(self, "_top_widget") and self._top_widget is not None:
                self._top_widget.removeEventFilter(self)
        except Exception:
            pass
        self._top_widget = w
        w.installEventFilter(self)

    def _wire_resize_filters(self):
        # 递归安装事件过滤器到所有子部件，确保任意区域靠近边缘都可缩放
        try:
            targets = [self.centralWidget(), self.statusBar()]
            for t in targets:
                if t is None:
                    continue
                t.setMouseTracking(True)
                t.installEventFilter(self)
                for child in t.findChildren(QWidget):
                    child.setMouseTracking(True)
                    child.installEventFilter(self)
            # 处理所有 DockWidget 及其子部件
            for dock in self.findChildren(QDockWidget):
                dock.setMouseTracking(True)
                dock.installEventFilter(self)
                for child in dock.findChildren(QWidget):
                    child.setMouseTracking(True)
                    child.installEventFilter(self)
        except Exception:
            traceback.print_exc()

    def open_nav(self, name: str) -> bool:
        # 根据目录名切换页面，供顶栏通知按钮等调用
        if not hasattr(self, "_nav"):
            return False
        for i in range(self._nav.count()):
            item = self._nav.item(i)
            if item and item.text() == name:
                self._nav.setCurrentRow(i)
                return True
        return False

    def register_diagnostics_sink(self, plugin_inst) -> None:
        # 注册诊断日志的插件实例，供统一追加日志
        self._diagnostics = plugin_inst

    def append_diagnostic(self, level: str, message: str) -> None:
        # 追加诊断日志到插件（若已注册）
        try:
            if hasattr(self, "_diagnostics") and hasattr(self._diagnostics, "append_log"):
                self._diagnostics.append_log(level, message)
        except Exception:
            traceback.print_exc()

    def changeEvent(self, event):
        # 根据窗口状态更新最大化/还原按钮图标
        super().changeEvent(event)
        if event.type() == QEvent.WindowStateChange and hasattr(self, "_btn_max"):
            self._btn_max.setIcon(self._icon("restore.svg" if self.isMaximized() else "maximize.svg"))

    def _build_dock_plugins(self):
        # 构建并挂载右侧 Dock 插件（zone='dock'）
        for item in self._plugins:
            if item.get("zone") != "dock":
                continue
            try:
                inst = item["inst"]
                w = inst.build(self)
                if not isinstance(w, QWidget):
                    continue
                title = getattr(inst, "dock_title", getattr(inst, "nav_name", "Dock"))
                dock = QDockWidget(title, self)
                dock.setObjectName(f"dock_{item['dir']}")
                dock.setWidget(w)
                dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
                self.addDockWidget(Qt.RightDockWidgetArea, dock)
                # 若为诊断 dock，保存引用以便显示或聚焦
                if title == "消息与诊断":
                    self._diagnostics_dock = dock
            except Exception:
                traceback.print_exc()

    def show_diagnostics(self):
        # 显示并聚焦右侧“消息与诊断”Dock
        try:
            if hasattr(self, "_diagnostics_dock") and self._diagnostics_dock is not None:
                self._diagnostics_dock.show()
                self._diagnostics_dock.raise_()
        except Exception:
            traceback.print_exc()
    def _ops(self, buttons: list[tuple[str]]):
        w = QWidget()
        l = QHBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(8)
        for (text,) in buttons:
            b = QPushButton(text)
            l.addWidget(b)
        return w

    def _apply_style(self):
        css_path = Path(__file__).parent / "resource" / "css" / "default.qss"
        try:
            self.setStyleSheet(css_path.read_text(encoding="utf-8"))
        except Exception:
            # Fallback：最小样式，防止缺失文件时界面无样式
            self.setStyleSheet("#nav { background: #171a1f; } #pageTitle { font-size: 18px; font-weight: 600; }")


def main():
    app = QApplication(sys.argv)
    make_dark_palette(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
