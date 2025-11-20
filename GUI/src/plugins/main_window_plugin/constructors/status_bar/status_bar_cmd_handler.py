######import_start######
from core import cmd, Global
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views.status_bar_view import StatusBarView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class StatusBarCmdHandler:
    """
    StatusBar 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 StatusBar 命令
        """

        @cmd("8ba404a6-6cb6-4804-a719-c82163773eb2", "activate_status_bar")
        def activate_status_bar(parent_widget_id):
            """
            激活 StatusBar 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(StatusBarView)), vm_creator())
            # 注册插件到主界面
            Global().views_manager.fill_widget_with_execution(
                parent_widget_id, view_id, "set_status_bar_widget"
            )