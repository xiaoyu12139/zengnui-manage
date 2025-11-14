
from utils import SingletonMeta
from .plugin_manager import PluginManager
from .command_manager import CommandManager
from .views_manager import ViewsManager

class Global(metaclass=SingletonMeta):
    """
    全局管理类
    """
    def __init__(self):
        self._plugin_manager = PluginManager()
        self._command_manager = CommandManager()
        self._views_manager = ViewsManager()
    
    def load_core(self):
        """
        加载app需要的基础核心组件
        """
        self._plugin_manager.load_core()
    
    @property
    def plugin_manager(self):
        return self._plugin_manager
    
    @property
    def command_manager(self):
        return self._command_manager
    
    @property
    def views_manager(self):
        return self._views_manager