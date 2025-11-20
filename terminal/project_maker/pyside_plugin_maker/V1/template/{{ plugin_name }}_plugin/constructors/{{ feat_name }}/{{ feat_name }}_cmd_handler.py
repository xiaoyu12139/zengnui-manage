{{ placeholder_import_start }}
from core import cmd, Global
{{ placeholder_constructor_start }}
{{ placeholder_constructor_end }}
{{ placeholder_ui_start }}
{{ placeholder_ui_end }}
{{ placeholder_view_start }}
from ...views.{{ feat_name }}_view import {{ FeatName }}View
{{ placeholder_view_end }}
{{ placeholder_viewmodel_start }}
{{ placeholder_viewmodel_end }}
{{ placeholder_import_end }}

class {{ FeatName }}CmdHandler:
    """
    {{ FeatName }} 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 {{ FeatName }} 命令
        """

        @cmd("", "activate_{{ feat_name }}")
        def activate_{{ feat_name }}():
            """
            激活 {{ FeatName }} 插件
            """
            view_id = Global().views_manager.instance_view(str(hash({{ FeatName }}View)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            # 注册插件到主界面
            # Global().command_manager.execute_command("register_menu_pane", instance, view_id)