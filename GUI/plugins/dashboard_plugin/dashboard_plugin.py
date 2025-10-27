from core import Plugin, Global
from .constructors import DashboardViewModelBuilder, DashboardCmdHandler
from .views import DashboardView

def instance():
    return DashboardPlugin()

class DashboardPlugin(Plugin, DashboardViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.dashboard_cmd_handler = DashboardCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view(str(hash(DashboardView)), DashboardView)
        
    def assembled(self, context):
        self.dashboard_cmd_handler.assemble_cmd(self.create_dashboard_vm_instance(context))
        