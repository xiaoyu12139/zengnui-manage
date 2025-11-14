from utils import get_logger
from uuid import uuid1
from functools import partial
from PySide6.QtWidgets import QDialog

logger = get_logger("ViewsManager")

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
    
    def get_view_instance(self, view_id: str) -> any:
        """
        获取主窗口实例
        """
        return self.__window_objs.get(view_id)
    
    def instance_view(self, view_id: str, view_model: any, parent: str = "", force_new: bool = False, **kwargs) -> str:
        """
        获取主窗口实例
        """
        if not force_new:
            for win_id, window in self.__window_objs.items():
                if getattr(window, "view_model", None) == view_model:
                    if hasattr(window, "instance_view_id") and window.instance_view_id == view_id:
                        return win_id
        parent_widget = self.__window_objs.get(parent)
        view_type = self.__window_types.get(view_id)
        if not view_type:
            logger.error(f"View type {view_id} not registered")
            return ""
        win_id = uuid1().__str__()
        window = view_type(parent=parent_widget, **kwargs)

        setattr(window, "instance_view_id", view_id)
        
        if hasattr(view_model, "set_window_id"):
            view_model.set_window_id(win_id, view_id)
        if hasattr(window, "set_view_model"):
            window.set_view_model(view_model)
        else:
            logger.error(f"View type {view_id} not support set_view_model")
            return ""
        self.__window_objs[win_id] = window
        window.destroyed.connect(partial(self.__destroy_window, win_id))
        return win_id
    
    def __destroy_window(self, win_id: str):
        """
        销毁主窗口实例
        """
        if win_id not in self.__window_objs:
            return
        widget = self.__window_objs.pop(win_id)
        if hasattr(widget, "unlink_mode"):
            widget.unlink_mode()
            
        
    def show(self, win_id: str, *args, outer_win_id: str = None):
        """
        显示主窗口实例
        """
        if win_id not in self.__window_objs:
            return
        window = self.__window_objs[win_id]
        if outer_win_id is not None:
            outer_win = self.__window_objs.get(outer_win_id)
            if outer_win is None:
                pass
            elif hasattr(outer_win, "add_reorganized_widget"):
                outer_win.add_reorganized_widget(window)
            else:
                logger.error(f"View type {outer_win_id} not support add_reorganized_widget")
        if window.isWindow():
            window.show()
        else:
            window.showNormal()
    
    def exec(self, win_id: str, *args):
        """
        show模态窗口
        """
        if win_id not in self.__window_objs:
            return
        window = self.__window_objs[win_id]
        if isinstance(window, QDialog):
            window.exec()
        else:
            window.show()
    
    def close(self, win_id: str, *args):
        """
        关闭主窗口实例
        """
        if win_id not in self.__window_objs:
            return
        window = self.__window_objs[win_id]
        if window.isWindow():
            window.close()
        else:
            window.hide()
    
    def destroy(self, win_id: str, *args):
        """
        销毁主窗口实例
        """
        if win_id not in self.__window_objs:
            return
        window = self.__window_objs[win_id]
        if hasattr(window, "destroy"):
            window.destroy()
        window.deleteLater()
    
    def fill_widget_with_execution(self, outer_win_id: str, inner_win_id: str, exec_func, *args, **kwargs):
        """
        用模态窗口填充外部窗口
        """
        if not exec_func:
            return
        outer_widget = self.__window_objs.get(outer_win_id)
        if outer_widget is None:
            logger.error(f"View type {outer_win_id} not found")
            return
        inner_widget = self.__window_objs.get(inner_win_id)
        if inner_widget is None:
            logger.error(f"View type {inner_win_id} not found")
            return
        # 支持传入方法名字符串或可调用对象
        if isinstance(exec_func, str):
            method = getattr(outer_widget, exec_func, None)
            if not callable(method):
                logger.error(f"Method {exec_func} not found on view {outer_win_id}")
                return
            method(inner_widget, *args, **kwargs)
        else:
            exec_func(inner_widget, *args, **kwargs)

        
        
