######import_start######
######constructor_start######
from ..viewmodels.main_window_view_model import MainWindowViewModel
######constructor_end######
######ui_start######
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
from ..viewmodels.top_bar_viewmodel import TopBarViewModel
from ..viewmodels.status_bar_viewmodel import StatusBarViewModel
from ..viewmodels.diagnostics_viewmodel import DiagnosticsViewModel
######viewmodel_end######
######import_end######
from typing import Callable

class MainWindowViewModelBuilder:
    """
    MainWindow视图模型构建类
    """
    ######vmbuild_method_start######
    def create_main_window_vm_instance(self, context) -> Callable[[], MainWindowViewModel]:
        """
        创建MainWindow视图模型实例
        """
        main_window_vm = None
        def _create_main_window_vm() -> MainWindowViewModel:
            nonlocal main_window_vm
            if main_window_vm is None:
                main_window_vm = MainWindowViewModel(context)
            return main_window_vm
        return _create_main_window_vm

    def create_top_bar_vm_instance(self, context) -> Callable[[], TopBarViewModel]:
        """
        创建TopBar视图模型实例
        """
        top_bar_vm = None
        def _create_top_bar_vm() -> TopBarViewModel:
            nonlocal top_bar_vm
            if top_bar_vm is None:
                top_bar_vm = TopBarViewModel(context)
            return top_bar_vm
        return _create_top_bar_vm

    def create_status_bar_vm_instance(self, context) -> Callable[[], StatusBarViewModel]:
        """
        创建StatusBar视图模型实例
        """
        status_bar_vm = None
        def _create_status_bar_vm() -> StatusBarViewModel:
            nonlocal status_bar_vm
            if status_bar_vm is None:
                status_bar_vm = StatusBarViewModel(context)
            return status_bar_vm
        return _create_status_bar_vm

    def create_diagnostics_vm_instance(self, context) -> Callable[[], DiagnosticsViewModel]:
        """
        创建Diagnostics视图模型实例
        """
        diagnostics_vm = None
        def _create_diagnostics_vm() -> DiagnosticsViewModel:
            nonlocal diagnostics_vm
            if diagnostics_vm is None:
                diagnostics_vm = DiagnosticsViewModel(context)
            return diagnostics_vm
        return _create_diagnostics_vm
    ######vmbuild_method_end######