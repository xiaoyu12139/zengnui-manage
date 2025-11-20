######import_start######
from core import cmd, Global

######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views.settings_view import SettingsView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######


class SettingsCmdHandler:
    """
    Settings 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 Settings 命令
        """

        @cmd("60525ba9-3f53-4661-9077-7d987c5e13a4", "activate_settings")
        def activate_settings():
            """
            激活设置插件
            """
            view_id = Global().views_manager.instance_view(
                str(hash(SettingsView)), vm_creator()
            )
            instance = Global().views_manager.get_view_instance(view_id)
            instance.init_view()
            # 注册插件到主界面
            Global().command_manager.execute_command(
                "register_menu_pane", instance, view_id
            )
