class ViewsManager:
    """
    视图管理器类
    """
    def __init__(self):
        self.__window_objs = {}  # 实例
        self.__window_types = {} # 类
    
    def register_view(self, view_id: str, view: type):
        """
        注册主窗口
        """
        self.__window_types[view_id] = view