from core import cmd, Global
from utils import logger
from ...views import MainWindowView

class MainWindowCommandHandler:
    """
    主窗口命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装主窗口命令
        """
        @cmd("ed23f387-7767-41bd-a8dc-29bc9025e2b0", "activate_main_window")
        def activate_main_window():
            """
            激活主窗口
            """
            logger.info("activate_main_window")
            # 主窗口容器
            main_win_id = Global().views_manager.instance_view(str(hash(MainWindowView)), vm_creator())
            # top 组件
            Global().command_manager.cmd("d56194f5-4ab5-44d6-a65c-7d3161b7764a", main_win_id)
            # 诊断组件
            Global().command_manager.cmd("8ba404a6-6cb6-4804-a719-c82163773eb2", main_win_id)
            # # status bar组件
            Global().command_manager.cmd("cdec7d58-7551-411f-847b-6285e8eb52c2", main_win_id)
            Global().views_manager.show(main_win_id)
        
        @cmd("ef8555d2-17c1-4b60-9ddb-98d255788ed4", "close_main_window")
        def close_main_window():
            """
            关闭主窗口
            """
            logger.info("close_main_window")
            vm_creator().close_main_window()
