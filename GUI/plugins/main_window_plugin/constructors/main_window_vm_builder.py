from typing import Callable
from plugins.main_window_plugin.viewmodels import MainWindowViewModel

class MainWindowVMBuilder:
    """
    主窗口视图模型构建类
    """
    def create_main_window_vm_instance(self, context) -> Callable[[], MainWindowViewModel]:
        """
        创建主窗口视图模型实例
        """
        main_window_vm = None
        def _create_main_window_vm() -> MainWindowViewModel:
            nonlocal main_window_vm
            if main_window_vm is None:
                main_window_vm = MainWindowViewModel(context)
            return main_window_vm
        return _create_main_window_vm
    