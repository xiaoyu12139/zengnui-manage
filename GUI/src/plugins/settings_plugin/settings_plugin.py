######import_start######
from core import Plugin, Global
######constructor_start######
from .constructors.settings_vm_build import SettingsViewModelBuilder
from .constructors.settings.settings_cmd_handler import SettingsCmdHandler
from .constructors.sub_generate_setting.sub_generate_setting_cmd_handler import SubGenerateSettingCmdHandler
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from .views.settings_view import SettingsView
from .views.sub_generate_setting_view import SubGenerateSettingView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

def instance():
    return SettingsPlugin()

class SettingsPlugin(Plugin, SettingsViewModelBuilder):

    def __init__(self):
        super().__init__()
        ######plugin_init_start######
        self.settings_cmd_handler = SettingsCmdHandler()
        self.sub_generate_setting_cmd_handler = SubGenerateSettingCmdHandler()
        ######plugin_init_end######
    
    def initialize(self):
        ######plugin_initialize_start######
        Global().views_manager.register_view(str(hash(SettingsView)), SettingsView)
        Global().views_manager.register_view(str(hash(SubGenerateSettingView)), SubGenerateSettingView)
        ######plugin_initialize_end######
        
    def assembled(self, context):
        ######plugin_assembled_start######
        self.settings_cmd_handler.assemble_cmd(self.create_settings_vm_instance(context))
        self.sub_generate_setting_cmd_handler.assemble_cmd(self.create_sub_generate_setting_vm_instance(context))
        ######plugin_assembled_end######
        