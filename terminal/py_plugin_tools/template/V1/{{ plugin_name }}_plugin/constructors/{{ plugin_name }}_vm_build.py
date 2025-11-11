######import_start######
#constructor_start
#constructor_end
#ui_start
#ui_end
#view_start
#view_end
#viewmodel_start
from ..viewmodels.{{ feat_name }}_view_model import {{ feat_name }}ViewModel
#viewmodel_end
######import_end######
from typing import Callable

class {{ FeatName }}ViewModelBuilder:
    """
    {{ FeatName }}视图模型构建类
    """
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
