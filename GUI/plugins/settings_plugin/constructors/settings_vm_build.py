from ..viewmodels import SettingsViewModel
from typing import Callable

class SettingsViewModelBuilder:
    """
    设置视图模型构建类
    """
    def create_settings_vm_instance(self, context) -> Callable[[], SettingsViewModel]:
        """
        创建设置视图模型实例
        """
        settings_vm = None
        def _create_settings_vm() -> SettingsViewModel:
            nonlocal settings_vm
            if settings_vm is None:
                settings_vm = SettingsViewModel(context)
            return settings_vm
        return _create_settings_vm