from PySide6.QtWidgets import QFrame, QHBoxLayout


def row(left: QWidget, right_ops: QWidget) -> QFrame:
    r = QFrame()
    r.setObjectName("row")
    layout = QHBoxLayout(r)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)
    layout.addWidget(left, 1)
    layout.addWidget(right_ops, 0)
    return r