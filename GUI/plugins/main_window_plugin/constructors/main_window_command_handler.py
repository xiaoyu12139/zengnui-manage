from core import cmd

class MainWindowCommandHandler:
    """
    主窗口命令处理类
    """

    def assemble_cmd(self, vm_creator: callable):
        """
        组装主窗口命令
        """
        @cmd("ed23f387-7767-41bd-a8dc-29bc9025e2b0", "activate_main_window")
        def activate_main_window():
            """
            测试方法
            """
            print("测试主窗口插件")