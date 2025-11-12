{{ placeholder_import_start }}
{{ placeholder_constructor_start }}
from ..viewmodels.{{ feat_name }}_view_model import {{ FeatName }}ViewModel
{{ placeholder_constructor_end }}
{{ placeholder_ui_start }}
{{ placeholder_ui_end }}
{{ placeholder_view_start }}
{{ placeholder_view_end }}
{{ placeholder_viewmodel_start }}
{{ placeholder_viewmodel_end }}
{{ placeholder_import_end }}
from typing import Callable

class {{ FeatName }}ViewModelBuilder:
    """
    {{ FeatName }}视图模型构建类
    """
    {{ placeholder_vmbuild_method_start }}
    def create_{{ feat_name }}_vm_instance(self, context) -> Callable[[], {{ FeatName }}ViewModel]:
        """
        创建{{ FeatName }}视图模型实例
        """
        {{ feat_name }}_vm = None
        def _create_{{ feat_name }}_vm() -> {{ FeatName }}ViewModel:
            nonlocal {{ feat_name }}_vm
            if {{ feat_name }}_vm is None:
                {{ feat_name }}_vm = {{ FeatName }}ViewModel(context)
            return {{ feat_name }}_vm
        return _create_{{ feat_name }}_vm
    {{ placeholder_vmbuild_method_end }}

