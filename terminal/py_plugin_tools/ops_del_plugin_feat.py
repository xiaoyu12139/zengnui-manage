# 内部包
from public import *
from .config import *
from .plugin_template_rule import *
# 外部包
from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader, Template
import copy
import re

def check_plugin_feat(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    检查插件
    """
    plugin_path = plugin_dir / f"{plugin_name}_plugin"
    if not plugin_path.exists():
        ERROR(f"插件{plugin_name}不存在")
        return False
    # 判断plugin_name与feat_name是否是蛇形小写
    snake_pattern = re.compile(r'^[a-z1-9]+(_[a-z1-9]+)*$')
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

def check_plugin_del_feat(plugin_dir: Path, plugin_name: str, feat_name: str, file_placeholder_table: dict, context: dict):
    """
    检查插件是否可以删除特性
    """
    #1.检查文件是否存在
    check_file_list = []
    view_file_path = plugin_dir / f"{plugin_name}_plugin" / "views" / f"{feat_name}_view.py"
    viewmodel_file_path = plugin_dir / f"{plugin_name}_plugin" / "viewmodels" / f"{feat_name}_viewmodel.py"
    constructor_file_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{feat_name}" / f"{feat_name}_cmd_handler.py"
    check_file_list.append(view_file_path)
    check_file_list.append(viewmodel_file_path)
    check_file_list.append(constructor_file_path)
    # for f in check_file_list:
    #     if not f.exists():
    #         ERROR(f"插件{plugin_name}不存在{feat_name}\n检查至文件{f}时终止")
    #         return False
    return check_plugin_rule(plugin_dir, plugin_name, file_placeholder_table, context)

def update_plugin_file(plugin_dir: Path, plugin_name: str, feat_name: str, context: dict, file_placeholder_table: dict):
    """
    更新插件文件
    """
    plugin_file_path = plugin_dir / f"{plugin_name}_plugin" / f"{plugin_name}_plugin.py"
    placeholder_table = file_placeholder_table[plugin_file_path]
    lines = plugin_file_path.read_text(encoding="utf-8").splitlines()
    ## 删除import语句
    import_statement = rf"^\s*from\s*.views.{feat_name}_view\s*import\s*{context['FeatName']}View\s*$"
    del_line_in_rule(lines, import_statement, "placeholder_import", placeholder_table)
    import_statement = rf"^\s*from\s*.constructors.{feat_name}\s*import\s*{context['FeatName']}CmdHandler\s*$"
    del_line_in_rule(lines, import_statement, "placeholder_constructor", placeholder_table)
    # 删除函数语句
    init_statement = rf"^\s*self.{feat_name}_cmd_handler\s*=\s*{context['FeatName']}CmdHandler\s*\(\s*\)\s*$"
    del_line_in_rule(lines, init_statement, "placeholder_plugin_init", placeholder_table)
    initialize_statement = rf"^\s*Global\(\).views_manager.register_view\s*\(\s*str\s*\(\s*hash\s*\(\s*{context['FeatName']}View\s*\)\s*\)\s*,\s*{context['FeatName']}View\s*\)\s*$"
    del_line_in_rule(lines, initialize_statement, "placeholder_plugin_initialize", placeholder_table)
    assembled_statement = rf"^\s*self.{feat_name}_cmd_handler.assemble_cmd\s*\(\s*self.create_{feat_name}_vm_instance\s*\(\s*context\s*\)\s*\)\s*$"
    del_line_in_rule(lines, assembled_statement, "placeholder_plugin_assembled", placeholder_table)
    ## 保存lines
    plugin_file_content = "\n".join(lines)
    plugin_file_path.write_text(plugin_file_content, encoding="utf-8")
    SUCCESS(f"文件: {plugin_file_path} 插入assembled语句成功")

def update_vmbuild_file(plugin_dir: Path, plugin_name: str, feat_name: str, context: dict, file_placeholder_table: dict):
    """
    更新vm_build文件
    """
    vm_build_file_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{plugin_name}_vm_build.py"
    placeholder_table = file_placeholder_table[vm_build_file_path]
    lines = vm_build_file_path.read_text(encoding="utf-8").splitlines()
    import_statement = rf"^\s*from\s*\.\.viewmodels.{feat_name}_viewmodel\s*import\s*{context['FeatName']}ViewModel\s*$"
    del_line_in_rule(lines, import_statement, "placeholder_import", placeholder_table)
    first_line = rf"^\s*def\s*create_{feat_name}_vm_instance\s*\(\s*self\s*,\s*context\s*\s*\)\s*->\s*Callable\[\[\],\s*{context['FeatName']}ViewModel\s*\]\s*:\s*$"
    last_line = rf"^\s*return\s*_create_{feat_name}_vm\s*$"
    first_line_index = get_line_num(lines, first_line)
    last_line_index = get_line_num(lines, last_line)
    del_line_in_range(lines, first_line_index, last_line_index, placeholder_table)
    # 去除函数上方的空行，如果存在
    if lines[first_line_index - 1].strip() == "":
        del lines[first_line_index - 1]
    ## 保存lines
    vm_build_file_content = "\n".join(lines)
    vm_build_file_path.write_text(vm_build_file_content, encoding="utf-8")
    SUCCESS(f"文件: {vm_build_file_path} 插入create vm instance语句成功")

def del_plugin_feat(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    删除plugin feat
    """
    if not check_plugin_feat(plugin_dir, plugin_name, feat_name):
        return
    context = config_del_feat(plugin_name, feat_name)
    INFO(f"基于context: {context}删除plugin feat")
    file_placeholder_table = {} # 占位符表，记录每个文件中占位符对应的行号
    if not check_plugin_del_feat(plugin_dir, plugin_name, feat_name, file_placeholder_table, context):
        return
    SUCCESS(f"插件{plugin_name}扫描通过，可进行删除操作")
    #1.删除feat文件
    view_file_path = plugin_dir / f"{plugin_name}_plugin" / "views" / f"{feat_name}_view.py"
    viewmodel_file_path = plugin_dir / f"{plugin_name}_plugin" / "viewmodels" / f"{feat_name}_viewmodel.py"
    constructor_dir_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{feat_name}"
    constructor_file_path = constructor_dir_path / f"{feat_name}_cmd_handler.py"
    # view_file_path.unlink()
    # viewmodel_file_path.unlink()
    # constructor_file_path.unlink()
    # constructor_dir_path.rmdir()
    SUCCESS(f"{plugin_name} {feat_name}对应文件删除成功")
    #2.删除plugin文件中feat相关代码
    update_plugin_file(plugin_dir, plugin_name, feat_name, context, file_placeholder_table)
    #2.删除vm_build文件中feat相关代码
    update_vmbuild_file(plugin_dir, plugin_name, feat_name, context, file_placeholder_table)

    SUCCESS(f"plugin:{plugin_name} feat_name:{feat_name} 删除成功")

