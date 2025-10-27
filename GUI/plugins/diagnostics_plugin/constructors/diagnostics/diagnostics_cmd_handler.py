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
        def activate_diagnostics():
            """
            测试方法
            """
            ...