import os
import sys
import re
import platform
import winreg
import subprocess
from pathlib import Path
from typing import Optional, Tuple

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
                pattern = re.compile(r'(?:cmd\s*/c|call)\s*(?:"[^"]*cmd_aliases\\.cmd"|[^\s&]*cmd_aliases\\.cmd)', re.IGNORECASE)
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
        except Exception:
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
        fn_block = (
            f"function {alias} {{\n" 
            f"    {body}\n" 
            f"}}\n"
        )
        try:
            content = ""
            if profile_path.exists():
                content = profile_path.read_text(encoding="utf-8", errors="ignore")
                pattern = re.compile(rf"function\\s+{re.escape(alias)}\\s*{{[\\s\\S]*?}}", re.MULTILINE)
                if pattern.search(content):
                    content = pattern.sub(fn_block.strip(), content)
                else:
                    content = content + ("\n" if not content.endswith("\n") else "") + fn_block
                profile_path.write_text(content, encoding="utf-8")
            else:
                profile_path.write_text(fn_block, encoding="utf-8")
        except Exception as e:
            return False, f"写入 PowerShell 配置失败: {e}"
        return True, f"PowerShell 函数已持久化：{alias} -> {command}\n重新加载：. $PROFILE"

    def set_alias(self, alias_name: str, target_function: str) -> Tuple[bool, str]:
        alias = self.sanitize_alias_name(alias_name)
        target = self.sanitize_alias_name(target_function)
        if not alias or not target:
            return False, "无效的别名或目标函数名称"
        profile_path = self.profile_path()
        self.ensure_parent(profile_path)
        line = f"Set-Alias {alias} {target}\n"
        try:
            content = ""
            if profile_path.exists():
                content = profile_path.read_text(encoding="utf-8", errors="ignore")
                pattern = re.compile(rf"^Set-Alias\\s+{re.escape(alias)}\\s+\\S+.*$", re.MULTILINE)
                if pattern.search(content):
                    content = pattern.sub(line.strip(), content)
                else:
                    content = content + ("\n" if not content.endswith("\n") else "") + line
                profile_path.write_text(content, encoding="utf-8")
            else:
                profile_path.write_text(line, encoding="utf-8")
        except Exception as e:
            return False, f"写入 PowerShell 配置失败: {e}"
        return True, f"PowerShell 别名已持久化：{alias} -> {target}\n重新加载：. $PROFILE"


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
        line = f"alias {alias}='{safe_cmd}'\n"
        try:
            content = ""
            if bashrc.exists():
                raw = bashrc.read_text(encoding="utf-8", errors="ignore")
                filtered = []
                for l in raw.splitlines():
                    if re.match(rf"^\s*alias\s+{re.escape(alias)}\s*=", l):
                        continue
                    filtered.append(l)
                content = "\n".join(filtered)
                if content and not content.endswith("\n"):
                    content += "\n"
                content += line
                bashrc.write_text(content, encoding="utf-8")
            else:
                bashrc.write_text(line, encoding="utf-8")
        except Exception as e:
            return False, f"写入 ~/.bashrc 失败: {e}"
        return True, f"Bash 别名已持久化：{alias} -> {command}\n重新加载：source ~/.bashrc"


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

# 新接口：不再直接使用旧的函数式入口

def set_terminal_alias(alias_name: str, command: str, shell: Optional[str] = None) -> Tuple[bool, str]:
    return TerminalAliasService().set_alias(alias_name, command, shell)


def set_persistent_alias(alias_name: str, command: str, shell: Optional[str] = None) -> Tuple[bool, str]:
    return set_terminal_alias(alias_name, command, shell)