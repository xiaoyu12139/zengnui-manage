from ..viewmodels import DashboardViewModel
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
