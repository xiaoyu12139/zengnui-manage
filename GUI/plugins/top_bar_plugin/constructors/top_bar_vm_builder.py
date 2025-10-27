class TopBarVMBuilder:
    """
    顶部栏视图模型构建器类
    """
    def create_top_bar_vm_instance(self, context) -> Callable[[], TopBarViewModel]:
        """
        创建顶部栏视图模型实例
        """
        top_bar_vm = None
        def _create_top_bar_vm() -> TopBarViewModel:
            nonlocal top_bar_vm
            if top_bar_vm is None:
                top_bar_vm = TopBarViewModel(context)
            return top_bar_vm
        return _create_top_bar_vm
