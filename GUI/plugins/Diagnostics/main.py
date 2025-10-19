from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QSizePolicy


class Plugin:
    zone = "dock"
    dock_title = "消息与诊断"

    def build(self, main_window) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(12)
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.log.setText("""[INFO] update-change-dir 成功创建模块与宏\n[INFO] 已配置 AutoRun 自动加载宏\n[WARN] Windows Terminal 启动参数包含 /d，AutoRun 将被禁用\n[HINT] 新开 CMD 窗口或手动 call load.cmd""")
        self.log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v.addWidget(self.log, 1)
        
        # 注册为诊断日志 sink
        main_window.register_diagnostics_sink(self)
        return w

    def append_log(self, level: str, message: str) -> None:
        # 追加一行日志，保持简单格式
        self.log.append(f"[{level}] {message}")