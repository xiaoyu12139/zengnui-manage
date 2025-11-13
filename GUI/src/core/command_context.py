import threading

class CommandContext:
    """
    命令上下文类
    """
    _local = threading.local()

    @classmethod
    def get_current_instance(cls) -> "Plugin":
        """
        获取当前命令上下文实例
        """
        return getattr(cls._local, "current_instance", None)
    
    @classmethod
    def set_current_instance(cls, instance: "Plugin"):
        """
        设置当前命令上下文实例
        """
        setattr(cls._local, "current_instance", instance)
    
    @classmethod
    def clear_current_instance(cls):
        """
        清除当前命令上下文实例
        """
        if hasattr(cls._local, "current_instance"):
            delattr(cls._local, "current_instance")