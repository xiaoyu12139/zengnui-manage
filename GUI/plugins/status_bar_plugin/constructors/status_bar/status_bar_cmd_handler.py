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
        @cmd("cdec7d58-7551-411f-847b-6285e8eb52c2", "")
        def activate_status_bar(parent_widget_id):
            """
            激活状态栏
            """
            status_bar_win_id = Global().views_manager.instance_view("StatusBarView", vm_creator())
            Global().views_manager.fill_widget_with_execution(parent_widget_id, status_bar_win_id, "set_status_bar_widget")
