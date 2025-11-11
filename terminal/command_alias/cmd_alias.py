import os
import re
import subprocess
from pathlib import Path
from typing import Tuple
from .base_alias import BaseAliasManager
from public.logger import *

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
            # powershell -NoProfile -Command (Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -ErrorAction SilentlyContinue).AutoRun
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
        except Exception as e:  # type: ignore
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
                    filtered.append(l) # type: ignore
                content = "\n".join(filtered) # type: ignore
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
            current_value = current_value.replace(resolved_value, "") # type: ignore
            ps_set = [
                "powershell", "-NoProfile", "-Command",
                f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -Type ExpandString -Value '{current_value}'"
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

    def print_aliases(self) -> None:
        """打印当前 CMD 别名配置"""
        alias_file = self.alias_file()
        if not alias_file.exists():
            ERROR("未找到 cmd_aliases.cmd 文件")
        else:
            # 打印配置文件的路径
            INFO(f"当前 CMD 别名配置文件路径:")
            SUCCESS(alias_file) # type: ignore
            content = alias_file.read_text(encoding="utf-8", errors="ignore")
            alias_pattern = re.compile(r"^\s*doskey\s+([A-Za-z0-9_-]+)\s*=.*$", re.MULTILINE)
            matches = alias_pattern.findall(content)
            if matches:
                INFO("当前 CMD 别名配置：")
                for alias in sorted(matches):
                    SUCCESS(f"  {alias}")
            else:
                ERROR("当前 CMD 没有定义别名")
        # 打印autorun中的内容
        INFO("当前 AutoRun 配置：")
        ps_get = [
            "powershell", "-NoProfile", "-Command",
            "(Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Command Processor' -Name AutoRun -ErrorAction SilentlyContinue).AutoRun"
        ]
        query = subprocess.run(ps_get, capture_output=True, text=True)
        current_value = (query.stdout or "").strip() if query.returncode == 0 else None
        SUCCESS(f"  {current_value}")
        WARNING(r"注册表配置：计算机\HKEY_CURRENT_USER\Software\Microsoft\Command Processor")
