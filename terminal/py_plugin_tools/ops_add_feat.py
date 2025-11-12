# 内部包
from public import *
from .config import *
# 外部包
from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader, Template
import copy
import re

BASE_DIR = Path(__file__).parent
version_path = BASE_DIR / "template" / "V1"

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

def rule_match(line: str, rule: str):
    """
    规则匹配
    """
    rule_value = context.get(rule, None)
    if rule_value is None:
        ERROR(f"规则{rule}未定义")
        return False
    pattern = rf"^\s*{rule_value}\s*$"
    match = re.match(pattern, line)
    if not match:
        return False
    return True

def file_rule_match(file_path: Path, rule_seq: list, placeholder_table: dict):
    """
    文件规则匹配
    """
    # 规则扫描，从行首扫描到行尾，每次匹配rule_seq中的第1个元素
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    tmp_rule = copy.copy(rule_seq)
    for index,line in enumerate(lines):
        if not tmp_rule:
            break
        if rule_match(line, tmp_rule[0]):
            placeholder_table[tmp_rule[0]] = index
            tmp_rule.pop(0)
    if tmp_rule:
        ERROR(f"文件{file_path}匹配导入规则失败")
        return False
    return True

def check_plugin_add_feat(plugin_dir: Path, plugin_name: str, feat_name: str, file_placeholder_table: dict):
    """
    检查插件是否可以添加特性
    """
    #1.检查文件是否存在
    check_file_list = []
    view_file_path = plugin_dir / f"{plugin_name}_plugin" / "views" / f"{feat_name}_view.py"
    viewmodel_file_path = plugin_dir / f"{plugin_name}_plugin" / "viewmodels" / f"{feat_name}_viewmodel.py"
    constructor_file_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{feat_name}" / f"{feat_name}_cmd_handler.py"
    check_file_list.append(view_file_path)
    check_file_list.append(viewmodel_file_path)
    check_file_list.append(constructor_file_path)
    for f in check_file_list:
        if f.exists():
            ERROR(f"插件{plugin_name}已存在{feat_name}\n检查至文件{f}时终止")
            return False
    #2.扫描plugin目录中的所有py文件中代码插入部分是否符合定义规范，是否存在与feat_name冲突的部分
    rule_seq = copy.copy(placeholder_import_seq)
    plugin_path = plugin_dir / f"{plugin_name}_plugin"
    for f in plugin_path.glob("**/*.py"):
        if f.is_file():
            placeholder_table = {}
            if not file_rule_match(f, rule_seq, placeholder_table):
                return False
            # 如果为plugin文件扫描init，initalize, assemble规则
            if f.name == f"{plugin_name}_plugin.py":
                rule_init = copy.copy(placeholder_plugin_init_seq)
                rule_initialize = copy.copy(placeholder_plugin_initialize_seq)
                rule_assembled = copy.copy(placeholder_plugin_assembled_seq)
                if not file_rule_match(f, rule_init, placeholder_table) or not file_rule_match(f, rule_initialize, placeholder_table) or not file_rule_match(f, rule_assembled, placeholder_table):
                    return False
            file_placeholder_table[f] = placeholder_table
    return True

def insert_before(lines: list, target_index:int,  placeholder_table: dict, statement: str):
    """
    在指定索引前插入语句
    """
    lines.insert(target_index, statement)
    # 更新索引序号
    for key, value in placeholder_table.items():
        if value >= target_index:
            placeholder_table[key] += 1

def insert_after(lines: list, target_index:int,  placeholder_table: dict, statement: str):
    """
    在指定索引后插入语句
    """
    lines.insert(target_index + 1, statement)
    # 更新索引序号
    for key, value in placeholder_table.items():
        if value > target_index:
            placeholder_table[key] += 1

def add_plugin_feat(plugin_dir: Path, plugin_name: str, feat_name: str):
    """
    添加插件特性
    """
    if not check_plugin_feat(plugin_dir, plugin_name, feat_name):
        return
    context = config_add_feat(plugin_name, feat_name)
    INFO(f"基于context: {context}添加plugin feat")
    # 渲染模板添加plugin feat
    # 0.扫描plugin确认是否存在与feat冲突的部分
    file_placeholder_table = {} # 占位符表，记录每个文件中占位符对应的行号
    if not check_plugin_add_feat(plugin_dir, plugin_name, feat_name, file_placeholder_table):
        return
    SUCCESS(f"插件{plugin_name}关于{feat_name}的扫描通过，可进行添加")
    # 1.渲染创建feat对应的功能文件
    env = Environment(loader=FileSystemLoader(version_path / "{{ plugin_name }}_plugin"))
    ## 渲染view文件
    view_file_path = plugin_dir / f"{plugin_name}_plugin" / "views" / f"{feat_name}_view.py"
    view_file_content = env.get_template("views/{{ feat_name }}_view.py").render(context)
    view_file_path.write_text(view_file_content, encoding="utf-8")
    ## 渲染viewmodel文件
    viewmodel_file_path = plugin_dir / f"{plugin_name}_plugin" / "viewmodels" / f"{feat_name}_viewmodel.py"
    viewmodel_file_content = env.get_template("viewmodels/{{ feat_name }}_view_model.py").render(context)
    viewmodel_file_path.write_text(viewmodel_file_content, encoding="utf-8")
    ## 渲染constructor文件
    constructor_dir_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{feat_name}"
    constructor_dir_path.mkdir(parents=True, exist_ok=True)
    constructor_file_path = constructor_dir_path / f"{feat_name}_cmd_handler.py"
    constructor_file_content = env.get_template("constructors/{{ feat_name }}/{{ feat_name }}_cmd_handler.py").render(context)
    constructor_file_path.write_text(constructor_file_content, encoding="utf-8")
    SUCCESS(f"渲染创建feat对应的功能文件成功")

    #2.更新plugin文件
    plugin_file_path = plugin_dir / f"{plugin_name}_plugin" / f"{plugin_name}_plugin.py"
    placeholder_table = file_placeholder_table[plugin_file_path]
    lines = plugin_file_path.read_text(encoding="utf-8").splitlines()
    ## 插入import语句
    ### 插入import view
    import_statement = f"from .views.{feat_name}_view import {context['FeatName']}View\n"
    import_index = placeholder_table[placeholder_view_end]
    insert_before(lines, import_index, placeholder_table, import_statement)
    ### 插入import viewmodel
    import_statement = f"from .viewmodels.{feat_name}_view_model import {context['FeatName']}ViewModel\n"
    import_index = placeholder_table[placeholder_viewmodel_end]
    insert_before(lines, import_index, placeholder_table, import_statement)
    ### 插入import constructor
    import_statement = f"from .constructors.{feat_name} import {context['FeatName']}CmdHandler\n"
    import_index = placeholder_table[placeholder_constructor_end]
    insert_before(lines, import_index, placeholder_table, import_statement)
    SUCCESS(f"文件: {plugin_file_path} 插入import语句成功")
    ## 插入init语句
    init_statement = f"        self.{feat_name}_cmd_handler = {context['FeatName']}CmdHandler()\n"
    init_index = placeholder_table[placeholder_plugin_init_end]
    insert_before(lines, init_index, placeholder_table, init_statement)
    SUCCESS(f"文件: {plugin_file_path} 插入init语句成功")
    ## 插入 initialize 语句
    initialize_statement = f"        Global().views_manager.register_view(str(hash({context['FeatName']}View)), {context['FeatName']}View)\n"
    initialize_index = placeholder_table[placeholder_plugin_initialize_end]
    insert_before(lines, initialize_index, placeholder_table, initialize_statement)
    SUCCESS(f"文件: {plugin_file_path} 插入initialize语句成功")
    ## 插入 assembled 语句
    assembled_statement = f"        self.{feat_name}_cmd_handler.assemble_cmd(self.create_{feat_name}_vm_instance(context))\n"
    assembled_index = placeholder_table[placeholder_plugin_assembled_end]
    insert_before(lines, assembled_index, placeholder_table, assembled_statement)
    SUCCESS(f"文件: {plugin_file_path} 插入assembled语句成功")

    #3.更新vm_build文件
    vm_build_file_path = plugin_dir / f"{plugin_name}_plugin" / "constructors" / f"{plugin_name}_vm_build.py"
    placeholder_table = file_placeholder_table[vm_build_file_path]
    lines = vm_build_file_path.read_text(encoding="utf-8").splitlines()
    ## 插入import语句
    ### 插入import viewmodel
    import_statement = f"from .viewmodels.{feat_name}_view_model import {context['FeatName']}ViewModel\n"
    import_index = placeholder_table[placeholder_viewmodel_end]
    insert_before(lines, import_index, placeholder_table, import_statement)
    SUCCESS(f"文件: {vm_build_file_path} 插入import语句成功")
    ## 插入create vm instance语句
    create_vm_instance_statements = f'''
    def create_{feat_name}_vm_instance(self, context) -> Callable[[], {context['FeatName']}ViewModel]:
        """
        创建{context['FeatName']}视图模型实例
        """
        {feat_name}_vm = None
        def _create_{feat_name}_vm() -> {context['FeatName']}ViewModel:
            nonlocal {feat_name}_vm
            if {feat_name}_vm is None:
                {feat_name}_vm = {context['FeatName']}ViewModel(context)
            return {feat_name}_vm
        return _create_{feat_name}_vm
    '''
    for create_vm_instance_statement in create_vm_instance_statements.splitlines():
        create_vm_instance_index = placeholder_table[placeholder_vmbuild_method_end]
        insert_before(lines, create_vm_instance_index, placeholder_table, create_vm_instance_statement)
    SUCCESS(f"文件: {vm_build_file_path} 插入create vm instance语句成功")




