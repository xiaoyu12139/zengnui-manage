######import_start######
######constructor_start######
from ..viewmodels.settings_view_model import SettingsViewModel
######constructor_end######
######ui_start######
######ui_end######
######view_start######
######view_end######
######viewmodel_start######
from ..viewmodels.sub_generate_setting_viewmodel import SubGenerateSettingViewModel
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

    def create_sub_generate_setting_vm_instance(self, context) -> Callable[[], SubGenerateSettingViewModel]:
        """
        创建SubGenerateSetting视图模型实例
        """
        sub_generate_setting_vm = None
        def _create_sub_generate_setting_vm() -> SubGenerateSettingViewModel:
            nonlocal sub_generate_setting_vm
            if sub_generate_setting_vm is None:
                sub_generate_setting_vm = SubGenerateSettingViewModel(context)
            return sub_generate_setting_vm
        return _create_sub_generate_setting_vm
    ######vmbuild_method_end######