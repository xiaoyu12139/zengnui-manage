import os
from typing import Optional, Tuple
import click
from .bash_alias import BashAliasManager
from .cmd_alias import CmdAliasManager
from .powershell_alias import PowerShellAliasManager
from public import *

try:
    # Reuse existing terminal detection if available
    from .check_terminal_type import get_terminal_type # type: ignore
except Exception:
    def get_terminal_type() -> str:
        # Fallback: naive detection
        return 'powershell' if os.name == 'nt' else 'bash'

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
            results.append(f"CMD: {msg}") # type: ignore
            if not success:
                errors.append(f"CMD: {msg}") # type: ignore
        except Exception as e:
            errors.append(f"CMD: {str(e)}") # type: ignore
        
        # 重置 PowerShell
        try:
            ps_mgr = PowerShellAliasManager()
            success, msg = ps_mgr.reset(aggressive)
            results.append(f"PowerShell: {msg}") # type: ignore
            if not success:
                errors.append(f"PowerShell: {msg}") # type: ignore
        except Exception as e:
            errors.append(f"PowerShell: {str(e)}") # type: ignore
        
        # 重置 Bash
        try:
            bash_mgr = BashAliasManager()
            success, msg = bash_mgr.reset(aggressive)
            results.append(f"Bash: {msg}") # type: ignore
            if not success:
                errors.append(f"Bash: {msg}") # type: ignore
        except Exception as e:
            errors.append(f"Bash: {str(e)}") # type: ignore 
        
        if errors:
            return False, f"部分重置失败: {'; '.join(errors)}" # type: ignore
        else:
            return True, f"所有终端重置成功: {'; '.join(results)}" # type: ignore
    
########################################### 接口定义 ###########################################
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

def reset_all_terminal_aliases(aggressive: bool = False) -> Tuple[bool, str]:
    """重置所有终端的别名配置
    
    Args:
        aggressive: 是否使用激进模式，清理所有相关内容
    
    Returns:
        (success, message): 操作结果和消息
    """
    success, message = TerminalAliasService().reset_all_terminal_aliases(aggressive)
    if success:
        SUCCESS(message)
    else:
        ERROR(message)
    
    return success, message


def print_aliases_config(shell: Optional[str] = None) -> None:
    mgr = TerminalAliasService().get_manager(shell)
    mgr.print_aliases()

########################################### 命令定义 ###########################################
@click.command()
def reset_all():
    reset_all_terminal_aliases()

@click.command()
@click.option('-s', 'shell', type=click.Choice(['cmd', 'ps', 'bash']),required=True,help='指定终端类型：cmd / ps / bash')
@click.option('-p', 'do_print', is_flag=True, help='打印别名配置')
@click.option('-d', 'do_delete', is_flag=True, help='删除别名配置')
def cli(shell, do_print, do_delete): # type: ignore
    # 互斥校验
    if do_print and do_delete:
        raise click.UsageError('请只选择一种操作：--print 或 --delete')

    # 统一 shell 名称映射
    shell_map = {'ps': 'powershell', 'cmd': 'cmd', 'bash': 'bash'}
    target_shell = shell_map.get(shell, shell) # type: ignore

    # 分派动作
    if do_print:
        print_aliases_config(target_shell)
    elif do_delete:
        reset_terminal_aliases(target_shell, aggressive=aggressive) # type: ignore
    else:
        click.echo("请指定操作：-p 打印别名配置，-d 删除别名配置")

if __name__ == "__main__":
    # set_terminal_alias('clash1', 'echo 1234', 'cmd')
    # set_terminal_alias('clash2', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234', 'bash')
    # set_terminal_alias('clash1', 'echo 12341234last', 'bash')
    reset_terminal_aliases('cmd')