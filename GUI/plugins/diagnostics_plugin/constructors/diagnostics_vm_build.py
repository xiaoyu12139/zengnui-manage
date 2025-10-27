from ..viewmodels import DiagnosticsViewModel
from typing import Callable

class DiagnosticsVMBuilder:
    """
    诊断视图模型构建器类
    """
    def create_diagnostics_vm_instance(self, context) -> Callable[[], DiagnosticsViewModel]:
        """
        创建诊断视图模型实例
        """
        diagnostics_vm = None
        def _create_diagnostics_vm() -> DiagnosticsViewModel:
            nonlocal diagnostics_vm
            if diagnostics_vm is None:
                diagnostics_vm = DiagnosticsViewModel(context)
            return diagnostics_vm
        return _create_diagnostics_vm
