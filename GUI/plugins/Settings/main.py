from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QGroupBox
)


def row(left: QWidget, right_ops: QWidget) -> QFrame:
    r = QFrame()
    r.setObjectName("row")
    l = QHBoxLayout(r)
    l.setContentsMargins(10, 10, 10, 10)
    l.setSpacing(10)
    l.addWidget(left, 1)
    l.addWidget(right_ops, 0)
    return r


class Plugin:
    zone = "page"
    nav_name = "Settings"

    def build(self, main_window) -> QWidget:
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(12)

        g = QGroupBox("常规")
        g_v = QVBoxLayout(g)
        g_v.setContentsMargins(14, 12, 14, 12)
        g_v.setSpacing(8)
        g_v.addWidget(QLabel("启动行为: 默认"))

        t = QGroupBox("终端")
        t_v = QVBoxLayout(t)
        t_v.setContentsMargins(14, 12, 14, 12)
        t_v.setSpacing(8)
        t_v.addWidget(QLabel("默认终端: Windows Terminal"))

        v.addWidget(g)
        v.addWidget(t)
        v.addStretch(1)
        return page