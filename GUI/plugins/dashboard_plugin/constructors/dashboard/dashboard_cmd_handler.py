from core import cmd, Global
from utils import logger
from ...views import DashboardView

class DashboardCmdHandler:
    """
    仪表盘命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装仪表盘命令
        """
        def activate_dashboard():
            """
            测试方法
            """
            ...