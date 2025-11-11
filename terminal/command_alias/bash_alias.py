import re
from pathlib import Path
from typing import Tuple
from .base_alias import BaseAliasManager
from public.logger import *

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
    
    def print_aliases(self) -> None:
        """打印当前 Bash 别名配置"""
        bashrc = self.bashrc_path()
        if not bashrc.exists():
            ERROR("未找到 ~/.bashrc 文件")
            return
        # 打印配置文件的路径
        SUCCESS(f"当前 Bash 别名配置文件路径：{bashrc}")
        content, _ = self.read_text_with_encoding(bashrc)
        alias_pattern = re.compile(r"^\s*alias\s+([A-Za-z0-9_-]+)\s*=.*$", re.MULTILINE)
        matches = alias_pattern.findall(content)
        if matches:
            INFO("当前 Bash 别名配置：")
            for alias in sorted(matches):
               SUCCESS(f"  {alias}")
        else:
            ERROR("当前 Bash 没有定义别名")
