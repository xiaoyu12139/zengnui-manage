# 根据参数来创建Plugin或者给plugin添加view
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_DIR = Path(__file__).resolve().parent.parent
PLUGIN_BASE_DIR = BASE_DIR / 'plugins'

# 模板目录改为绝对路径，提升健壮性；启用严格未定义与空白控制
TPL_DIR = Path(__file__).resolve().parent / 'template' / 'plugin_template'
env = Environment(
    loader=FileSystemLoader(str(TPL_DIR)),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)

def plugin_create(plugin_name: str, plugin_view: str):
    """
    创建plugin
    :param plugin_name: plugin的名称
    :param plugin_view: plugin的view名称
    :return:
    """
    print(f"创建插件 {plugin_name} 视图 {plugin_view}")
    # 创建插件目录
    plugin_dir = PLUGIN_BASE_DIR / f"{plugin_name}_plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    plugin_views_dir = plugin_dir / 'views'
    plugin_views_dir.mkdir(parents=True, exist_ok=True)
    plugin_viewmodels_dir = plugin_dir / 'viewmodels'
    plugin_viewmodels_dir.mkdir(parents=True, exist_ok=True)
    plugin_constructors_dir = plugin_dir / 'constructors'
    plugin_constructors_dir.mkdir(parents=True, exist_ok=True)
    plugin_view_constructor_dir = plugin_constructors_dir / plugin_view
    plugin_view_constructor_dir.mkdir(parents=True, exist_ok=True)

    # 创建ctx
    ctx = {
        "plugin_name": plugin_name,
        "PluginName": plugin_name.title(),
        "plugin_view": plugin_view,
        "PluginView": plugin_view.title(),
    }

    # 创建plugin文件
    plugin_file = plugin_dir / f"{plugin_name}_plugin.py"
    plugin_file.touch(exist_ok=True)
    tpl = env.get_template('plugin.txt')
    out = tpl.render(**ctx)
    plugin_file.write_text(out, encoding='utf-8')

    # 创建view文件
    plugin_view_file = plugin_views_dir / f"{plugin_view}_view.py"
    plugin_view_file.touch(exist_ok=True)
    plugin_view_init_file = plugin_views_dir / '__init__.py'
    plugin_view_init_file.touch(exist_ok=True)
    tpl = env.get_template('view.txt')
    out = tpl.render(**ctx)
    plugin_view_file.write_text(out, encoding='utf-8')
    # 写入init
    plugin_view_init_file.write_text(f"from .{plugin_view}_view import {plugin_view.title()}View", encoding='utf-8')

    # 创建viewmodel文件
    plugin_viewmodel_file = plugin_viewmodels_dir / f"{plugin_view}_view_model.py"
    plugin_viewmodel_file.touch(exist_ok=True)
    plugin_viewmodel_init_file = plugin_viewmodels_dir / '__init__.py'
    plugin_viewmodel_init_file.touch(exist_ok=True)
    tpl = env.get_template('viewmodel.txt')
    out = tpl.render(**ctx)
    plugin_viewmodel_file.write_text(out, encoding='utf-8')
    # 写入init
    plugin_viewmodel_init_file.write_text(f"from .{plugin_view}_view_model import {plugin_view.title()}ViewModel", encoding='utf-8')

    # 创建constructor文件
    plugin_constructor_file = plugin_constructors_dir / f"{plugin_view}_vm_build.py"
    plugin_constructor_file.touch(exist_ok=True)
    plugin_constructor_init_file = plugin_constructors_dir / '__init__.py'
    plugin_constructor_init_file.touch(exist_ok=True)
    tpl = env.get_template('vm_build.txt')
    out = tpl.render(**ctx)
    plugin_constructor_file.write_text(out, encoding='utf-8')
    # 写入init
    plugin_constructor_init_file.write_text(f"from .{plugin_view}_vm_build import {plugin_view.title()}ViewModelBuilder", encoding='utf-8')
    # 追加导入使用普通文件追加方式，Path 无 append_text 方法
    with open(plugin_constructor_init_file, 'a', encoding='utf-8') as f:
        # 统一从子包导出视图级 CmdHandler，类名按视图名
        f.write(f"\nfrom .{plugin_view} import {plugin_view.title()}CmdHandler")

    # 创建constructor view文件
    plugin_view_constructor_file = plugin_view_constructor_dir / f"{plugin_view}_cmd_handler.py"
    plugin_view_constructor_file.touch(exist_ok=True)
    plugin_view_constructor_init_file = plugin_view_constructor_dir / '__init__.py'
    plugin_view_constructor_init_file.touch(exist_ok=True)
    tpl = env.get_template('cmd_handler.txt')
    out = tpl.render(**ctx)
    plugin_view_constructor_file.write_text(out, encoding='utf-8')
    # 写入init
    plugin_view_constructor_init_file.write_text(f"from .{plugin_view}_cmd_handler import {plugin_view.title()}CmdHandler", encoding='utf-8')
    
def plugin_add(plugin_name: str, plugin_view: str):
    """
    给plugin添加view
    :param plugin_name: plugin的名称
    :param plugin_view: plugin的view名称
    :return:
    """
    print(f"给插件{plugin_name}添加视图{plugin_view}")
    # 基础目录检查
    plugin_dir = PLUGIN_BASE_DIR / f"{plugin_name}_plugin"
    if not plugin_dir.exists():
        print(f"插件 {plugin_name} 不存在，先执行 create 再 add")
        return

    # 需要创建的文件的path
    plugin_file = plugin_dir / f"{plugin_name}_plugin.py"
    plugin_views_dir = plugin_dir / 'views'
    plugin_viewmodels_dir = plugin_dir / 'viewmodels'
    plugin_constructors_dir = plugin_dir / 'constructors'
    plugin_view_constructor_dir = plugin_constructors_dir / plugin_view

    # 确保目录存在
    plugin_views_dir.mkdir(parents=True, exist_ok=True)
    plugin_viewmodels_dir.mkdir(parents=True, exist_ok=True)
    plugin_constructors_dir.mkdir(parents=True, exist_ok=True)
    plugin_view_constructor_dir.mkdir(parents=True, exist_ok=True)

    # 上下文 plugin_name为蛇形小写，PluginName为大驼峰
    ctx = {
        "plugin_name": plugin_name,
        "PluginName": ''.join(word.capitalize() for word in plugin_name.split('_')),
        "plugin_view": plugin_view,
        "PluginView": ''.join(word.capitalize() for word in plugin_view.split('_')),
    }

    # 视图文件与 __init__
    plugin_view_file = plugin_views_dir / f"{plugin_view}_view.py"
    tpl = env.get_template('view.txt')
    out = tpl.render(**ctx)
    if not plugin_view_file.exists():
        plugin_view_file.write_text(out, encoding='utf-8')
    plugin_view_init_file = plugin_views_dir / '__init__.py'
    plugin_view_init_file.touch(exist_ok=True)
    view_import_line = f"from .{plugin_view}_view import {plugin_view.title()}View"
    current = plugin_view_init_file.read_text(encoding='utf-8') if plugin_view_init_file.exists() else ""
    if view_import_line not in current:
        with open(plugin_view_init_file, 'a', encoding='utf-8') as f:
            f.write(("\n" if current else "") + view_import_line)

    # ViewModel 文件与 __init__
    plugin_viewmodel_file = plugin_viewmodels_dir / f"{plugin_view}_view_model.py"
    tpl = env.get_template('viewmodel.txt')
    out = tpl.render(**ctx)
    if not plugin_viewmodel_file.exists():
        plugin_viewmodel_file.write_text(out, encoding='utf-8')
    plugin_viewmodel_init_file = plugin_viewmodels_dir / '__init__.py'
    plugin_viewmodel_init_file.touch(exist_ok=True)
    vm_import_line = f"from .{plugin_view}_view_model import {plugin_view.title()}ViewModel"
    current = plugin_viewmodel_init_file.read_text(encoding='utf-8') if plugin_viewmodel_init_file.exists() else ""
    if vm_import_line not in current:
        with open(plugin_viewmodel_init_file, 'a', encoding='utf-8') as f:
            f.write(("\n" if current else "") + vm_import_line)

    # 构造器（VM Builder）：复用插件级 builder 文件，追加新 ViewModel 的工厂方法
    plugin_constructor_init_file = plugin_constructors_dir / '__init__.py'
    plugin_constructor_init_file.touch(exist_ok=True)
    builder_file = plugin_constructors_dir / f"{plugin_name}_vm_build.py"
    # 如果标准 builder 文件不存在，回退到视图名（兼容早期用法）
    if not builder_file.exists():
        fallback_builder = plugin_constructors_dir / f"{plugin_view}_vm_build.py"
        if fallback_builder.exists():
            builder_file = fallback_builder
        else:
            # 首次 add 时若未创建过，使用模板创建插件级 builder 文件
            tpl = env.get_template('vm_build.txt')
            out = tpl.render(**ctx)
            builder_file.write_text(out, encoding='utf-8')

    builder_code = builder_file.read_text(encoding='utf-8')
    # 补齐 import：将新 ViewModel 合并到 import 列表中
    vm_import_name = f"{plugin_view.title()}ViewModel"
    if f"from ..viewmodels import" in builder_code and vm_import_name not in builder_code:
        # 合并到首个 import 行
        import_lines = builder_code.splitlines()
        for i, line in enumerate(import_lines):
            if line.startswith("from ..viewmodels import"):
                if vm_import_name not in line:
                    if "," in line:
                        import_lines[i] = line + f", {vm_import_name}"
                    else:
                        import_lines[i] = line + f", {vm_import_name}"
                break
        builder_code = "\n".join(import_lines)
    elif f"from ..viewmodels import {vm_import_name}" not in builder_code:
        builder_code = f"from ..viewmodels import {vm_import_name}\n" + builder_code

    # 追加新的工厂方法 create_<view>_vm_instance，如果不存在的话
    new_method_signature = f"def create_{plugin_view}_vm_instance(self, context)"
    if new_method_signature not in builder_code:
        method_block = f"\n\n    def create_{plugin_view}_vm_instance(self, context) -> Callable[[], {plugin_view.title()}ViewModel]:\n        \"\"\n        创建{plugin_name.title()}视图模型实例\n        \"\"\n        {plugin_view}_vm = None\n        def _create_{plugin_view}_vm() -> {plugin_view.title()}ViewModel:\n            nonlocal {plugin_view}_vm\n            if {plugin_view}_vm is None:\n                {plugin_view}_vm = {plugin_view.title()}ViewModel(context)\n            return {plugin_view}_vm\n        return _create_{plugin_view}_vm\n"
        # 简单策略：追加到类定义末尾
        builder_code += method_block
        builder_file.write_text(builder_code, encoding='utf-8')
    else:
        # 已存在方法，仅在 import 更新时落盘
        builder_file.write_text(builder_code, encoding='utf-8')

    # constructors/__init__.py 保持仅导出一次插件级 builder 与新增视图的 CmdHandler
    builder_import_line = f"from .{builder_file.stem} import {plugin_name.title()}ViewModelBuilder"
    cmd_handler_pkg_import_line = f"from .{plugin_view} import {plugin_view.title()}CmdHandler"
    current = plugin_constructor_init_file.read_text(encoding='utf-8') if plugin_constructor_init_file.exists() else ""
    to_append = []
    if builder_import_line not in current:
        to_append.append(builder_import_line)
    if cmd_handler_pkg_import_line not in current:
        to_append.append(cmd_handler_pkg_import_line)
    if to_append:
        with open(plugin_constructor_init_file, 'a', encoding='utf-8') as f:
            f.write(("\n" if current else "") + "\n".join(to_append))

    # 规范化 constructors/__init__.py：
    # - 仅保留一次插件级 builder 导出（指向 builder_file.stem）
    # - 去重每个视图的 CmdHandler 导出
    init_lines = plugin_constructor_init_file.read_text(encoding='utf-8').splitlines()
    normalized = []
    seen = set()
    desired_builder_line = f"from .{builder_file.stem} import {plugin_name.title()}ViewModelBuilder"
    for line in init_lines:
        line = line.strip()
        if not line:
            continue
        # 统一 builder：只保留期望的这一行
        if line.startswith("from .") and "_vm_build import" in line:
            if desired_builder_line not in seen:
                normalized.append(desired_builder_line)
                seen.add(desired_builder_line)
            continue
        # CmdHandler 行去重（以 CmdHandler 结尾的导出均视为处理类）
        if line.startswith("from .") and line.endswith("CmdHandler"):
            # 移除旧格式：from .<view> import <PluginName>CmdHandler（仅保留 .<plugin_name> 的同名行）
            try:
                parts = line.split()
                # 形如：from .<view> import <Name>CmdHandler
                view_part = parts[1]
                imported_name = parts[-1]
                if view_part.startswith("."):
                    view_pkg = view_part[1:]
                else:
                    view_pkg = view_part
                if imported_name == f"{plugin_name.title()}CmdHandler" and view_pkg != plugin_name:
                    # 跳过旧的错误导出
                    continue
            except Exception:
                pass
            if line not in seen:
                normalized.append(line)
                seen.add(line)
            continue
        # 其它行按原样保留（并去重）
        if line not in seen:
            normalized.append(line)
            seen.add(line)
    plugin_constructor_init_file.write_text("\n".join(normalized) + ("\n" if normalized else ""), encoding='utf-8')

    # 子包 constructors/<view>/ 文件与 __init__
    plugin_view_constructor_file = plugin_view_constructor_dir / f"{plugin_view}_cmd_handler.py"
    tpl = env.get_template('cmd_handler.txt')
    out = tpl.render(**ctx)
    # 覆盖写入，确保模板更新后内容同步
    plugin_view_constructor_file.write_text(out, encoding='utf-8')
    plugin_view_constructor_init_file = plugin_view_constructor_dir / '__init__.py'
    plugin_view_constructor_init_file.touch(exist_ok=True)
    sub_init_line = f"from .{plugin_view}_cmd_handler import {plugin_view.title()}CmdHandler"
    # 只保留视图级导出，清理旧的插件级同名导出
    plugin_view_constructor_init_file.write_text(sub_init_line + "\n", encoding='utf-8')

    # 自动更新主插件文件：引入新视图、处理器，初始化注册与组装命令（幂等）
    if plugin_file.exists():
        code = plugin_file.read_text(encoding='utf-8')
        modified = False

        # 1) 导入视图与处理器
        view_import_line = f"from .views import {plugin_view.title()}View"
        handler_import_line = f"from .constructors import {plugin_view.title()}CmdHandler"
        pending_imports = []
        if view_import_line not in code:
            pending_imports.append(view_import_line)
        if handler_import_line not in code:
            pending_imports.append(handler_import_line)
        if pending_imports:
            anchor = "from utils import get_logger"
            idx = code.find(anchor)
            if idx != -1:
                code = code[:idx] + "\n" + "\n".join(pending_imports) + "\n" + code[idx:]
            else:
                code = "\n".join(pending_imports) + "\n" + code
            modified = True

        # 2) __init__ 中新增处理器实例
        init_attr_line = f"        self.{plugin_view}_cmd_handle = {plugin_view.title()}CmdHandler()"
        if init_attr_line not in code:
            init_sig = "def __init__(self):"
            init_idx = code.find(init_sig)
            if init_idx != -1:
                super_line = "        super().__init__()"
                super_idx = code.find(super_line, init_idx)
                insert_pos = super_idx + len(super_line) if super_idx != -1 else code.find("\n", init_idx) + 1
                code = code[:insert_pos] + "\n" + init_attr_line + code[insert_pos:]
                modified = True

        # 3) initialize 中注册新视图
        register_line = f"        Global().views_manager.register_view(str(hash({plugin_view.title()}View)), {plugin_view.title()}View)"
        if register_line not in code:
            init_sig = "def initialize(self):"
            init_idx = code.find(init_sig)
            if init_idx != -1:
                existing_reg_idx = code.find("Global().views_manager.register_view", init_idx)
                if existing_reg_idx != -1:
                    eol = code.find("\n", existing_reg_idx)
                    eol = eol if eol != -1 else existing_reg_idx
                    code = code[:eol+1] + register_line + "\n" + code[eol+1:]
                else:
                    def_eol = code.find("\n", init_idx)
                    code = code[:def_eol+1] + register_line + "\n" + code[def_eol+1:]
                modified = True

        # 4) assembled 中组装新视图命令
        assemble_line = f"        self.{plugin_view}_cmd_handle.assemble_cmd(self.create_{plugin_view}_vm_instance(context))"
        if assemble_line not in code:
            assembled_sig = "def assembled(self, context):"
            assembled_idx = code.find(assembled_sig)
            if assembled_idx != -1:
                existing_assem_idx = code.find(".assemble_cmd(", assembled_idx)
                if existing_assem_idx != -1:
                    eol = code.find("\n", existing_assem_idx)
                    eol = eol if eol != -1 else existing_assem_idx
                    code = code[:eol+1] + assemble_line + "\n" + code[eol+1:]
                else:
                    def_eol = code.find("\n", assembled_idx)
                    code = code[:def_eol+1] + assemble_line + "\n" + code[def_eol+1:]
                modified = True

        if modified:
            plugin_file.write_text(code, encoding='utf-8')
    


def plugin_del(plugin_name: str, plugin_view: str):
    """
    删除plugin的view
    :param plugin_name: plugin的名称
    :param plugin_view: plugin的view名称
    :return:
    """
    if plugin_view == 'all':
        print(f"删除插件{plugin_name}的所有视图")
    else:
        print(f"删除插件{plugin_name}的视图{plugin_view}")

def main(plugin_ops: str, plugin_name: str, plugin_view: str):
    """
    根据参数来创建Plugin或者给plugin添加view
    :param plugin_ops: 操作类型，create或者add,del
    :param plugin_name: plugin的名称
    :param plugin_view: plugin的view名称
    :return:
    """
    if plugin_ops == 'create':
        # 创建plugin
        plugin_create(plugin_name, plugin_view)
    elif plugin_ops == 'add':
        # 给plugin添加view
        plugin_add(plugin_name, plugin_view)
    elif plugin_ops == 'del':
        # 删除plugin的view
        plugin_del(plugin_name, plugin_view)

if __name__ == '__main__':
    # 获取输入参数
    import sys
    if len(sys.argv) < 4:
        print("用法: python GUI/script/plugin_tools.py <create|add|del> <plugin_name> <plugin_view|all>")
        sys.exit(1)
    plugin_ops = sys.argv[1]
    plugin_name = sys.argv[2]
    plugin_view = sys.argv[3]
    # 三个参数不能为空
    if not plugin_ops or not plugin_name or not plugin_view:
        print("参数不能为空")
        sys.exit(1)
    main(plugin_ops, plugin_name, plugin_view)
