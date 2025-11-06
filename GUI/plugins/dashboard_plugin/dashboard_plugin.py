from core import Plugin, Global
from .constructors import DashboardViewModelBuilder, DashboardCmdHandler, CardConfigCmdHandler, CardQuickOptionCmdHandler
from .views import DashboardView, CardConfigView, CardQuickOptionView

def instance():
    return DashboardPlugin()

class DashboardPlugin(Plugin, DashboardViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.dashboard_cmd_handler = DashboardCmdHandler()
        self.card_config_cmd_handler = CardConfigCmdHandler()
        self.card_quick_option_cmd_handler = CardQuickOptionCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view(str(hash(DashboardView)), DashboardView)
        Global().views_manager.register_view(str(hash(CardConfigView)), CardConfigView)
        Global().views_manager.register_view(str(hash(CardQuickOptionView)), CardQuickOptionView)
        
    def assembled(self, context):
        self.dashboard_cmd_handler.assemble_cmd(self.create_dashboard_vm_instance(context))
        self.card_config_cmd_handler.assemble_cmd(self.create_card_config_vm_instance(context))
        self.card_quick_option_cmd_handler.assemble_cmd(self.create_card_quick_option_vm_instance(context))
        