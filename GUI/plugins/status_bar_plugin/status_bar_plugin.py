from core import Plugin, Global
from .constructors import StatusBarVMBuilder, StatusBarCmdHandler
from .views import StatusBarView

def instance():
    return StatusBarPlugin()

class StatusBarPlugin(Plugin, StatusBarVMBuilder):

    def __init__(self):
        super().__init__()
        self.status_bar_cmd_handler = StatusBarCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view("StatusBarView", StatusBarView)
    
    def assembled(self, context):
        self.status_bar_cmd_handler.assemble_cmd(self.create_status_bar_vm_instance(context))
        