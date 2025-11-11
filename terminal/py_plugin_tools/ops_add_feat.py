# 内部包
from ntpath import isdir
from public import *
# 外部包
from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader, Template

BASE_DIR = Path(__file__).parent
version_path = BASE_DIR / "template" / "V1"

def check_plugin(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    检查插件
    """
    plugin_path = plugin_dir / f"{plugin_name}.py"
    if not plugin_path.exists():
        ERROR(f"插件{plugin_name}不存在")
        return False
    # 判断plugin_name与feat_name是否是蛇形小写
    snake_pattern = re.compile(r'^[a-z]+(_[a-z]+)*$')
    if not snake_pattern.match(plugin_name):
        ERROR(f"插件名 {plugin_name} 不是蛇形小写")
        return False
    if not snake_pattern.match(feat_name):
        ERROR(f"特性名 {feat_name} 不是蛇形小写")
        return False
    if not feat_name:
        ERROR(f"特性名 {feat_name} 不能为空")
        return False
    return True

def create_plugin(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    创建插件
    """
    # 检查插件目录是否存在
    if not isdir(plugin_dir):
        raise Exception(f"插件目录{plugin_dir}不存在")
    # 检查插件名称是否符合要求
    if not re.match(r"^[a-z_]+$", plugin_name):
        raise Exception(f"插件名称{plugin_name}不符合要求")
    # 检查组件名称是否符合要求
    if not re.match(r"^[a-z_]+$", feat_name):
        raise Exception(f"组件名称{feat_name}不符合要求")
    # 渲染模板
    env = Environment(loader=FileSystemLoader(version_path))
    template = env.get_template("plugin.py.j2")
    output = template.render(config_add_feat(plugin_name, feat_name))
    # 写入文件
    plugin_path = plugin_dir / f"{plugin_name}.py"
    with open(plugin_path, "w") as f:
        f.write(output)