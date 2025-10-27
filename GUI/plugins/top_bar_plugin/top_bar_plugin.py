from core import Plugin, Global
from .constructors import TopBarVMBuilder, TopBarCmdHandler
from .views import TopBarView

def instance():
    return TopBarPlugin()

class TopBarPlugin(Plugin, TopBarVMBuilder):

    def __init__(self):
        super().__init__()
        self.top_cmd_handler = TopBarCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view("TopBarView", TopBarView)
    
    def assembled(self, context):
        self.top_cmd_handler.assemble_cmd(self.create_top_bar_vm_instance(context))
        