class StatusBarVMBuilder:
    """
    状态栏视图模型构建器类
    """
    def create_status_bar_vm_instance(self, context) -> Callable[[], StatusBarViewModel]:
        """
        创建状态栏视图模型实例
        """
        status_bar_vm = None
        def _create_status_bar_vm() -> StatusBarViewModel:
            nonlocal status_bar_vm
            if status_bar_vm is None:
                status_bar_vm = StatusBarViewModel(context)
            return status_bar_vm
        return _create_status_bar_vm
