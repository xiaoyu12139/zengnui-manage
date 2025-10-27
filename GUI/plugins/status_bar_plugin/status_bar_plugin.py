from core import Plugin
from .constructors import StatusBarVMBuilder, StatusBarCmdHandler

class StatusBarPlugin(Plugin, StatusBarVMBuilder):

    def __init__(self):
        super().__init__()
        self.status_bar_cmd_handler = StatusBarCmdHandler()
    
    def initialize(self):
        self.status_bar_cmd_handler.assemble_cmd(self.create_status_bar_vm_instance)
    
    def assembled(self, context):
        self.status_bar_cmd_handler.assemble_cmd(self.create_status_bar_vm_instance(context))
        