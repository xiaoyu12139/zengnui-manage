from utils.meta_class import SingletonMeta


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
            self.__commands[key] = value
            self.__command_names.append(value.cmd_terminal)
            self.__name_to_key_map[value.cmd_terminal] = key
    
    def cmd(self, cmd_id: str, *args, **kwargs):
        """
        执行命令
        """
        if cmd_id in self.__commands:
            self.__commands[cmd_id].exec(*args, **kwargs)
        else:
            print(f"命令 {cmd_id} 不存在")
    
    def execute_command(self, name: str, *args, **kwargs):
        """
        执行命令
        """
        key = self.__name_to_key_map[name]
        self.cmd(key, *args, **kwargs)