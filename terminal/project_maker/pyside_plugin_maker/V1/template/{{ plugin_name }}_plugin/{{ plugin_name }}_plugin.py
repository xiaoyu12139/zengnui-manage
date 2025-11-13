{{ placeholder_import_start }}
from core import Plugin, Global, Context, cmd
{{ placeholder_constructor_start }}
from .constructors.{{ plugin_name }}_vm_build import {{ PluginName }}ViewModelBuilder
from .constructors.{{ feat_name }}.{{ feat_name }}_cmd_handler import {{ FeatName }}CmdHandler
{{ placeholder_constructor_end }}
{{ placeholder_ui_start }}
{{ placeholder_ui_end }}
{{ placeholder_view_start }}
from .views.{{ feat_name }}_view import {{ FeatName }}View
{{ placeholder_view_end }}
{{ placeholder_viewmodel_start }}
{{ placeholder_viewmodel_end }}
{{ placeholder_import_end }}

def instance():
    return {{ PluginName }}Plugin()

class {{ PluginName }}Plugin(Plugin, {{ PluginName }}ViewModelBuilder):

    def __init__(self):
        super().__init__()
        {{ placeholder_plugin_init_start }}
        self.{{ feat_name }}_cmd_handler = {{ FeatName }}CmdHandler()
        {{ placeholder_plugin_init_end }}
    
    def initialize(self):
        {{ placeholder_plugin_initialize_start }}
        Global().views_manager.register_view(str(hash({{ FeatName }}View)), {{ FeatName }}View)
        {{ placeholder_plugin_initialize_end }}
        
    def assembled(self, context):
        {{ placeholder_plugin_assembled_start }}
        self.{{ feat_name }}_cmd_handler.assemble_cmd(self.create_{{ feat_name }}_vm_instance(context))
        {{ placeholder_plugin_assembled_end }}
        