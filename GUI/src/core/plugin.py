from typing import Callable
import functools
from .command_manager import CommandManager
from .context import Context
from .app_global import Global
from .command import Command
import types
from .command_context import CommandContext
from utils import get_logger

logger = get_logger("Plugin")

class Plugin:
    """
    插件基类
    """
    def __init__(self):
        """3
        """
        self.local_commands = {}
        self.collect_and_register_commands()
    
    def cmd(self, command: str, terminal: str = "") -> Callable:
        """2
        实例方法版本的命令装饰器
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args,**kwargs):
                return func(*args,**kwargs)
            self.local_commands[command] = func
            return wrapper
        return decorator

    def __init_subclass__(cls, **kwargs):
        """1
        子类初始化
        """
        if hasattr(cls, "assembled") and callable(cls.assembled):
            cls.assembled = cls._enable_cmd_decorator(cls.assembled)
        
        cls.global_commands = {}
        for _, method in cls.__dict__.items():
            # 处理静态方法和类方法
            if isinstance(method, (staticmethod, classmethod)):
                func = method.__func__
            else:
                func = method
            # 检查装饰器标记
            if hasattr(func, "__cmd_id__"):
                cmd_id = getattr(func, "__cmd_id__")
                cls.global_commands[cmd_id] = method

    def _enable_cmd_decorator(func: Callable) -> Callable:
        """
        命令装饰器
        """
        @functools.wraps(func)
        def wrapper(self:"PLugin",context:"Context",*args,**kwargs):
            #设置当前实例到上下文
            try:
                #执行原始方法
                CommandContext.set_current_instance(self)
                try:
                    setattr(self, "_context", context)
                    assambled_result = func(self,context,*args,**kwargs)
                except Exception as err:
                    logger.error(f"An error occur assambling {self.__class__},{err}.")
                    return
                #注册Local command
                self.collect_and_register_commands(self.local_commands,Global().command_manager)
                return assambled_result
            finally:
                #清理上下文
                CommandContext.clear_current_instance()
        return wrapper
    
    def collect_and_register_commands(self,function_map:dict = None, cmd_manager:"CommandManager" = None):
        """
        收集并注册插件中的命令
        """
        # 确保参数同时存在与同时不存在
        if (function_map is None) != (cmd_manager is None):
            raise ValueError("function_map and cmd_manager must be provided together or not at all.")
        commands_dict = function_map or self.global_commands
        if cmd_manager is None:
            cmd_manager = Global().command_manager
        commands = {}
        for cmd_id,cmd_func in commands_dict.items():
            if isinstance(cmd_func, classmethod):
                bond_method = types.MethodType(cmd_func.__func__, self.__class__)
            elif isinstance(cmd_func, staticmethod):
                bond_method = cmd_func.__func__
            elif "<locals>" in cmd_func.__qualname__:
                bond_method = cmd_func
            else:
                bond_method = types.MethodType(cmd_func, self)
            terminal = getattr(bond_method, "__terminal__", None)
            command = Command()
            command.register_callable(cmd_id, terminal, bond_method)
            commands[cmd_id] = command
        cmd_manager.register_commands(commands)
