######import_start######
from core import cmd, Global

######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views import TopBarView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######


class TopBarCmdHandler:
    """
    TopBar 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 TopBar 命令
        """

        @cmd("d56194f5-4ab5-44d6-a65c-7d3161b7764a", "")
        def activate_top_bar(parent_widget_id):
            """
            激活顶部栏
            """
            top_win_id = Global().views_manager.instance_view(
                "TopBarView", vm_creator()
            )
            Global().views_manager.fill_widget_with_execution(
                parent_widget_id, top_win_id, "set_top_widget"
            )
