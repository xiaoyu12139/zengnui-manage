from core import cmd, Global
from ...views import SubGenerateSettingWidgetView
from utils import get_logger

logger = get_logger(f"SubGenerateSettingWidgetCmdHandler")

class SubGenerateSettingWidgetCmdHandler:
    """
    Settings 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装命令
        """

        @cmd("a3e8ac6f-a39a-4367-a2c7-8ff628a1c3b8", f"activate_sub_generate_setting_widget")
        def activate_sub_generate_setting_widget():
            """
            激活 SubGenerateSettingWidget 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(SubGenerateSettingWidgetView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            return instance