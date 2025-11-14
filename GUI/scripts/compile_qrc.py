from pathlib import Path
import subprocess
import shutil
from typing import List

CURRENT_DIR = Path(__file__).parent


def get_plugins_path() -> List[Path]:
    """
    获取所有插件的路径
    """
    plugin_base_path = CURRENT_DIR.parent / "src" / "plugins"
    plugins_path = []
    for f in plugin_base_path.iterdir():
        if f.is_dir() and f.name.endswith("_plugin"):
            plugins_path.append(f)
    return plugins_path


def rm_build_dir(plugin_path: Path):
    """
    删除插件目录下的build文件夹
    """
    build_path = plugin_path / "build"
    if build_path.exists():
        print(f"删除文件夹：{build_path}")
        # 递归删除文件夹下的所有文件
        shutil.rmtree(build_path)


def reset_build_dir(plugin_path: Path):
    """
    初始化插件目录下的build文件夹
    """
    rm_build_dir(plugin_path)
    build_path = plugin_path / "build"
    build_path.mkdir()  # 创建build文件夹
    (build_path / "__init__.py").touch()  # 创建build/__init__.py文件


def main():
    """
    编译资源文件
    """
    plugins_path = get_plugins_path()
    # 重置build目录
    print("重置插件build目录")
    for plugin_path in plugins_path:
        reset_build_dir(plugin_path)
    # 编译资源文件
    print("编译资源文件")
    qrc_resource_path = (
        CURRENT_DIR.parent / "src" / "resources" / "resources.qrc"
    )
    for plugin_path in plugins_path:
        print(f"插件路径：{plugin_path}")
        # 编译resource.qrc文件
        cmd = f"pyside6-rcc {qrc_resource_path} -o {plugin_path / 'build' / 'rc_resource.py'}"
        subprocess.run(cmd, shell=True)
    print("编译完成")


if __name__ == "__main__":
    main()
