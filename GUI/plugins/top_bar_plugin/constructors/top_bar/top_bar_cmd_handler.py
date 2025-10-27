from core import cmd, Global
from utils import logger
from ..views.top_bar_view import TopBarView

class TopBarCmdHandler:
    """
    顶部栏命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装顶部栏命令
        """
        def activate_top_bar():
            """
            测试方法
            """
            ...