
from utils import SingletonMeta
from .plugin_controller import PluginController
from .command_controller import CommandController
from .message_queue import MessageQueue

class Global(metaclass=SingletonMeta):
    """
    全局管理类
    """
    def __init__(self):
        self._plugin_controller = PluginController()
        self._command_controller = CommandController()
        self._message_queue = MessageQueue()
    
    def load_core(self):
        """
        加载app需要的基础核心组件
        """
        self._plugin_controller.load_core()
    
    @property
    def plugin_controller(self):
        return self._plugin_controller
    
    @property
    def command_controller(self):
        return self._command_controller
    
    @property
    def message_queue(self):
        return self._message_queue