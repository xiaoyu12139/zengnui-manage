from core import Plugin, Global
from .constructors import DiagnosticsVMBuilder, DiagnosticsCmdHandler
from .views import DiagnosticsView

def instance():
    return DiagnosticsPlugin()

class DiagnosticsPlugin(Plugin, DiagnosticsVMBuilder):

    def __init__(self):
        super().__init__()
        self.diagnostics_cmd_handler = DiagnosticsCmdHandler()
    
    def initialize(self):
        Global().views_manager.register_view("DiagnosticsView", DiagnosticsView)

    def assembled(self, context):
        self.diagnostics_cmd_handler.assemble_cmd(self.create_diagnostics_vm_instance(context))
        