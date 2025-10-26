
from utils import SingletonMeta
from utils import logger
import importlib

from pathlib import Path

CURRENT_DIR = Path(__file__).parent.parent

class PluginManager(metaclass=SingletonMeta):
    """
    插件管理器类
    """
    def __init__(self):
        self._plugin_list = []
        self._plugin_base_path = CURRENT_DIR / "plugins"
    
    def load_plugin(self, plugin_name: str):
        """
        加载插件
        """
        logger.info(f"加载插件: {plugin_name}")
        # load plugin
        module_name = "plugins." + plugin_name + "." + plugin_name
        module = importlib.import_module(module_name)
        plugin = getattr(module, "instance")()
        plugin.initialize()
        self._plugin_list.append(plugin)
    
    @property
    def plugin_list(self):
        """
        获取插件
        """
        return self._plugin_list
    
    def load_all_plugins(self):
        """
        加载所有插件
        """
        logger.info(f"插件路径: {self._plugin_base_path}")
        self._plugin_list.clear()
        # 遍历插件路径下的所有文件夹
        for plugin_dir in self._plugin_base_path.iterdir():
            if plugin_dir.is_dir():
                # 加载插件
                try:
                    self.load_plugin(plugin_dir.name)
                except Exception as e:
                    logger.error(f"加载插件 {plugin_dir.name} 失败: {e}")
        
        

        