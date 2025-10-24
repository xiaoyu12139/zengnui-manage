from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton, QGridLayout
)


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


class Plugin:
    zone = "page"
    nav_name = "Dashboard"

    def build(self, main_window) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        # 简版系统状态
        c1 = card("系统状态")
        c1.layout().addWidget(QLabel("AutoRun: 已启用"))

        # 简版快速操作
        c2 = card("快速操作")
        ops = QWidget()
        ops_l = QHBoxLayout(ops)
        ops_l.setContentsMargins(0, 0, 0, 0)
        ops_l.setSpacing(8)
        ops_l.addWidget(QPushButton("update-change-dir"))
        ops_l.addWidget(QPushButton("加载宏"))
        c2.layout().addWidget(ops)

        # 简版别名概览
        c3 = card("别名概览")
        c3.layout().addWidget(QLabel("xiaoyu → C:/Users/xiaoyu"))
        c3.layout().addWidget(QLabel("yxtools → D:/yxtools"))

        grid.addWidget(c1, 0, 0)
        grid.addWidget(c2, 0, 1)
        grid.addWidget(c3, 1, 0, 1, 2)

        layout.addLayout(grid)
        layout.addStretch(1)
        return page