######import_start######
from core import cmd, Global
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views import DiagnosticsView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class DiagnosticsCmdHandler:
    """
    Diagnostics 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 Diagnostics 命令
        """

        @cmd("be226367-b4c3-4ca3-b36e-10a5aed58ecf", "activate_diagnostics")
        def activate_diagnostics():
            """
            激活 Diagnostics 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(DiagnosticsView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            # 注册插件到主界面
            # Global().command_manager.execute_command("register_menu_pane", instance, view_id)