from utils.meta_class import SingletonMeta
from utils import get_logger

logger = get_logger("CommandManager")

class CommandManager(metaclass=SingletonMeta):
    """
    命令控制器类
    """
    def __init__(self):
        self.__command_names = []
        self.__name_to_key_map = {}
        self.__commands = {}

    def register_commands(self,commands:dict):
        """
        注册命令
        """
        for key, value in commands.items():
            if key in self.__commands:
                logger.error(f"命令 {key} 已存在")
                continue
            self.__commands[key] = value
            self.__command_names.append(value.cmd_terminal)
            self.__name_to_key_map[value.cmd_terminal] = key
    
    def cmd(self, cmd_id: str, *args, **kwargs):
        """
        执行命令
        """
        try:
            if cmd_id in self.__commands:
                return self.__commands[cmd_id].exec(*args, **kwargs)
            else:
                logger.error(f"命令 {cmd_id} 不存在")
        except Exception as e:
            logger.error(f"执行命令 {cmd_id} 时出错：{e}")
    
    def execute_command(self, name: str, *args, **kwargs):
        """
        执行命令
        """
        try:
            key = self.__name_to_key_map[name]
            return self.cmd(key, *args, **kwargs)
        except KeyError:
            logger.error(f"命令 {name} 不存在")
        except Exception as e:
            logger.error(f"执行命令 {name} 时出错：{e}")