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
            测试方法
            """
            logger.info("activate_main_window")
            # 主窗口容器
            main_win_id = Global().views_manager.instance_view(str(hash(MainWindowView)), vm_creator())
            # top 组件
            top_win_id = Global().views_manager.instance_view("TopBarView", vm_creator())
            Global().views_manager.fill_widget_with_execution(main_win_id, top_win_id, "set_top_widget")
            # 诊断组件
            diagnostic_win_id = Global().views_manager.instance_view("DiagnosticsView", vm_creator())
            Global().views_manager.fill_widget_with_execution(main_win_id, diagnostic_win_id, "set_diagnostic_widget")
            # # status bar组件
            status_bar_win_id = Global().views_manager.instance_view("StatusBarView", vm_creator())
            Global().views_manager.fill_widget_with_execution(main_win_id, status_bar_win_id, "set_status_bar_widget")
            Global().views_manager.show(main_win_id)
