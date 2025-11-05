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
            # 激活菜单栏相关插件
            Global().command_manager.execute_command("activate_dashboard")
            Global().command_manager.execute_command("activate_settings")
            # 显示主窗口
            vm_creator().init_main_window()
            Global().views_manager.show(main_win_id)
        
        @cmd("ef8555d2-17c1-4b60-9ddb-98d255788ed4", "close_main_window")
        def close_main_window():
            """
            关闭主窗口
            """
            logger.info("close_main_window")
            vm_creator().close_main_window()
        
        @cmd("b5a0cd84-ea94-455c-9454-159b16c19047", "move_main_window")
        def move_main_window(pos):
            """
            移动主窗口
            """
            # logger.info(f"move_main_window: {pos}")
            vm_creator().move_main_window(pos)
        
        @cmd("baf41145-9615-467d-8c0c-45532548b6bd", "minimize_main_window")
        def minimize_main_window():
            """
            最小化主窗口
            """
            logger.info("minimize_main_window")
            vm_creator().minimize_main_window()

        @cmd("0ab1b41d-8ca3-473f-b407-7c0f3995eeab", "maximize_main_window")
        def maximize_main_window(maximize: bool):
            """
            最大化主窗口
            """
            logger.info("maximize_main_window")
            vm_creator().maximize_main_window(maximize) 
        
        @cmd("d38d98cc-626c-4c93-a0fa-fb03ba2b7ae2", "diagnostics_main_window")
        def diagnostics_main_window():
            """
            诊断主窗口
            """
            logger.info("diagnostics_main_window")
            vm_creator().diagnostics_main_window()
        
        @cmd("182a810e-69b2-4a5d-9ff4-496e08e01b20", "toggle_main_window_theme")
        def toggle_main_window_theme():
            """
            切换主窗口主题
            """
            logger.info("toggle_main_window_theme")
            vm_creator().toggle_main_window_theme()
        
        @cmd("eb8dc82d-2a9b-4256-a2d4-cdba41cb7131", "register_menu_pane")
        def register_menu_pane(menu_pane, view_id: str):
            """
            注册主窗口菜单面板
            """
            logger.info("register_menu_pane")
            vm_creator().register_menu_pane(menu_pane, view_id)
