from core import Plugin
from .constructors import DashboardViewModelBuilder, DashboardCmdHandler

class DashboardPlugin(Plugin, DashboardViewModelBuilder):

    def __init__(self):
        super().__init__()
        self.dashboard_cmd_handler = DashboardCmdHandler()
    
    def initialize(self):
        self.dashboard_cmd_handler.assemble_cmd(self.create_dashboard_vm_instance)  
        
    def assembled(self, context):
        self.dashboard_cmd_handler.assemble_cmd(self.create_dashboard_vm_instance(context))
        