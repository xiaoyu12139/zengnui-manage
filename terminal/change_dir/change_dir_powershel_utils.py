#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import click
import questionary
import configparser
from pathlib import Path

def create_powershell_module(module_name: str, directories: dict, aliases: dict):
    """
    通用的 PowerShell 模块创建函数
    
    Args:
        module_name: 模块名称，如 "DirectorySwitch"
        directories: 目录配置 {'plugin': {'path': 'D:/path', 'desc': 'Plugin 目录'}}
        aliases: 别名配置 {'plugin': 'cdp', 'proxy': 'cdx', 'help': 'ds-help'}
    
    Returns:
        tuple: (success: bool, module_path: Path, error_msg: str)
    """
    try:
        import datetime
        import uuid
        import shutil
        
        # 获取 PowerShell 模块路径
        result = subprocess.run(
            ["powershell", "-Command", "$env:PSModulePath -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }"],
            capture_output=True, text=True, check=True
        )
        
        module_paths = [Path(path.strip()) for path in result.stdout.strip().split('\n') if path.strip()]
        
        # 优先使用用户目录避免权限问题
        module_base_path = None
        user_paths = [p for p in module_paths if 'Users' in str(p)]
        
        for path in user_paths:
            if path.exists():
                module_base_path = path
                break
        
        if not module_base_path:
            # 创建用户模块目录
            user_module_path = Path.home() / "Documents" / "WindowsPowerShell" / "Modules"
            user_module_path.mkdir(parents=True, exist_ok=True)
            module_base_path = user_module_path
        
        # 创建模块目录
        module_dir = module_base_path / module_name
        if module_dir.exists():
            shutil.rmtree(module_dir)
        module_dir.mkdir(exist_ok=True)
        
        # 生成时间戳和 GUID
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        module_guid = str(uuid.uuid4())
        
        # 生成 PowerShell 函数
        functions = []
        alias_lines = []
        help_lines = []
        export_functions = []
        export_aliases = []
        
        # 为每个目录生成函数
        for key, config in directories.items():
            func_name = f"Switch-To{key.title()}"
            alias_name = aliases.get(key, key)
            path = config['path']
            desc = config['desc']
            
            # 生成切换函数
            func_code = f"""function {func_name} {{
    $TargetDir = "{path}"
    if (Test-Path $TargetDir) {{
        $OldDir = Get-Location
        Set-Location $TargetDir
        Write-Host "✓ 已切换到 {desc}: $TargetDir" -ForegroundColor Green
        Write-Host "  (从: $OldDir)" -ForegroundColor Gray
    }} else {{
        Write-Error "{desc}不存在: $TargetDir"
    }}
}}"""
            functions.append(func_code)
            alias_lines.append(f'Set-Alias -Name "{alias_name}" -Value "{func_name}"')
            help_lines.append(f'    Write-Host "  {func_name}  (别名: {alias_name})  - 切换到 {desc}" -ForegroundColor Green')
            export_functions.append(func_name)
            export_aliases.append(alias_name)
        
        # 生成帮助函数
        help_alias = aliases.get('help', 'ds-help')
        help_func = f"""function Show-{module_name}Help {{
    Write-Host "{module_name} 模块命令:" -ForegroundColor Cyan
{chr(10).join(help_lines)}
    Write-Host "  Show-{module_name}Help (别名: {help_alias}) - 显示此帮助信息" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "配置信息:" -ForegroundColor Cyan
{chr(10).join([f'    Write-Host "  {config["desc"]}: {config["path"]}" -ForegroundColor White' for config in directories.values()])}
}}"""
        functions.append(help_func)
        alias_lines.append(f'Set-Alias -Name "{help_alias}" -Value "Show-{module_name}Help"')
        export_functions.append(f"Show-{module_name}Help")
        export_aliases.append(help_alias)
        
        # 生成完整模块内容
        module_content = f"""#!/usr/bin/env pwsh
# {module_name} PowerShell Module - 生成于: {timestamp}

{chr(10).join(functions)}

# 创建别名
{chr(10).join(alias_lines)}

# 导出函数和别名
Export-ModuleMember -Function {', '.join(export_functions)} -Alias {', '.join(export_aliases)}

Write-Host "{module_name} 模块已加载! 输入 '{help_alias}' 查看帮助" -ForegroundColor Yellow
"""
        
        # 写入文件
        (module_dir / f"{module_name}.psm1").write_text(module_content, encoding="utf-8-sig")
        
        # 生成清单文件
        manifest = f"""@{{
    RootModule = '{module_name}.psm1'
    ModuleVersion = '1.0.0'
    GUID = '{module_guid}'
    Author = 'Company CLI Tool'
    Description = '{module_name} Tool'
    PowerShellVersion = '5.1'
    FunctionsToExport = @({', '.join([f"'{f}'" for f in export_functions])})
    AliasesToExport = @({', '.join([f"'{a}'" for a in export_aliases])})
}}"""
        (module_dir / f"{module_name}.psd1").write_text(manifest, encoding="utf-8-sig")
        
        return True, module_dir, None
        
    except Exception as e:
        return False, None, str(e)


def test_powershell_module(module_name: str, test_alias: str):
    """测试 PowerShell 模块是否正常工作"""
    try:
        test_result = subprocess.run([
            "powershell", "-Command", f"""
            Remove-Module {module_name} -Force -ErrorAction SilentlyContinue
            Import-Module {module_name} -Force
            if (Get-Command {test_alias} -ErrorAction SilentlyContinue) {{
                Write-Host "✓ 模块测试成功" -ForegroundColor Green
            }} else {{
                Write-Host "✗ 模块测试失败" -ForegroundColor Red
                exit 1
            }}
            """
        ], capture_output=True, text=True)
        
        return test_result.returncode == 0, test_result.stdout.strip()
    except Exception as e:
        return False, str(e)