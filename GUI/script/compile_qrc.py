
from pathlib import Path
import subprocess
import shutil


CURRENT_DIR = Path(__file__).parent

def main():
    """
    编译资源文件
    """
    img_base_path = CURRENT_DIR.parent / "resource" / "img"
    qss_base_path = CURRENT_DIR.parent / "resource" / "qss"
    plugin_base_path = CURRENT_DIR.parent / "plugins"
    qrc_img_path = img_base_path / "images.qrc"
    qrc_qss_path = qss_base_path / "qss.qrc"
    # 遍历img_base_path下的直接子文件夹
    for f in img_base_path.iterdir():
        if f.is_dir():
            print(f"查找到文件夹：{f.name}")
            # 删除插件对应的目录下的build文件夹，然后重建build文件夹
            if not Path(plugin_base_path / f.name).exists():
                continue
            build_path = plugin_base_path / f.name / "build"
            if build_path.exists():
                print(f"删除文件夹：{build_path}")
                # 递归删除文件夹下的所有文件
                shutil.rmtree(build_path)
            print(f"创建文件夹：{build_path}")
            build_path.mkdir()
            # 创建build/__init__.py文件
            init_path = build_path / "__init__.py"
            init_path.touch()
            # 将qrc转为对应的py文件
            cmd = f"pyside6-rcc {qrc_img_path} -o {build_path / 'rc_icon.py'}"
            print(f"执行命令：{cmd}")
            subprocess.run(cmd, shell=True)
            # 将qss.qrc转为对应的py文件
            cmd = f"pyside6-rcc {qrc_qss_path} -o {build_path / 'rc_qss.py'}"
            print(f"执行命令：{cmd}")
            subprocess.run(cmd, shell=True)
    
    print("编译完成")
    
if __name__ == "__main__":
    main()