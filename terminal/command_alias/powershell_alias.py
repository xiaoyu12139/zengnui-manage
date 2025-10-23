import re
from pathlib import Path
from typing import Optional, Tuple
from .base_alias import BaseAliasManager
from public.logger import *

class PowerShellAliasManager(BaseAliasManager):
    def profile_path(self, prefer_ps7: Optional[bool] = None) -> Path:
        home = Path.home()
        ps5 = home / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
        ps7 = home / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
        if prefer_ps7 is None:
            try:
                t = (get_terminal_type() or "").lower()
            except Exception:
                t = ""
            if t == "pwsh":
                prefer_ps7 = True
            elif t == "powershell":
                prefer_ps7 = False
            else:
                prefer_ps7 = ps7.parent.exists()
        return ps7 if prefer_ps7 else ps5

    def set_function(self, alias_name: str, command: str) -> Tuple[bool, str]:
        alias = self.sanitize_alias_name(alias_name)
        if not alias:
            return False, "无效的函数名称"
        profile_path = self.profile_path()
        self.ensure_parent(profile_path)
        body = command.strip()
        indented = "\n".join("    " + line for line in body.splitlines())
        block = (
            f"# alias-manager : start {alias}\n"
            f"function {alias} {{\n"
            f"{indented}\n"
            f"}}\n"
            f"# alias-manager : end {alias}\n"
        )
        try:
            content = ""
            encoding = "utf-8"
            if profile_path.exists():
                content, encoding = self.read_text_with_encoding(profile_path)
                # 移除已有该函数的标记块
                marked_func = re.compile(
                    rf"\n*#\s*alias-manager\s*:\s*start.*?function\s+{re.escape(alias)}\s*\{{.*?}}.*?#\s*alias-manager\s*:\s*end.*\n*",
                    re.MULTILINE | re.DOTALL
                )
                content = marked_func.sub("", content)
                # 移除未标记的旧函数块
                func_pat = re.compile(rf"^\s*function\s+{re.escape(alias)}\s*\{{[\s\S]*?}}", re.MULTILINE)
                content = func_pat.sub("", content)
                # 清理多余空行
                content = re.sub(r"\n\s*\n+", "\n\n", content)
                # 追加新标记块
                content = content.rstrip("\n") + "\n" + block
                self.write_text_with_encoding(profile_path, content, encoding)
            else:
                self.write_text_with_encoding(profile_path, block, encoding)
        except Exception as e:
            return False, f"写入 PowerShell 配置失败: {e}"
        return True, f"PowerShell 函数已持久化：{alias} -> {command}\n重新加载：. $PROFILE"

    def reset(self, aggressive: bool = False) -> Tuple[bool, str]:
        """重置 PowerShell 别名配置
        
        Args:
            aggressive: 如果为 True，则额外删除未标记的 Set-Alias 目标函数块，并过滤仅数字行
        """
        try:
            # 清理 PS5 和 PS7 配置文件
            home = Path.home()
            profiles = [
                home / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1",
                home / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
            ]
            
            cleaned_profiles = []
            
            for profile_path in profiles:
                if not profile_path.exists():
                    continue
                    
                # 使用编码检测读取文件
                content, encoding = self.read_text_with_encoding(profile_path)
                if not content.strip():
                    continue
                
                # 1) 先移除标记块
                marked_pattern = re.compile(r"#\s*alias-manager\s*:\s*start(?:\s+\S+)?[\s\S]*?#\s*alias-manager\s*:\s*end(?:\s+\S+)?", re.MULTILINE)
                content = marked_pattern.sub("", content)
                
                if aggressive:
                    # 2) 收集 Set-Alias 命令中的别名名称和目标名称
                    alias_names = set()
                    target_names = set()
                    func_names = set()
                    
                    # 从标记块中提取名称（在删除前）
                    original_content, _ = self.read_text_with_encoding(profile_path)
                    for match in marked_pattern.finditer(original_content):
                        block = match.group(0)
                        # 提取 Set-Alias 和 function 名称
                        for alias_match in re.finditer(r'Set-Alias\s+(\S+)\s+(\S+)', block):
                            alias_names.add(alias_match.group(1))
                            target_names.add(alias_match.group(2))
                        for func_match in re.finditer(r'function\s+(\S+)\s*\{', block):
                            func_names.add(func_match.group(1))
                    
                    # 额外：从整个文件中解析未标记的 Set-Alias
                    for alias_match in re.finditer(r'^Set-Alias\s+(\S+)\s+(\S+).*$', original_content, re.MULTILINE):
                        alias_names.add(alias_match.group(1))
                        target_names.add(alias_match.group(2))
                    
                    # 3) 移除未标记的 Set-Alias 行
                    setalias_pattern = re.compile(r'^Set-Alias\s+\S+\s+\S+.*$', re.MULTILINE)
                    content = setalias_pattern.sub("", content)
                    
                    # 4) 移除对应的未标记函数块（包括目标函数名和可能同名别名的函数）
                    for name in list(alias_names | target_names | func_names):
                        func_pat = re.compile(rf"function\s+{re.escape(name)}\s*{{[\s\S]*?}}", re.MULTILINE)
                        content = re.sub(func_pat, "", content)
                    
                    # 5) 过滤仅数字的噪声行和 Unicode 控制字符
                    lines = content.splitlines()
                    filtered_lines = []
                    cleanup_names = alias_names | target_names | func_names
                    
                    for line in lines:
                        # 移除 Unicode 控制字符
                        clean_line = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', line)
                        
                        # 跳过仅数字的行
                        if re.match(r'^\s*\d+\s*$', clean_line):
                            continue
                        
                        # 跳过仅包含清理名称的行
                        if cleanup_names and re.match(rf'^[\s\u200e\u200f\u202a-\u202e]*({"|".join(re.escape(name) for name in cleanup_names)})[\s\u200e\u200f\u202a-\u202e]*$', clean_line):
                            continue
                        
                        filtered_lines.append(line)
                    
                    content = '\n'.join(filtered_lines)
                
                # 清理多余的空行
                content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
                content = content.strip()
                
                # 写回文件
                if content:
                    self.write_text_with_encoding(profile_path, content + '\n', encoding)
                else:
                    profile_path.unlink()  # 如果内容为空，删除文件
                
                cleaned_profiles.append(str(profile_path))
            
            if cleaned_profiles:
                return True, f"已清理 PowerShell 配置文件: {', '.join(cleaned_profiles)}" + (" 并进行了深度清理" if aggressive else "")
            else:
                return True, "未找到 PowerShell 配置文件，无需清理"
                
        except Exception as e:
            return False, f"清理 PowerShell 配置失败: {e}"
    
    def print_aliases(self) -> None:
        """打印当前 PowerShell 别名配置"""
        profile_path = self.profile_path()
        if not profile_path.exists():
            ERROR("未找到 PowerShell 配置文件")
            return
        # 打印配置文件的路径
        INFO("当前 PowerShell 别名配置文件路径:")
        SUCCESS(profile_path)
        content = profile_path.read_text(encoding="utf-8", errors="ignore")

        # 解析 Set-Alias 行（alias -> target）
        alias_pattern = re.compile(r"^\s*Set-Alias\s+([A-Za-z0-9_-]+)\s+([A-Za-z0-9_-]+).*$", re.MULTILINE)
        set_aliases = alias_pattern.findall(content)

        # 解析 alias-manager 标记的函数块（function 名称）
        func_names = set()
        marked_block_pat = re.compile(r"#\s*alias-manager\s*:\s*start[\s\S]*?#\s*alias-manager\s*:\s*end", re.MULTILINE)
        for m in marked_block_pat.finditer(content):
            block = m.group(0)
            fn = re.search(r"function\s+(\S+)\s*\{", block)
            if fn:
                func_names.add(fn.group(1))

        if set_aliases or func_names:
            INFO("当前 PowerShell 别名配置：")
            # 先打印 Set-Alias 映射
            if set_aliases:
                for alias, target in sorted(set_aliases):
                    SUCCESS(f"  {alias} -> {target}")
            # 再打印函数别名（避免与 Set-Alias 重复）
            alias_names = {a for a, _ in set_aliases}
            remaining_funcs = sorted(name for name in func_names if name not in alias_names)
            for name in remaining_funcs:
                SUCCESS(f"  {name}")
        else:
            ERROR("当前 PowerShell 没有定义别名")