from .views import SubGenerateSettingWidgetView
from .constructors import SubGenerateSettingWidgetCmdHandler
from core import Plugin, Global
from .constructors import SettingsViewModelBuilder, SettingsCmdHandler
from .views import SettingsView

def instance():
    return SettingsPlugin()

class SettingsPlugin(Plugin, SettingsViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.sub_generate_setting_widget_cmd_handle = SubGenerateSettingWidgetCmdHandler()
        self.settings_cmd_handler = SettingsCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view(str(hash(SettingsView)), SettingsView)
        Global().views_manager.register_view(str(hash(SubGenerateSettingWidgetView)), SubGenerateSettingWidgetView)
        
    def assembled(self, context):
        self.settings_cmd_handler.assemble_cmd(self.create_settings_vm_instance(context))
        self.sub_generate_setting_widget_cmd_handle.assemble_cmd(self.create_sub_generate_setting_widget_vm_instance(context))
        