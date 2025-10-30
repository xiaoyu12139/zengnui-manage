from pathlib import Path
import subprocess
import shutil
import re

CURRENT_DIR = Path(__file__).parent

def to_pascal_case(name: str) -> str:
    """将文件名（如 main_window、top-widget）转换为大驼峰（MainWindow、TopWidget）。"""
    parts = re.findall(r"[A-Za-z0-9]+", name)
    return ''.join(p.capitalize() for p in parts if p)

def build_all_ui():
    # 清除所有ui_widget下的带有plugin结尾的文件夹
    ui_widget_path = CURRENT_DIR.parent / "plugins" / "ui_widget"
    if ui_widget_path.exists():
        for f in ui_widget_path.rglob("*plugin"):
            if f.is_dir():
                print(f"删除非空文件夹（递归）：{f}")   
                shutil.rmtree(f)
    else:
        print(f"ui_widget路径不存在：{ui_widget_path}")
    ui_path = CURRENT_DIR.parent / "resource" / "ui"
    print(f"ui资源文件夹：{ui_path}\n")
    for f in ui_path.rglob("*.ui"):
        print(f"编译UI文件：{f}")
        # 编译UI文件
        out_parent = CURRENT_DIR.parent / 'plugins' / 'ui_widget' / f.parent.name
        if not out_parent.exists():
            out_parent.mkdir(parents=True)
            open(out_parent / "__init__.py", "w").close() # 创建空的__init__.py文件
        cmd = f"pyside6-uic {f} -o {out_parent / (f.stem + '.py')}"
        f_init = open(out_parent / "__init__.py", "a") # 以追加模式打开__init__.py文件
        # 将文件名转换为真正的大驼峰（PascalCase），如 main_window -> MainWindow
        class_name = to_pascal_case(f.stem)
        f_init.write(f"from .{f.stem} import Ui_{class_name}\n")
        f_init.close()
        print(f"执行命令：{cmd}")
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    # 编译所有UI文件
    print("编译所有UI文件...")
    build_all_ui()