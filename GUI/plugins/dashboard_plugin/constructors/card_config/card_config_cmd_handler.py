from core import cmd, Global
from ...views import CardConfigView

class CardConfigCmdHandler:
    """
    卡片配置命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装卡片配置命令
        """

        @cmd("be2189d6-c93b-4762-a0b6-e09c9a41a9bf", "activate_card_config_view")
        def activate_card_config_view():
            """
            激活卡片配置视图
            """
            win_id = Global().views_manager.instance_view(str(hash(CardConfigView)))
            instance = Global().views_manager.get_view_instance(win_id)
            return instance