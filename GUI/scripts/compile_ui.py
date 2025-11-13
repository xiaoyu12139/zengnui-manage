from pathlib import Path
import subprocess
import shutil
import re
from typing import List

CURRENT_DIR = Path(__file__).parent

def to_pascal_case(name: str) -> str:
    """将文件名（如 main_window、top-widget）转换为大驼峰（MainWindow、TopWidget）。"""
    parts = re.findall(r"[A-Za-z0-9]+", name)
    return ''.join(p.capitalize() for p in parts if p)

def reset_ui_files():
    """
    重置已编译的ui文件夹
    """
    ui_widget_path = CURRENT_DIR.parent / "plugins" / "ui_widget"
    if ui_widget_path.exists():
        for f in ui_widget_path.iterdir():
            if f.is_dir() and f.name.endswith("_plugin"):
                print(f"删除ui文件夹：{f}")   
                shutil.rmtree(f)

def create_ui_plugin():
    """
    创建ui插件文件夹
    """
    ui_widget_path = CURRENT_DIR.parent / "plugins" / "ui_widget"
    ui_path = CURRENT_DIR.parent / "resource" / "ui"
    for f in ui_path.iterdir():
        if f.is_dir() and f.name.endswith("_plugin"):
            (ui_widget_path / f"{f.name}").mkdir()
            (ui_widget_path / f"{f.name}" / "__init__.py").touch() # 创建空的__init__.py文件

def main():
    """
    编译UI文件
    """
    print("重置已编译的ui文件夹")
    reset_ui_files()
    create_ui_plugin()
    print("编译UI文件")
    ui_path = CURRENT_DIR.parent / "resource" / "ui"
    ui_widget_path = CURRENT_DIR.parent / "plugins" / "ui_widget"
    for f in ui_path.rglob("*.ui"):
        if f.is_file() and f.name.endswith(".ui"):
            print(f"编译UI文件：{f}")
            ui_build_path = ui_widget_path / f"{f.parent.name}" / f"ui_{f.stem}.py"
            ui_build_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "pyside6-uic",
                str(f),
                "-o",
                str(ui_build_path),
            ], check=True)
            # 处理init文件
            init_path = ui_build_path.parent / "__init__.py"
            open(init_path, "a").write(f"from .{ui_build_path.name.split('.')[0]} import Ui_{to_pascal_case(f.stem)}\n")
    print("编译完成")

if __name__ == "__main__":
    main()