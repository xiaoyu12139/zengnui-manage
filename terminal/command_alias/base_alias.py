import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import click


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