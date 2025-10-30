from core import cmd, Global
from utils import logger
from ...views import DiagnosticsView

class DiagnosticsCmdHandler:
    """
    诊断命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装诊断命令
        """
        @cmd("8ba404a6-6cb6-4804-a719-c82163773eb2", "")
        def activate_diagnostics(parent_widget_id):
            """
            激活诊断组件
            """
            diagnostic_win_id = Global().views_manager.instance_view("DiagnosticsView", vm_creator())
            Global().views_manager.fill_widget_with_execution(parent_widget_id, diagnostic_win_id, "set_diagnostic_widget")
