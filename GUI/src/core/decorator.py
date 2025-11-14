
from typing import Callable
import functools
import re
from .command_context import CommandContext

def cmd(coommand: str, terminal: str) -> Callable:
    """
    命令装饰器
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            return func(*args, **kwargs)
        
        # 设置命令元数据
        setattr(wrapper, "__cmd_id__", coommand)
        setattr(wrapper, "__terminal__", terminal)
        instance = CommandContext.get_current_instance()
        if instance:
            return instance.cmd(coommand, terminal)(wrapper)
        else:
            return wrapper
    return decorator

def pcmd(feature: str, action: str) -> Callable:
    def _camel_to_snake(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _derive_plugin_name(func: Callable) -> str:
        instance = CommandContext.get_current_instance()
        if instance is not None:
            cls = instance.__class__.__name__
            if cls.endswith('Plugin'):
                cls = cls[:-6]
            return _camel_to_snake(cls)
        mod = getattr(func, '__module__', '')
        parts = mod.split('.plugins.')
        if len(parts) > 1:
            rest = parts[1]
            seg = rest.split('.', 1)[0]
            return seg.replace('_plugin', '').lower()
        return 'plugin'

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            return func(*args, **kwargs)

        plugin = _derive_plugin_name(wrapper)
        terminal = f"{plugin}.{feature}.{action}"
        setattr(wrapper, "__cmd_id__", terminal)
        setattr(wrapper, "__terminal__", terminal)
        instance = CommandContext.get_current_instance()
        if instance:
            return instance.cmd(terminal, terminal)(wrapper)
        else:
            return wrapper
    return decorator
