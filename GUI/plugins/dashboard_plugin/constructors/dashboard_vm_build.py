from ..viewmodels import DashboardViewModel, CardConfigViewModel, CardQuickOptionViewModel
from typing import Callable

class DashboardViewModelBuilder:
    """
    仪表盘视图模型构建类
    """

    def create_dashboard_vm_instance(self, context) -> Callable[[], DashboardViewModel]:
        """
        创建仪表盘视图模型实例
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
        创建卡片配置视图模型实例
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
        创建卡片快捷操作视图模型实例
        """
        card_quick_option_vm = None
        def _create_card_quick_option_vm() -> CardQuickOptionViewModel:
            nonlocal card_quick_option_vm
            if card_quick_option_vm is None:
                card_quick_option_vm = CardQuickOptionViewModel(context)
            return card_quick_option_vm
        return _create_card_quick_option_vm