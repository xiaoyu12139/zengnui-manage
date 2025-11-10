from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton, QLabel, QButtonGroup
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from core import Global
from ...ui_widget.settings_plugin import Ui_SettingsWidget
from ..build.rc_qss import *
from utils import set_style_sheet

class SettingsView(QWidget):
    """
    设置视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
        set_style_sheet(self, ":/qss/settings_plugin/settings_widget.qss")
    
    def setup_widget(self):
        """
        设置用户界面
        """
        self.ui = Ui_SettingsWidget()
        self.ui.setupUi(self)
        self._build_segment_tabs()
        
    
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm
        
    def get_menu_name(self) -> str:
        return "Settings"

    def _build_segment_tabs(self):
        """构建顶部分段 Tab，用于切换 contentStackedWidget"""
        # 容器：在 ui.tabWidget 内部添加水平布局与承载控件
        layout = QHBoxLayout(self.ui.tabWidget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)
        self.segmentBar = QWidget(self.ui.tabWidget)
        self.segmentBar.setObjectName("tabSegment")
        barLayout = QHBoxLayout(self.segmentBar)
        barLayout.setContentsMargins(5, 5, 5, 5)
        barLayout.setSpacing(6)
        layout.addWidget(self.segmentBar)
        layout.addStretch()

        # 定义分段按钮与对应页索引
        segments = [
            {"text": "通用设置", "icon": ":/img/top_bar_plugin/bell.svg"},
            {"text": "通知", "icon": ":/img/top_bar_plugin/bell.svg"},
            {"text": "安全", "icon": ":/img/top_bar_plugin/bell.svg"},
            {"text": "外观", "icon": ":/img/top_bar_plugin/theme.svg"},
        ]

        self._seg_buttons = []
        # 确保至少有与按钮数量匹配的页面；如果不足则创建占位页
        while self.ui.contentStackedWidget.count() < len(segments):
            page = QWidget()
            # 简单占位内容
            ph = QLabel(page)
            ph.setText(f"页面占位 {self.ui.contentStackedWidget.count()}")
            ph.setAlignment(Qt.AlignCenter)
            pageLayout = QHBoxLayout(page)
            pageLayout.addWidget(ph)
            self.ui.contentStackedWidget.addWidget(page)

        # 创建互斥的按钮组，保证仅一个处于选中态
        self._seg_group = QButtonGroup(self.segmentBar)
        self._seg_group.setExclusive(True)

        for idx, seg in enumerate(segments):
            btn = QPushButton(seg["text"], self.segmentBar)
            btn.setCheckable(True)
            btn.setProperty("seg", True)
            btn.setObjectName(f"seg_{idx}")
            if seg["icon"]:
                try:
                    btn.setIcon(QIcon(seg["icon"]))
                except Exception:
                    pass
            # 加入互斥分组并设置标识为索引
            self._seg_group.addButton(btn, idx)
            barLayout.addWidget(btn)
            self._seg_buttons.append(btn)

        # 统一处理点击：切换页面，分组将自动取消其他选中从而恢复默认样式
        try:
            # 优先使用 idClicked(int)
            self._seg_group.idClicked.connect(self._on_segment_clicked)
        except Exception:
            # 兼容不支持 idClicked 的环境
            self._seg_group.buttonClicked.connect(self._on_segment_button_clicked)

        # 默认选中第一个
        if self._seg_group.button(0):
            self._seg_group.button(0).setChecked(True)

    def _on_segment_clicked(self, idx: int):
        try:
            self.ui.contentStackedWidget.setCurrentIndex(idx)
        except Exception:
            pass

    def _on_segment_button_clicked(self, btn: QPushButton):
        try:
            idx = self._seg_group.id(btn)
            if idx == -1:
                idx = self._seg_buttons.index(btn)
            self.ui.contentStackedWidget.setCurrentIndex(idx)
        except Exception:
            pass
