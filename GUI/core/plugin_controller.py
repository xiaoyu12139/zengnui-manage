
from utils import SingletonMeta
from utils import logger

class PluginController(metaclass=SingletonMeta):
    """
    插件控制器类
    """
    def __init__(self):
        self._plugin_list = []
    
    def load_plugin(self, plugin_name: str):
        """
        加载插件
        """
        logger.info(f"加载插件: {plugin_name}")

        