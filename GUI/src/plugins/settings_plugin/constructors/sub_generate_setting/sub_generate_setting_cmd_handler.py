######import_start######
from core import cmd, Global, pcmd
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views.sub_generate_setting_view import SubGenerateSettingView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class SubGenerateSettingCmdHandler:
    """
    SubGenerateSetting 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 SubGenerateSetting 命令
        """

        @pcmd("activate_sub_generate_setting")
        def activate_sub_generate_setting():
            """
            激活 SubGenerateSetting 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(SubGenerateSettingView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            return instance