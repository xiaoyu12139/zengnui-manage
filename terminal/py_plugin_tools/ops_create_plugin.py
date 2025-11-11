# 内部包
from ntpath import isdir
from public import *
# 外部包
from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader, Template

BASE_DIR = Path(__file__).parent
version_path = BASE_DIR / "template" / "V1"

context = {
    "plugin_main_feat": True,
    "plugin_name": "",
    "PluginName": "",
    "feat_name": "",
    "FeatName": "",
    # 导包占位符
    "placeholder_import_start": "######import_start######",
    "placeholder_import_end": "######import_end######",
    "placeholder_constructor_start": "######constructor_start######",
    "placeholder_constructor_end": "######constructor_end######",
    "placeholder_ui_start": "######ui_start######",
    "placeholder_ui_end": "######ui_end######",
    "placeholder_view_start": "######view_start######",
    "placeholder_view_end": "######view_end######",
    "placeholder_viewmodel_start": "######viewmodel_start######",
    "placeholder_viewmodel_end": "######viewmodel_end######",
    # plugin文件占位符
    "placeholder_plugin_init_start": "######plugin_init_start######",
    "placeholder_plugin_init_end": "######plugin_init_end######",
    "placeholder_plugin_initialize_start": "######plugin_initialize_start######",
    "placeholder_plugin_initialize_end": "######plugin_initialize_end######",
    "placeholder_plugin_assembled_start": "######plugin_assembled_start######",
    "placeholder_plugin_assembled_end": "######plugin_assembled_end######",
}

def check_plugin(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    检查插件目录、插件名和特性名是否符合要求
    """
    if not plugin_dir.exists():
        ERROR(f"插件目录 {plugin_dir} 不存在")
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

def get_real_path(tmplate: Path, plugin_dir: Path) -> Path:
    """
    获取渲染目录的实际路径
    """
    # 获取相对实际目录位置
    plugin_prefix = str(tmplate).replace(str(version_path), "")
    real_path = Path(plugin_dir / plugin_prefix[1:])
    return real_path

def path_render(tmplate: Path, plugin_dir: Path) -> Path:
    """
    渲染目录路径

    Args:
        tmplate (Path): 模板目录路径
    Returns:
        Path: 渲染后的目录路径
    """
    real_path = get_real_path(tmplate, plugin_dir)
    real_template = Template(str(real_path))
    render_path = real_template.render(context)
    if tmplate.is_dir():
        # 创建渲染目录
        Path(render_path).mkdir(parents=True, exist_ok=True)
        INFO(f"创建目录 {render_path}")
    else:
         Path(render_path).touch(exist_ok=True)
         INFO(f"创建文件 {render_path}")
    return render_path

def file_render(tmplate: Path) -> str:
    """
    渲染文件路径

    Args:
        tmplate (Path): 模板文件路径
    Returns:
        str: 渲染后的文件内容
    """
    # 读取模板文件内容
    with open(tmplate, "r", encoding="utf-8") as f:
        template_content = f.read()
    # 渲染模板内容
    render_content = Template(template_content).render(context)
    return render_content

def create_plugin(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    创建插件
    """
    if not check_plugin(plugin_dir, plugin_name, feat_name):
        return
    PluginName = ''.join([word.capitalize() for word in plugin_name.split("_")])
    FeatName = ''.join([word.capitalize() for word in feat_name.split("_")])
    context["plugin_name"] = plugin_name
    context["PluginName"] = PluginName
    context["feat_name"] = feat_name
    context["FeatName"] = FeatName
    INFO(f"基于context: {context}创建插件")
    # 渲染插件模板目录 {{ plugin_name }}_plugin 到plugin_dir下
    plugin_template_dir = version_path / "{{ plugin_name }}_plugin"
    dir_queue = [plugin_template_dir]
    while dir_queue:
        cur_dir = dir_queue.pop(0)
        path_render(cur_dir, plugin_dir)
        for item in cur_dir.iterdir():
            if item.is_dir():
                dir_queue.append(item)
            else:
                file_path = path_render(item, plugin_dir)
                render_content = file_render(item)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(render_content)
    
