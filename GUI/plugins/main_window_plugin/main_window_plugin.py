from core import Global, Plugin, Context, cmd
from .views import MainWindowView
from .viewmodels import MainWindowViewModel
from .constructors import MainWindowVMBuilder, MainWindowCommandHandler

def instance():
    return MainWindowPlugin()

class MainWindowPlugin(Plugin, MainWindowVMBuilder):
    """
    主窗口插件类
    """
    def __init__(self):
        super().__init__()
        self.main_window_cmd_handle = MainWindowCommandHandler()
        
    
    def initialize(self):
        """
        初始化插件
        """
        Global().views_manager.register_view(str(hash(MainWindowView)), MainWindowView)
    
    def assembled(self, context):
        """
        组装插件
        """
        self.main_window_cmd_handle.assemble_cmd(self.create_main_window_vm_instance(context))
    
    @cmd("f64715b7-8a60-4f78-b42b-6b935b63a32c", "startup")
    def load_support_plugins(self, *args):
        """
        加载支持插件
        """
        # 创建一个上下文
        context = Context()
        Global().plugin_manager.load_all_plugins()
        # 遍历插件管理器中的所有插件
        for plugin in Global().plugin_manager.plugin_list:
            # 调用插件的assemble方法传入context
            plugin.assembled(context)
        # 显示主窗口
        Global().command_manager.execute_command("activate_main_window")
    
    