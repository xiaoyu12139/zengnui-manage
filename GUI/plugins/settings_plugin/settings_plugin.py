from core import Plugin
from .constructors import SettingsViewModelBuilder, SettingsCmdHandler

class SettingsPlugin(Plugin, SettingsViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.settings_cmd_handler = SettingsCmdHandler()
    
    def initialize(self):
        self.settings_cmd_handler.assemble_cmd(self.create_settings_vm_instance)  
        
    def assembled(self, context):
        self.settings_cmd_handler.assemble_cmd(self.create_settings_vm_instance(context))
        