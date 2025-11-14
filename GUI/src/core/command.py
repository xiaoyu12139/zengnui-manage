from utils import get_logger
from typing import Callable, Any

logger = get_logger("Command")

class Command:
    """
    命令类
    """
    def __init__(self) -> None:
        self.__cmd_terminal = None
        self.__callable = None
        self.__cmd_id = None
    
    @property
    def cmd_id(self) -> str:
        """
        获取命令ID
        """
        return self.__cmd_id
    
    @property
    def cmd_terminal(self) -> str:
        """
        获取命令终端
        """
        return self.__cmd_terminal
    
    @property
    def callable(self) -> Callable:
        """
        获取可调用对象
        """
        return self.__callable
    
    def register_callable(self, cmd_id: str, terminal: str, callable: Callable) -> None:
        """
        注册可调用对象
        """
        self.__callable = callable
        self.__cmd_id = cmd_id
        self.__cmd_terminal = terminal
    
    def exec(self, *args, **kwargs) -> Any:
        """
        执行命令
        """
        if self.__callable is None:
            logger.error(f"Command {self.__cmd_id} on terminal {self.__cmd_terminal} is not registered.")
            return 
        return self.__callable(*args, **kwargs)
