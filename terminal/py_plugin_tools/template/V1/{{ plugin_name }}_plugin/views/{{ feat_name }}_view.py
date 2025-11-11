######import_start######
#constructor_start
#constructor_end
#ui_start
from ...ui_widget.{{ feat_name }}_plugin import Ui_{{ FeatName }}
#ui_end
#view_start
#view_end
#viewmodel_start
#viewmodel_end
######import_end######
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

class {{ FeatName }}View(QWidget):
    """
    {{ FeatName }}视图类
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 允许 QWidget 绘制样式表背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setup_widget()
    
    def setup_widget(self):
        """
        设置用户界面
        """
        self.ui = Ui_{{ FeatName }}()
        self.ui.setupUi(self)
        
    def set_view_model(self, vm):
        """
        注入视图模型，供 ViewsManager 调用
        """
        self.view_model = vm

    ######plugin_main_feat_start######
    def get_menu_name(self) -> str:
        return "{{ FeatName }}"
    ######plugin_main_feat_end######
