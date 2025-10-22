import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import click

try:
    # Reuse existing terminal detection if available
    from .check_terminal_type import get_terminal_type
except Exception:
    def get_terminal_type() -> str:
        # Fallback: naive detection
        return 'powershell' if os.name == 'nt' else 'bash'

class BaseAliasManager:
    def sanitize_alias_name(self, name: str) -> str:
        # Keep simple, letters, numbers, hyphen/underscore
        return re.sub(r"[^A-Za-z0-9_-]", "", name).strip()

    def ensure_parent(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def read_text_with_encoding(self, path: Path) -> Tuple[str, str]:
        """读取文件并自动检测编码，返回 (规范化为 LF 的内容, 编码)
        - 统一将换行规范化为 "\n"，便于正则与文本处理
        - 保留原始编码信息以便写回时复原
        """
        if not path.exists():
            return "", "utf-8"
        
        raw = path.read_bytes()
        for encoding in ('utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'utf-8', 'gbk'):
            try:
                content = raw.decode(encoding)
                # 统一换行为 LF
                content = content.replace('\r\n', '\n')
                return content, encoding
            except Exception:
                continue
        
        # 如果都失败，使用 utf-8 并忽略错误
        content = raw.decode('utf-8', errors='ignore')
        content = content.replace('\r\n', '\n')
        return content, 'utf-8'

    def write_text_with_encoding(self, path: Path, content: str, encoding: str = 'utf-8') -> None:
        """使用指定编码写入文件，并自动复原原文件的换行风格
        - 输入内容应为统一的 LF（如果不是，本方法也会先规范化）
        - 如果目标文件已存在，则依据其二进制内容判断使用 CRLF 或 LF
        - 如果目标文件不存在，则在 Windows 使用 CRLF，否则使用 LF
        - 始终保证文件以单个换行结尾
        """
        # 规范化为 LF
        normalized = content.replace('\r\n', '\n')
        # 保证以单个换行结尾
        normalized = normalized.rstrip('\n') + '\n'

        normalized = re.sub(r'\n+', '\n', normalized)
        path.write_text(normalized, encoding=encoding)


class CmdAliasManager(BaseAliasManager):
    def alias_file(self) -> Path:
        return Path.home() / "cmd_aliases.cmd"

    def ensure_autorun_points_to(self, file_path: Path) -> None:
        try:
            user_home = str(Path.home())
            fp = str(file_path)
            if fp.lower().startswith(user_home.lower()):
                rel_fp = fp.replace(user_home, "%USERPROFILE%")
            else:
                rel_fp = fp
            macro_cmd = f'if exist "{rel_fp}" call "{rel_fp}" >nul 2>&1'

            ps_get = [
                "powershell", "-NoProfile", "-Command",
                "(Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -ErrorAction SilentlyContinue).AutoRun"
            ]
            query = subprocess.run(ps_get, capture_output=True, text=True)
            current_value = (query.stdout or "").strip() if query.returncode == 0 else None

            if current_value:
                # pattern = re.compile(r'(?:cmd\s*/c|call)\s*(?:"[^"]*cmd_aliases\\.cmd"|[^\s&]*cmd_aliases\\.cmd)', re.IGNORECASE)
                # pattern = re.compile(r'(?:if\s+exist\s+)?(?:cmd\s*/c|call)\s*(?:"[^"]*cmd_aliases\.cmd"|[^\s&]*cmd_aliases\.cmd)(?=\s*(?:>nul|2>&1|$))', re.IGNORECASE)
                pattern = re.compile(r'(?:call)\s*(?:"[^"]*cmd_aliases\.cmd"|[^\s&]*cmd_aliases\.cmd)', re.IGNORECASE)
                # 经测试，如果已经包含了会走到这里，但sub时会报错就不走下面的逻辑了，所以正常运行
                # 如果不存在则会一直执行
                if pattern.search(current_value):
                    new_value = pattern.sub(macro_cmd, current_value)
                else:
                    new_value = f"{current_value} & {macro_cmd}"
            else:
                new_value = macro_cmd

            subprocess.run([
                "powershell", "-NoProfile", "-Command",
                "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name DisableAutoRun -Type DWord -Value 0"
            ], capture_output=True, text=True)

            safe_value = new_value.replace("'", "''")
            ps_set = [
                "powershell", "-NoProfile", "-Command",
                f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -Type ExpandString -Value '{safe_value}'"
            ]
            add = subprocess.run(ps_set, capture_output=True, text=True)
            if add.returncode != 0:
                subprocess.run([
                    "REG", "ADD", '"HKCU\\Software\\Microsoft\\Command Processor"',
                    "/v", "AutoRun",
                    "/t", "REG_EXPAND_SZ",
                    "/d", new_value,
                    "/f"
                ], capture_output=True, text=True)
        except Exception as e:
            # print(f"设置 CMD AutoRun 失败: {e}")
            pass

    def set_alias(self, alias_name: str, command: str) -> Tuple[bool, str]:
        alias = self.sanitize_alias_name(alias_name)
        if not alias:
            return False, "无效的别名名称"

        file_path = self.alias_file()
        self.ensure_parent(file_path)

        line = f"doskey {alias}={command}\n"
        try:
            content = ""
            if file_path.exists():
                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                filtered = []
                for l in raw.splitlines():
                    if re.match(rf"^\s*doskey\s+{re.escape(alias)}\s*=", l, re.IGNORECASE):
                        continue
                    filtered.append(l)
                content = "\n".join(filtered)
                head = "@echo off\n"
                if not content.strip().lower().startswith("@echo off"):
                    content = head + content.lstrip()
                if content and not content.endswith("\n"):
                    content += "\n"
                content += line
                file_path.write_text(content, encoding="utf-8")
            else:
                file_path.write_text("@echo off\n" + line, encoding="utf-8")
        except Exception as e:
            return False, f"写入 CMD 别名文件失败: {e}"

        try:
            self.ensure_autorun_points_to(file_path)
        except Exception as e:
            return True, f"已更新 {file_path}，但设置 AutoRun 失败: {e}"

        return True, f"CMD 别名已持久化：{alias} -> {command}"

    def reset(self, aggressive: bool = False) -> Tuple[bool, str]:
        """重置 CMD 别名配置"""
        try:
            file_path = self.alias_file()
            removed_file = False
            
            # 删除别名文件
            if file_path.exists():
                file_path.unlink()
                removed_file = True
            
            # 删除 AutoRun 中的调用
            user_home = str(Path.home())
            fp = str(file_path)
            if fp.lower().startswith(user_home.lower()):
                rel_fp = fp.replace(user_home, "%USERPROFILE%")
            else:
                rel_fp = fp
            macro_cmd = f'if exist "{rel_fp}" call "{rel_fp}" >nul 2>&1'

            ps_get = [
                "powershell", "-NoProfile", "-Command",
                "(Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -ErrorAction SilentlyContinue).AutoRun"
            ]
            query = subprocess.run(ps_get, capture_output=True, text=True)
            current_value = (query.stdout or "").strip() if query.returncode == 0 else None
            # 获取环境变量并替换
            resolved_value = os.path.expandvars(macro_cmd)
            current_value = current_value.replace(resolved_value, "")
            ps_set = [
                "powershell", "-NoProfile", "-Command",
                f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -Type ExpandString -Value '{resolved_value_rpl}'"
            ]
            subprocess.run(ps_set, capture_output=True, text=True)
            
            # 如果是 aggressive 模式，清理注册表中的 AutoRun 设置
            if aggressive:
                try:
                    # 清除 AutoRun 注册表项
                    subprocess.run([
                        "powershell", "-NoProfile", "-Command",
                        "Remove-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -ErrorAction SilentlyContinue"
                    ], capture_output=True, text=True)
                except Exception:
                    pass
            
            if removed_file:
                return True, f"已删除 CMD 别名文件: {file_path}" + (" 并清理了注册表设置" if aggressive else "")
            else:
                return True, "未找到 CMD 别名文件，无需清理" + (" 但已清理注册表设置" if aggressive else "")
                
        except Exception as e:
            return False, f"清理 CMD 别名失败: {e}"


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


class BashAliasManager(BaseAliasManager):
    def bashrc_path(self) -> Path:
        return Path.home() / ".bashrc"

    def set_alias(self, alias_name: str, command: str) -> Tuple[bool, str]:
        alias = self.sanitize_alias_name(alias_name)
        if not alias:
            return False, "无效的别名名称"
        bashrc = self.bashrc_path()
        self.ensure_parent(bashrc)
        safe_cmd = command.replace("'", "'\\''")
        block = f"# alias-manager: start {alias}\nalias {alias}='{safe_cmd}'\n# alias-manager: end {alias}\n"
        try:
            content = ""
            if bashrc.exists():
                content, _ = self.read_text_with_encoding(bashrc)
                # 移除现有的标记块
                pattern = re.compile(rf"#\s*alias-manager\s*:\s*start\s+{re.escape(alias)}[\s\S]*?#\s*alias-manager\s*:\s*end\s+{re.escape(alias)}", re.MULTILINE)
                if pattern.search(content):
                    content = pattern.sub(block.strip(), content)
                else:
                    content = content + ("\n" if not content.endswith("\n") else "") + block
                self.write_text_with_encoding(bashrc, content, 'utf-8')
            else:
                self.write_text_with_encoding(bashrc, block, 'utf-8')
        except Exception as e:
            return False, f"写入 ~/.bashrc 失败: {e}"
        return True, f"Bash 别名已持久化：{alias} -> {command}\n重新加载：source ~/.bashrc"

    def reset(self, aggressive: bool = False) -> Tuple[bool, str]:
        """重置 Bash 别名配置
        
        Args:
            aggressive: 如果为 True，则额外删除所有 alias name='...' 行（可能删除用户自定义别名）
        """
        try:
            bashrc = self.bashrc_path()
            if not bashrc.exists():
                return True, "未找到 ~/.bashrc 文件，无需清理"
            
            content, encoding = self.read_text_with_encoding(bashrc)
            if not content.strip():
                return True, "~/.bashrc 文件为空，无需清理"
            
            # 1) 移除标记块
            marked_pattern = re.compile(r"#\s*alias-manager\s*:\s*start(?:\s+\S+)?[\s\S]*?#\s*alias-manager\s*:\s*end(?:\s+\S+)?", re.MULTILINE)
            content = marked_pattern.sub("", content)
            
            if aggressive:
                # 2) 移除所有 alias name='...' 行
                # 注意：这可能会删除用户自定义的别名
                alias_pattern = re.compile(r"^\s*alias\s+[A-Za-z0-9_-]+\s*=.*$", re.MULTILINE)
                content = alias_pattern.sub("", content)
            
            # 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip()
            
            # 写回文件
            if content:
                self.write_text_with_encoding(bashrc, content + '\n', encoding)
            else:
                bashrc.unlink()  # 如果内容为空，删除文件
            
            return True, f"已清理 ~/.bashrc 文件" + (" 并删除了所有别名行" if aggressive else "")
            
        except Exception as e:
            return False, f"清理 ~/.bashrc 失败: {e}"


class TerminalAliasService:
    def get_manager(self, shell: Optional[str] = None):
        target = shell or get_terminal_type()
        target = (target or "").lower()
        if target in ("cmd", "command prompt"):
            return CmdAliasManager()
        elif target in ("powershell", "pwsh"):
            return PowerShellAliasManager()
        elif target in ("bash", "posix"):
            return BashAliasManager()
        else:
            if os.name == 'nt':
                return PowerShellAliasManager()
            else:
                return BashAliasManager()

    def set_alias(self, alias_name: str, command: str, shell: Optional[str] = None) -> Tuple[bool, str]:
        mgr = self.get_manager(shell)
        # PowerShell 采用函数持久化作为统一语义
        if isinstance(mgr, PowerShellAliasManager):
            return mgr.set_function(alias_name, command)
        return mgr.set_alias(alias_name, command)

    def reset_terminal_aliases(self, shell: Optional[str] = None, aggressive: bool = False) -> Tuple[bool, str]:
        """重置指定终端的别名配置"""
        mgr = self.get_manager(shell)
        return mgr.reset(aggressive)

    def reset_all_terminal_aliases(self, aggressive: bool = False) -> Tuple[bool, str]:
        """重置所有终端的别名配置"""
        results = []
        errors = []
        
        # 重置 CMD
        try:
            cmd_mgr = CmdAliasManager()
            success, msg = cmd_mgr.reset(aggressive)
            results.append(f"CMD: {msg}")
            if not success:
                errors.append(f"CMD: {msg}")
        except Exception as e:
            errors.append(f"CMD: {str(e)}")
        
        # 重置 PowerShell
        try:
            ps_mgr = PowerShellAliasManager()
            success, msg = ps_mgr.reset(aggressive)
            results.append(f"PowerShell: {msg}")
            if not success:
                errors.append(f"PowerShell: {msg}")
        except Exception as e:
            errors.append(f"PowerShell: {str(e)}")
        
        # 重置 Bash
        try:
            bash_mgr = BashAliasManager()
            success, msg = bash_mgr.reset(aggressive)
            results.append(f"Bash: {msg}")
            if not success:
                errors.append(f"Bash: {msg}")
        except Exception as e:
            errors.append(f"Bash: {str(e)}")
        
        if errors:
            return False, f"部分重置失败: {'; '.join(errors)}"
        else:
            return True, f"所有终端重置成功: {'; '.join(results)}"

# 新接口：不再直接使用旧的函数式入口

def set_terminal_alias(alias_name: str, command: str, shell: Optional[str] = None) -> Tuple[bool, str]:
    return TerminalAliasService().set_alias(alias_name, command, shell)


def set_persistent_alias(alias_name: str, command: str, shell: Optional[str] = None) -> Tuple[bool, str]:
    return set_terminal_alias(alias_name, command, shell)


def reset_terminal_aliases(shell: Optional[str] = None, aggressive: bool = False) -> Tuple[bool, str]:
    """重置指定终端的别名配置
    
    Args:
        shell: 终端类型 (cmd/powershell/bash)，None 表示自动检测
        aggressive: 是否使用激进模式，清理所有相关内容
    
    Returns:
        (success, message): 操作结果和消息
    """
    return TerminalAliasService().reset_terminal_aliases(shell, aggressive)

@click.command()
def reset_all_terminal_aliases(aggressive: bool = False) -> Tuple[bool, str]:
    """重置所有终端的别名配置
    
    Args:
        aggressive: 是否使用激进模式，清理所有相关内容
    
    Returns:
        (success, message): 操作结果和消息
    """
    return TerminalAliasService().reset_all_terminal_aliases(aggressive)


if __name__ == "__main__":
    # set_terminal_alias('clash1', 'echo 1234', 'cmd')
    # set_terminal_alias('clash2', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234last', 'bash')
    reset_terminal_aliases('cmd')