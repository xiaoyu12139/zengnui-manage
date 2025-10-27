from core import Plugin
from .constructors import TopBarVMBuilder, TopBarCmdHandler

class TopBarPlugin(Plugin, TopBarVMBuilder):

    def __init__(self):
        super().__init__()
        self.top_cmd_handler = TopBarCmdHandler()
    
    def initialize(self):
        self.top_cmd_handler.assemble_cmd(self.create_top_bar_vm_instance)
    
    def assembled(self, context):
        self.top_cmd_handler.assemble_cmd(self.create_top_bar_vm_instance(context))
        