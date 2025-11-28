######import_start######
from core import cmd, Global, pcmd
######constructor_start######
######constructor_end######
######ui_start######
######ui_end######
######view_start######
from ...views.card_config_view import CardConfigView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######

class CardConfigCmdHandler:
    """
    CardConfig 命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装 CardConfig 命令
        """

        @pcmd("get_card_config")
        def get_card_config():
            """
            获取 CardConfig 插件
            """
            view_id = Global().views_manager.instance_view(str(hash(CardConfigView)), vm_creator())
            instance = Global().views_manager.get_view_instance(view_id)
            return instance