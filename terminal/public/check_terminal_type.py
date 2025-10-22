import click
from public.logger import *
import os
import subprocess

# 先用环境变量快速判定
# env = os.environ
# prompt = env.get('PROMPT')
# psmod = env.get('PSModulePath')
# if psmod and not prompt:
#     return 'powershell'
# if prompt:
#     return 'cmd'

def _get_process_name_and_ppid(pid: int):
    # 优先使用 psutil 获取名称与父 PID
    try:
        import psutil
        proc = psutil.Process(pid)
        return proc.name(), proc.ppid()
    except Exception:
        pass
    # 回退使用 wmic
    try:
        out = subprocess.check_output(
            ['wmic', 'process', 'where', f'(ProcessId={pid})', 'get', 'Name,ParentProcessId', '/format:list'],
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        ).decode('utf-8', errors='ignore')
        name, ppid = None, None
        for line in out.splitlines():
            if line.startswith('Name='):
                name = line.split('=', 1)[1].strip()
            elif line.startswith('ParentProcessId='):
                try:
                    ppid = int(line.split('=', 1)[1].strip())
                except Exception:
                    ppid = None
        return name, ppid
    except Exception:
        pass
    # 最后回退仅通过 tasklist 获取名称
    try:
        out = subprocess.check_output(
            ['tasklist', '/FI', f'PID eq {pid}'],
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        ).decode('utf-8', errors='ignore')
        lines = [l for l in out.splitlines() if l.strip()]
        for l in lines:
            tk = l.strip().split()
            if tk and tk[0].lower().endswith('.exe'):
                return tk[0], None
    except Exception:
        pass
    return None, None

def _detect_shell_on_windows():
    # 先用环境变量快速判定（Git Bash 常见标识）
    env = os.environ
    shell_env = (env.get('SHELL') or '').lower()
    msystem = env.get('MSYSTEM')  # 例如 MINGW64/MINGW32/MSYS
    if 'bash' in shell_env or msystem:
        return 'bash'
    # 沿父进程链搜索已知 shell 进程
    max_hops = 16
    pid = os.getppid()
    visited = set()
    found_cmd = False
    for _ in range(max_hops):
        name, ppid = _get_process_name_and_ppid(pid)
        if not name:
            break
        n = name.lower()
        # Git Bash / MSYS2 / mintty
        if 'bash' in n or n.startswith('sh') or 'mintty' in n or 'git-bash' in n:
            return 'bash'
        # PowerShell
        if 'powershell' in n or 'pwsh' in n:
            return 'powershell'
        # cmd
        if n.startswith('cmd'):
            found_cmd = True
        if ppid is None or ppid == 0 or ppid in visited:
            break
        visited.add(pid)
        pid = ppid
    # 保守回退为 cmd（仅当链上曾出现过 cmd），否则标记为未知
    if found_cmd:
        return 'cmd'
    return 'unknown'

def get_terminal_type():
    """获取当前终端类型：Windows 下识别 cmd / PowerShell / Git Bash；其他系统为 posix"""
    shell = _detect_shell_on_windows() if os.name == 'nt' else 'posix'
    if shell == 'powershell':
        INFO("当前环境为powershell")
        return 'powershell'
    elif shell == 'cmd':
        INFO("当前环境为cmd")
        return 'cmd'
    elif shell == 'bash':
        INFO("当前环境为git bash")
        return 'bash'
    elif shell == 'posix':
        INFO("当前环境为posix")
        return 'posix'
    else:
        INFO(f"当前环境为{shell}")
        return shell
