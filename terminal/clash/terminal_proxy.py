# 内部导包
from public import *
from command_alias import set_terminal_alias
# 外部导包
from pathlib import Path
import json
import click

@click.command()
def cli_proxy_config():
    """配置别名Clash Terminal Proxy
    """
    # 配置开启代理配置
    cmd_str = """
    set http_proxy=http://127.0.0.1:7890$T
    set https_proxy=http://127.0.0.1:7890$T
    echo "Proxy configured successfully."
    """.replace("\n", " ")
    ps_str = """
    $Env:http_proxy="http://127.0.0.1:7890";
    $Env:https_proxy="http://127.0.0.1:7890";
    Write-Host "✓ Proxy configured successfully." -ForegroundColor Green
    """
    bash_str = """
    export https_proxy=http://127.0.0.1:7890;
    export http_proxy=http://127.0.0.1:7890;
    export all_proxy=socks5://127.0.0.1:7890;
    echo "Proxy configured successfully."
    """.replace("\n", "")
    set_terminal_alias('proxy-on', cmd_str, 'cmd')
    set_terminal_alias('proxy-on', ps_str, 'powershell')
    set_terminal_alias('proxy-on', bash_str, 'bash')
    SUCCESS("Clash Terminal Proxy on config 更新完成")

    # 配置关闭代理配置
    cmd_str = """
    set http_proxy= $T
    set https_proxy= $T
    echo "Proxy disabled successfully."
    """.replace("\n", " ")
    ps_str = """
    $Env:http_proxy="";
    $Env:https_proxy=""
    Write-Host "✓ Proxy disabled successfully." -ForegroundColor Green
    """
    bash_str = """
    unset https_proxy;
    unset http_proxy;
    unset all_proxy;
    echo "Proxy disabled successfully."
    """.replace("\n", "")
    set_terminal_alias('proxy-off', cmd_str, 'cmd')
    set_terminal_alias('proxy-off', ps_str, 'powershell')
    set_terminal_alias('proxy-off', bash_str, 'bash')
    SUCCESS("Clash Terminal Proxy off config 更新完成")
    WARNING("请重新打开终端窗口，使配置生效")

    
if __name__ == '__main__':
    set_terminal_alias('config_on', 'echo on', 'powershell')
    set_terminal_alias('config_off', 'echo off', 'powershell')