import logging

class AppLogging(object):
    """
    应用日志类
    """
    def __init__(self, name: str):
        name_str = name if name else __name__
        self._logger = logging.getLogger(name_str)
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
    
    def error(self, msg: str):
        """
        记录ERROR级别的日志
        """
        self._logger.error(msg)

__logger = AppLogging(None)

def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器
    """
    tmp_logger = AppLogging(name)
    return tmp_logger