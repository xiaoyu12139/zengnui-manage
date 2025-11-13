######import_start######
######constructor_start######
from ..viewmodels.settings_view_model import SettingsViewModel
######constructor_end######
######ui_start######
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######
from typing import Callable

class SettingsViewModelBuilder:
    """
    Settings视图模型构建类
    """
    ######vmbuild_method_start######
    def create_settings_vm_instance(self, context) -> Callable[[], SettingsViewModel]:
        """
        创建Settings视图模型实例
        """
        settings_vm = None
        def _create_settings_vm() -> SettingsViewModel:
            nonlocal settings_vm
            if settings_vm is None:
                settings_vm = SettingsViewModel(context)
            return settings_vm
        return _create_settings_vm
    ######vmbuild_method_end######
