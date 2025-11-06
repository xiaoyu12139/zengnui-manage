from core import cmd, Global
from ...views import CardQuickOptionView

class CardQuickOptionCmdHandler:
    """
    卡片快捷操作命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装卡片快捷操作命令
        """

        @cmd("c4c830cc-5572-4a35-abe8-3265911e5a93", "activate_card_quick_option_view")
        def activate_card_quick_option_view():
            """
            激活卡片快捷操作视图
            """
            win_id = Global().views_manager.instance_view(str(hash(CardQuickOptionView)))
            instance = Global().views_manager.get_view_instance(win_id)
            return instance
