from pathlib import Path
import subprocess

CURRENT_DIR = Path(__file__).parent

def build_all_ui():
    ui_path = CURRENT_DIR.parent / "resource" / "ui"
    print(f"ui资源文件夹：{ui_path}\n")
    for f in ui_path.glob("*.ui"):
        print(f"编译UI文件：{f}")
        # 编译UI文件
        cmd = f"pyside6-uic {f} -o {CURRENT_DIR.parent / 'plugins' / 'ui_widget' / (f.stem + '.py')}"
        print(f"执行命令：{cmd}")
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    # 编译所有UI文件
    print("编译所有UI文件...")
    build_all_ui()