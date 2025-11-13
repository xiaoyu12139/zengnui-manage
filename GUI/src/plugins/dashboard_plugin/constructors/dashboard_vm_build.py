######import_start######
######constructor_start######
from ..viewmodels.dashboard_view_model import DashboardViewModel
######constructor_end######
######ui_start######
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
from ..viewmodels.card_config_viewmodel import CardConfigViewModel
from ..viewmodels.card_quick_option_viewmodel import CardQuickOptionViewModel
######viewmodel_end######
######import_end######
from typing import Callable

class DashboardViewModelBuilder:
    """
    Dashboard视图模型构建类
    """
    ######vmbuild_method_start######
    def create_dashboard_vm_instance(self, context) -> Callable[[], DashboardViewModel]:
        """
        创建Dashboard视图模型实例
        """
        dashboard_vm = None
        def _create_dashboard_vm() -> DashboardViewModel:
            nonlocal dashboard_vm
            if dashboard_vm is None:
                dashboard_vm = DashboardViewModel(context)
            return dashboard_vm
        return _create_dashboard_vm

    def create_card_config_vm_instance(self, context) -> Callable[[], CardConfigViewModel]:
        """
        创建CardConfig视图模型实例
        """
        card_config_vm = None
        def _create_card_config_vm() -> CardConfigViewModel:
            nonlocal card_config_vm
            if card_config_vm is None:
                card_config_vm = CardConfigViewModel(context)
            return card_config_vm
        return _create_card_config_vm

    def create_card_quick_option_vm_instance(self, context) -> Callable[[], CardQuickOptionViewModel]:
        """
        创建CardQuickOption视图模型实例
        """
        card_quick_option_vm = None
        def _create_card_quick_option_vm() -> CardQuickOptionViewModel:
            nonlocal card_quick_option_vm
            if card_quick_option_vm is None:
                card_quick_option_vm = CardQuickOptionViewModel(context)
            return card_quick_option_vm
        return _create_card_quick_option_vm
    ######vmbuild_method_end######