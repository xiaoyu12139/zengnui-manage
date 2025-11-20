from .event_bus import EventBus
from .app_global import Global
import re

class Context:
    def __init__(self, global_bus: EventBus | None = None, current_plugin: str | None = None):
        self._global_bus = global_bus or EventBus()
        self._plugin_buses: dict[str, EventBus] = {}
        self._current_plugin = current_plugin

    @property
    def event_bus(self) -> EventBus:
        return self._global_bus
    
    @property
    def plugin_name(self) -> str | None:
        """
        当前插件的名称
        """
        class_name = self._current_plugin.__class__.__name__
        if class_name.endswith('Plugin'):
            class_name = class_name[:-6]
        return class_name

    def get_plugin_bus(self, name: str) -> EventBus:
        bus = self._plugin_buses.get(name)
        if bus is None:
            bus = EventBus()
            self._plugin_buses[name] = bus
        return bus

    def on(self, topic: str, handler, *, once: bool = False):
        self._global_bus.subscribe(topic, handler, once=once)

    def emit(self, topic: str, *args, **kwargs):
        self._global_bus.publish(topic, *args, **kwargs)

    def ask(self, topic: str, *args, **kwargs):
        return self._global_bus.request(topic, *args, **kwargs)

    def cmd(self, cmd_id: str, *args, **kwargs):
        return Global().command_manager.cmd(cmd_id, *args, **kwargs)

    def execute(self, terminal: str, *args, **kwargs):
        return Global().command_manager.execute_command(terminal, *args, **kwargs)

    def plugin_execute(self, feature: str, action: str, *args, **kwargs):
        """
        执行插件的命令
        """
        if self.plugin_name is None:
            raise ValueError("当前上下文没有插件")
        
        def _camel_to_snake(name: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        plugin_name = _camel_to_snake(self.plugin_name)
        feature_name = _camel_to_snake(feature)
        terminal = f"{plugin_name}.{feature_name}.{action}"
        return Global().command_manager.execute_command(terminal, *args, **kwargs)
