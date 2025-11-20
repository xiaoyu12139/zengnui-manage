######import_start######
from core import cmd, Global
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views.card_quick_option_view import CardQuickOptionView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class CardQuickOptionCmdHandler:
    """
    CardQuickOption 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 CardQuickOption 命令
        """

        @pcmd("activate_card_quick_option")
        def activate_card_quick_option():
            """
            激活 CardQuickOption 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(CardQuickOptionView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            return instance