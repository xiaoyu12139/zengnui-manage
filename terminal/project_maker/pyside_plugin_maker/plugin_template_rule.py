# 内部包
from public import *
from .config import *
# 外部包
import copy,re
from pathlib import Path

def rule_match(line: str, rule: str, context: dict):
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

def file_rule_match(file_path: Path, rule_seq: list, placeholder_table: dict, context: dict):
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
        if rule_match(line, tmp_rule[0], context):
            placeholder_table[tmp_rule[0]] = index
            tmp_rule.pop(0)
    if tmp_rule:
        ERROR(f"文件{file_path}匹配导入规则失败")
        return False
    return True

def check_plugin_rule(plugin_dir: Path, plugin_name: str, file_placeholder_table: dict, context: dict):
    """
    扫描plugin目录中的所有py文件中代码插入部分是否符合定义规范
    """
    rule_seq = copy.copy(placeholder_import_seq)
    plugin_path = plugin_dir / f"{plugin_name}_plugin"
    for f in plugin_path.glob("**/*.py"):
        if f.is_file():
            placeholder_table = {}
            if not file_rule_match(f, rule_seq, placeholder_table, context):
                return False
            # 如果为plugin文件扫描init，initalize, assemble规则
            if f.name == f"{plugin_name}_plugin.py":
                rule_init = copy.copy(placeholder_plugin_init_seq)
                rule_initialize = copy.copy(placeholder_plugin_initialize_seq)
                rule_assembled = copy.copy(placeholder_plugin_assembled_seq)
                if not file_rule_match(f, rule_init, placeholder_table, context) or not file_rule_match(f, rule_initialize, placeholder_table, context) or not file_rule_match(f, rule_assembled, placeholder_table, context):
                    return False
            if f.name == f"{plugin_name}_vm_build.py":
                rule_vmbuild_method = copy.copy(placeholder_vmbuild_method_seq)
                if not file_rule_match(f, rule_vmbuild_method, placeholder_table, context):
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
        
def del_line_in_range(lines: list, start_index: int, end_index: int, placeholder_table: dict):
    """
    删除指定索引行范围
    """
    for index in range(end_index, start_index - 1, -1):
        lines.pop(index)
        # 更新索引序号
        for key, value in placeholder_table.items():
            if value > index:
                placeholder_table[key] -= 1

def get_line_num(lines: list, regex: str):
    """
    获取匹配正则表达式的行号
    """
    for index, line in enumerate(lines):
        if re.match(regex, line):
            return index
    return 0

def del_line_in_rule(lines: list, regex: str,  rule_name: str, placeholder_table: dict):
    """
    删除指定索引行
    """
    start_index = placeholder_table.get(f"{rule_name}_start", None)
    if start_index is None:
        ERROR(f"规则{rule_name}未定义")
        return
    end_index = placeholder_table.get(f"{rule_name}_end", None)
    if end_index is None:
        ERROR(f"规则{rule_name}未定义")
        return
    #查找对应行
    for index, line in enumerate(lines[start_index:end_index+1]):
        if re.match(regex, line):
            # 删除行
            lines.pop(index + start_index)
            # 更新索引序号
            for key, value in placeholder_table.items():
                if value > index + start_index:
                    placeholder_table[key] -= 1
            break
    
    