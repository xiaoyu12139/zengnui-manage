from core import Plugin
from .constructors import DiagnosticsVMBuilder, DiagnosticsCmdHandler

class DiagnosticsPlugin(Plugin, DiagnosticsVMBuilder):

    def __init__(self):
        super().__init__()
        self.diagnostics_cmd_handler = DiagnosticsCmdHandler()
    
    def initialize(self):
        self.diagnostics_cmd_handler.assemble_cmd(self.create_diagnostics_vm_instance)  
        
    def assembled(self, context):
        self.diagnostics_cmd_handler.assemble_cmd(self.create_diagnostics_vm_instance(context))
        