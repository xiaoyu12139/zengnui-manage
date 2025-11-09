from core import cmd, Global
from ...views import DashboardView

class DashboardCmdHandler:
    """
    仪表盘命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装仪表盘命令
        """

        @cmd("be226367-b4c3-4ca3-b36e-10a5aed58ecf", "activate_dashboard")
        def activate_dashboard():
            """
            激活仪表盘插件
            """
            view_id = Global().views_manager.instance_view(str(hash(DashboardView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            # 装配 dashboard 视图
            instance.assemble_view()
            # 注册插件到主界面
            Global().command_manager.execute_command("register_menu_pane", instance, view_id)