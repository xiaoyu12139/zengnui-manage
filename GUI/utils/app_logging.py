import logging
from .meta_class import SingletonMeta

class AppLogging(metaclass=SingletonMeta):
    """
    应用日志类
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        # 添加控制台处理器到日志记录器
        self._logger.addHandler(console_handler)
    
    def info(self, msg: str):
        """
        记录INFO级别的日志
        """
        self._logger.info(msg)

__logger = AppLogging()