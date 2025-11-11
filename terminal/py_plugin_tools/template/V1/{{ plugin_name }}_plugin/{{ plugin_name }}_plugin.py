######import_start######
from core import Plugin, Global
#constructor_start
from .constructors.{{ plugin_name }}_vm_build import {{ PluginName }}ViewModelBuilder
from .constructors.{{ plugin_name }}_vm_build.{{ feat_name }}.{{ feat_name }}_cmd_handler import {{ FeatName }}CmdHandler
#constructor_end
#ui_start
#ui_end
#view_start
from .views import {{ PluginName }}View
#view_end
#viewmodel_start
#viewmodel_end
######import_end######

def instance():
    return {{ PluginName }}Plugin()

class {{ PluginName }}Plugin(Plugin, {{ PluginName }}ViewModelBuilder):

    def __init__(self):
        super().__init__()
        ######plugin_init_start######
        self.{{ feat_name }}_cmd_handler = {{ FeatName }}CmdHandler()
        ######plugin_init_end######
    
    def initialize(self):
        ######plugin_initialize_start######
        Global().views_manager.register_view(str(hash({{ FeatName }}View)), {{ FeatName }}View)
        ######plugin_initialize_end######
        
    def assembled(self, context):
        ######plugin_assembled_start######
        self.{{ feat_name }}_cmd_handler.assemble_cmd(self.create_{{ feat_name }}_vm_instance(context))
        ######plugin_assembled_end######
        