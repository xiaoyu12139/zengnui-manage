
from typing import Callable
import functools
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