from ..viewmodels import SettingsViewModel, SubGenerateSettingWidgetViewModel
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

    def create_sub_generate_setting_widget_vm_instance(self, context) -> Callable[[], SubGenerateSettingWidgetViewModel]:
        """
        创建Settings视图模型实例
        """
        sub_generate_setting_widget_vm = None
        def _create_sub_generate_setting_widget_vm() -> SubGenerateSettingWidgetViewModel:
            nonlocal sub_generate_setting_widget_vm
            if sub_generate_setting_widget_vm is None:
                sub_generate_setting_widget_vm = SubGenerateSettingWidgetViewModel(context)
            return sub_generate_setting_widget_vm
        return _create_sub_generate_setting_widget_vm
