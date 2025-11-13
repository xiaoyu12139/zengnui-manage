######import_start######
from core import Plugin, Global, Context, cmd

######constructor_start######
from .constructors.main_window_vm_build import MainWindowViewModelBuilder
from .constructors.main_window.main_window_cmd_handler import (
    MainWindowCmdHandler,
)
from .constructors.top_bar.top_bar_cmd_handler import TopBarCmdHandler
from .constructors.status_bar.status_bar_cmd_handler import StatusBarCmdHandler
from .constructors.diagnostics.diagnostics_cmd_handler import (
    DiagnosticsCmdHandler,
)

######constructor_end######
######ui_start######
######ui_end######
######view_start######
from .views.main_window_view import MainWindowView
from .views.top_bar_view import TopBarView
from .views.status_bar_view import StatusBarView
from .views.diagnostics_view import DiagnosticsView
######view_end######
######viewmodel_start######
######viewmodel_end######
######import_end######


def instance():
    return MainWindowPlugin()


class MainWindowPlugin(Plugin, MainWindowViewModelBuilder):
    def __init__(self):
        super().__init__()
        ######plugin_init_start######
        self.main_window_cmd_handler = MainWindowCmdHandler()
        self.top_bar_cmd_handler = TopBarCmdHandler()
        self.status_bar_cmd_handler = StatusBarCmdHandler()
        self.diagnostics_cmd_handler = DiagnosticsCmdHandler()
        ######plugin_init_end######

    def initialize(self):
        ######plugin_initialize_start######
        Global().views_manager.register_view(
            str(hash(MainWindowView)), MainWindowView
        )
        Global().views_manager.register_view(str(hash(TopBarView)), TopBarView)
        Global().views_manager.register_view(
            str(hash(StatusBarView)), StatusBarView
        )
        Global().views_manager.register_view(
            str(hash(DiagnosticsView)), DiagnosticsView
        )
        ######plugin_initialize_end######

    def assembled(self, context):
        ######plugin_assembled_start######
        self.main_window_cmd_handler.assemble_cmd(
            self.create_main_window_vm_instance(context)
        )
        self.top_bar_cmd_handler.assemble_cmd(
            self.create_top_bar_vm_instance(context)
        )
        self.status_bar_cmd_handler.assemble_cmd(
            self.create_status_bar_vm_instance(context)
        )
        self.diagnostics_cmd_handler.assemble_cmd(
            self.create_diagnostics_vm_instance(context)
        )
        ######plugin_assembled_end######

    @cmd("f64715b7-8a60-4f78-b42b-6b935b63a32c", "startup")
    def load_support_plugins(self, *args):
        """
        加载支持插件
        """
        # 创建一个上下文
        context = Context()
        Global().plugin_manager.load_all_plugins()
        # 遍历插件管理器中的所有插件
        for plugin in Global().plugin_manager.plugin_list:
            # 调用插件的assemble方法传入context
            plugin.assembled(context)
        # 显示主窗口
        Global().command_manager.execute_command("activate_main_window")
