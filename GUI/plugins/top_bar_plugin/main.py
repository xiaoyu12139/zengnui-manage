from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QToolButton
)


class Plugin:
    zone = "top"
    # 未配置 nav_name，表示不进入左侧目录

    def build(self, main_window) -> QWidget:
        top = QWidget()
        top.setObjectName("top")
        layout = QHBoxLayout(top)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(12)

        brand = QLabel("ZengNUI Manage")
        brand.setObjectName("brand")

        # 搜索框
        search_box = QWidget()
        sb_layout = QHBoxLayout(search_box)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(6)
        search_input = QLineEdit()
        search_input.setPlaceholderText("搜索…")
        sb_layout.addWidget(search_input)

        # 右侧按钮组
        actions = QWidget()
        al = QHBoxLayout(actions)
        al.setContentsMargins(0, 0, 0, 0)
        al.setSpacing(6)

        btn_theme = QToolButton()
        btn_theme.setObjectName("customBtn")
        btn_theme.setIcon(main_window._icon("theme.svg"))
        btn_theme.setToolTip("切换主题")
        btn_theme.setAutoRaise(True)
        btn_theme.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn_notify = QToolButton()
        btn_notify.setObjectName("customBtn")
        btn_notify.setIcon(main_window._icon("bell.svg"))
        btn_notify.setToolTip("通知")
        btn_notify.setAutoRaise(True)
        btn_notify.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn_min = QToolButton()
        btn_min.setObjectName("winBtnMin")
        btn_min.setIcon(main_window._icon("minimize.svg"))
        btn_min.setToolTip("最小化")
        btn_min.setAutoRaise(True)
        btn_min.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn_max = QToolButton()
        btn_max.setObjectName("winBtnMax")
        btn_max.setIcon(main_window._icon("maximize.svg"))
        btn_max.setToolTip("最大化/还原")
        btn_max.setAutoRaise(True)
        btn_max.setToolButtonStyle(Qt.ToolButtonIconOnly)

        btn_close = QToolButton()
        btn_close.setObjectName("winBtnClose")
        btn_close.setIcon(main_window._icon("close.svg"))
        btn_close.setToolTip("关闭")
        btn_close.setAutoRaise(True)
        btn_close.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # 事件连接
        btn_theme.clicked.connect(lambda: None)  # 可在此实现主题切换
        btn_notify.clicked.connect(main_window.show_diagnostics)
        btn_min.clicked.connect(main_window.showMinimized)
        btn_max.clicked.connect(main_window._toggle_max_restore)
        btn_close.clicked.connect(main_window.close)

        al.addWidget(btn_theme)
        al.addWidget(btn_notify)
        al.addSpacing(8)
        al.addWidget(btn_min)
        al.addWidget(btn_max)
        al.addWidget(btn_close)

        # 保存引用以便更新最大化/还原图标
        main_window._btn_max = btn_max

        layout.addWidget(brand)
        layout.addWidget(search_box, 1)
        layout.addWidget(actions)

        # 顶部栏作为窗口拖动区域
        main_window.set_drag_widget(top)
        return top