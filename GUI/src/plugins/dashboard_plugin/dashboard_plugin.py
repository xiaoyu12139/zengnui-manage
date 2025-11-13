######import_start######
from core import Plugin, Global
######constructor_start######
from .constructors.dashboard_vm_build import DashboardViewModelBuilder
from .constructors.dashboard.dashboard_cmd_handler import DashboardCmdHandler
from .constructors.card_config.card_config_cmd_handler import CardConfigCmdHandler
from .constructors.card_quick_option.card_quick_option_cmd_handler import CardQuickOptionCmdHandler
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from .views.dashboard_view import DashboardView
from .views.card_config_view import CardConfigView
from .views.card_quick_option_view import CardQuickOptionView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

def instance():
    return DashboardPlugin()

class DashboardPlugin(Plugin, DashboardViewModelBuilder):

    def __init__(self):
        super().__init__()
        ######plugin_init_start######
        self.dashboard_cmd_handler = DashboardCmdHandler()
        self.card_config_cmd_handler = CardConfigCmdHandler()
        self.card_quick_option_cmd_handler = CardQuickOptionCmdHandler()
        ######plugin_init_end######
    
    def initialize(self):
        ######plugin_initialize_start######
        Global().views_manager.register_view(str(hash(DashboardView)), DashboardView)
        Global().views_manager.register_view(str(hash(CardConfigView)), CardConfigView)
        Global().views_manager.register_view(str(hash(CardQuickOptionView)), CardQuickOptionView)
        ######plugin_initialize_end######
        
    def assembled(self, context):
        ######plugin_assembled_start######
        self.dashboard_cmd_handler.assemble_cmd(self.create_dashboard_vm_instance(context))
        self.card_config_cmd_handler.assemble_cmd(self.create_card_config_vm_instance(context))
        self.card_quick_option_cmd_handler.assemble_cmd(self.create_card_quick_option_vm_instance(context))
        ######plugin_assembled_end######
        