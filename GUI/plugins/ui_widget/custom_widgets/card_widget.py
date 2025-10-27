from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

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