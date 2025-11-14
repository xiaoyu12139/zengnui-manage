from .event_bus import EventBus
from .app_global import Global

class Context:
    def __init__(self, global_bus: EventBus | None = None):
        self._global_bus = global_bus or EventBus()
        self._plugin_buses: dict[str, EventBus] = {}

    @property
    def event_bus(self) -> EventBus:
        return self._global_bus

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

    def plugin_execute(self, plugin: str, feature: str, action: str, *args, **kwargs):
        terminal = f"{plugin}.{feature}.{action}"
        return Global().command_manager.execute_command(terminal, *args, **kwargs)
