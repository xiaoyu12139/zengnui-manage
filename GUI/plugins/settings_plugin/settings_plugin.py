from .views import Sub_Generate_Setting_WidgetView
from .constructors import Sub_Generate_Setting_WidgetCmdHandler
from core import Plugin, Global
from .constructors import SettingsViewModelBuilder, SettingsCmdHandler
from .views import SettingsView

def instance():
    return SettingsPlugin()

class SettingsPlugin(Plugin, SettingsViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.settings_cmd_handler = SettingsCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view(str(hash(SettingsView)), SettingsView)
        
    def assembled(self, context):
        self.settings_cmd_handler.assemble_cmd(self.create_settings_vm_instance(context))
        