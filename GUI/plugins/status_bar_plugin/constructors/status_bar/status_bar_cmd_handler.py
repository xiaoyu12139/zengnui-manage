from core import cmd, Global
from utils import logger
from ...views import StatusBarView

class StatusBarCmdHandler:
    """
    状态栏命令处理类
    """
    
    def assemble_cmd(self, vm_creator: callable):
        """
        组装状态栏命令
        """
        def activate_status_bar():
            """
            测试方法
            """
            ...