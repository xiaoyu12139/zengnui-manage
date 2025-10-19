#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path
from typing import Tuple, Optional


def _cmd_module_dir(module_name: str) -> Path:
    """返回 CMD 宏模块的存放目录。"""
    return Path.home() / "Documents" / "CMDMacros" / module_name


def create_cmd_macros(module_name: str, directories: dict, aliases: dict) -> Tuple[bool, Optional[Path], Optional[str]]:
    """
    为 Windows CMD 创建切换目录的 DOSKEY 宏及加载脚本。

    Args:
        module_name: 模块名称，例如 "DirectorySwitch"
        directories: 目录配置 {'key': {'path': 'D:/path', 'desc': '描述'}}
        aliases: 别名映射 {'key': 'alias', 'help': 'ds-help'}

    Returns:
        tuple: (success: bool, module_dir: Path | None, error_msg: str | None)
    """
    try:
        module_dir = _cmd_module_dir(module_name)
        module_dir.mkdir(parents=True, exist_ok=True)

        macros_file = module_dir / f"{module_name}.macros"
        load_script = module_dir / "load.cmd"

        help_alias = aliases.get('help', 'ds-help')

        # 生成宏文件内容（使用纯 ASCII/UTF-8，避免编码问题）
        macro_lines = []
        help_lines = []
        for key, cfg in directories.items():
            alias = aliases.get(key, key)
            raw_path = str(cfg.get('path', '')).strip()
            # 将路径标准化为 Windows 反斜杠，避免 CMD 中出现 “语法不正确” 错误
            path = raw_path.replace('/', '\\')
            desc = cfg.get('desc', key)
            # 宏：切换目录并输出提示；使用 $T 作为命令分隔符，避免 & 转义带来的解析问题
            macro_lines.append(f"{alias}=cd /d \"{path}\" $T echo Switched to {alias}: {path}")
            help_lines.append(f"echo  {alias} - Switch to {alias}")

        # 帮助宏：输出可用命令
        help_macro = f"{help_alias}=echo {module_name} commands:"
        for hl in help_lines:
            help_macro += f" $T {hl}"
        help_macro += f" $T echo  {help_alias} - Show this help"
        macro_lines.append(help_macro)

        # 写入宏文件（UTF-8），配合加载时切换到 UTF-8 代码页，保证中文不乱码
        macros_file.write_text("\n".join(macro_lines), encoding="utf-8")

        # 生成加载脚本：在当前 CMD 会话中加载宏（先切换代码页到 UTF-8）
        macro_path = str(macros_file)
        load_script_content = f"""@echo off
chcp 65001 >nul
REM Load {module_name} macros
if exist "{macro_path}" (
    doskey /macrofile="{macro_path}"
    echo {module_name} macros loaded. Type '{help_alias}' to see help.
) else (
    echo Macro file not found: {macro_path}
)
"""
        load_script.write_text(load_script_content, encoding="utf-8")

        return True, module_dir, None
    except Exception as e:
        return False, None, str(e)


def test_cmd_macros(module_name: str, test_alias: str):
    """测试 CMD 宏是否能在同一 CMD 会话中工作。

    注意：DOSKEY 宏是进程级的，需在同一 cmd 进程中加载后测试。
    我们通过 cmd /c "call load.cmd & <alias>" 在同一进程内执行。
    """
    try:
        module_dir = _cmd_module_dir(module_name)
        load_script = module_dir / "load.cmd"
        if not load_script.exists():
            return False, f"Load script not found: {load_script}"

        cmdline = f"cmd.exe /c \"call \"{str(load_script)}\" ^& {test_alias}\""
        result = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
        return result.returncode == 0, output.strip()
    except Exception as e:
        return False, str(e)


def enable_cmd_autoload_macros(module_name: str):
    """为当前用户启用在每次启动 CMD 时自动加载宏（设置 AutoRun）。

    使用 REG_EXPAND_SZ 并引用 %USERPROFILE% 以保证用户路径的可移植性。
    如果已有 AutoRun，则在末尾追加 doskey /macrofile 指令；若已包含则不重复追加。
    返回 (success: bool, message: str)
    """
    try:
        # 目标宏文件的环境变量路径（随用户变化）
        macro_rel_path = f"%USERPROFILE%\\Documents\\CMDMacros\\{module_name}\\{module_name}.macros"
        # 在自动加载时，先切换到 UTF-8 代码页，再加载 UTF-8 宏文件
        macro_cmd = f"chcp 65001 >nul & doskey /macrofile=\"{macro_rel_path}\""

        # 查询现有 AutoRun
        query = subprocess.run([
            "REG", "QUERY", '"HKCU\\Software\\Microsoft\\Command Processor"',
            "/v", "AutoRun"
        ], capture_output=True, text=True)

        current_value = None
        if query.returncode == 0:
            # 输出格式通常包含一行：AutoRun    REG_EXPAND_SZ    <value>
            for line in (query.stdout or "").splitlines():
                if "AutoRun" in line and "REG_" in line:
                    parts = [p for p in line.strip().split("    ") if p]
                    if len(parts) >= 3:
                        current_value = parts[-1]
                        break
        
        # 组装新的 AutoRun 值
        if current_value:
            if macro_cmd in current_value:
                return True, "AutoRun 已包含宏加载指令，无需修改"
            new_value = f"{current_value} & {macro_cmd}"
        else:
            new_value = macro_cmd

        add = subprocess.run([
            "REG", "ADD", '"HKCU\\Software\\Microsoft\\Command Processor"',
            "/v", "AutoRun", 
            "/t", "REG_EXPAND_SZ", 
            "/d", new_value, 
            "/f"
        ], capture_output=True, text=True)

        if add.returncode != 0:
            return False, (add.stderr or add.stdout or "设置 AutoRun 失败")

        return True, "已设置 CMD 自动加载宏 (AutoRun)"
    except Exception as e:
        return False, str(e)