# PowerShell 目录切换模块生成器

一个通用的 Python 工具，用于创建 PowerShell 模块来实现快速目录切换功能。通过简单的配置就能生成自定义的 PowerShell 命令和别名。

## 🌟 功能特点

- **通用性强**: 一个函数支持创建任意数量目录的切换模块
- **自定义别名**: 支持完全自定义的命令别名
- **自动处理**: 自动检测 PowerShell 模块路径、处理编码、生成模块清单
- **扩展性好**: 易于扩展到不同的目录配置场景
- **完整功能**: 包含帮助系统、错误处理、模块测试等完整功能

## 📁 文件结构

```
change_dir/
├── change_plugin_proxy_dir.py    # 主要工具 - Plugin/Proxy 目录切换
├── example_extended.py           # 扩展示例 - 演示不同类型的模块
├── config_generator.py           # 配置驱动的生成器
├── config.ini                   # 配置文件
└── README.md                    # 本说明文档
```

## 🚀 快速开始

### 基本使用

1. **运行主要工具**：
   ```bash
   cd d:\code\company-cli
   python -m change_dir.change_plugin_proxy_dir
   ```

2. **按提示配置**：
   - 选择是否自定义别名
   - 设置你喜欢的快捷命令名称

3. **在 PowerShell 中使用**：
   ```powershell
   Import-Module DirectorySwitch
   plugin  # 切换到 Plugin 目录
   proxy   # 切换到 Proxy 目录
   ds-help # 显示帮助信息
   ```

### 配置文件

编辑 `config.ini` 来设置你的目录路径：

```ini
[PLUGIN]
path = D:\your\plugin\path

[PROXY]  
path = D:\your\proxy\path
```

## 🔧 核心 API

### `create_powershell_module()`

通用的 PowerShell 模块创建函数：

```python
def create_powershell_module(module_name: str, directories: dict, aliases: dict):
    """
    Args:
        module_name: 模块名称，如 "DirectorySwitch"
        directories: 目录配置 {'plugin': {'path': 'D:/path', 'desc': 'Plugin 目录'}}
        aliases: 别名配置 {'plugin': 'cdp', 'proxy': 'cdx', 'help': 'ds-help'}
    
    Returns:
        tuple: (success: bool, module_path: Path, error_msg: str)
    """
```

### 使用示例

```python
# 基本使用
directories = {
    'frontend': {'path': 'D:/dev/frontend', 'desc': '前端项目'},
    'backend': {'path': 'D:/dev/backend', 'desc': '后端项目'}
}

aliases = {
    'frontend': 'fe',
    'backend': 'be', 
    'help': 'dev-help'
}

success, module_path, error = create_powershell_module(
    "DevTools", directories, aliases
)
```

## 📚 扩展示例

### 1. 开发工作区模块

```python
# 运行扩展示例
python change_dir/example_extended.py
```

这会创建三种不同的模块：
- **DevWorkspace**: 开发环境 (plugin, proxy, frontend, backend, docs)
- **ProjectNav**: 项目导航 (src, test, build, config) 
- **SystemNav**: 系统工具 (desktop, downloads, documents, temp)

### 2. 配置文件驱动

```python
# 运行配置生成器
python change_dir/config_generator.py
```

支持：
- JSON 配置文件
- INI 配置文件  
- 交互式配置创建

### 3. 自定义扩展

```python
from change_dir.change_plugin_proxy_dir import create_powershell_module

# Git 仓库导航示例
directories = {
    'main': {'path': 'D:/git/main-repo', 'desc': '主仓库'},
    'feature': {'path': 'D:/git/feature-branch', 'desc': '功能分支'},
    'hotfix': {'path': 'D:/git/hotfix', 'desc': '热修复分支'}
}

aliases = {
    'main': 'main',
    'feature': 'feat',
    'hotfix': 'fix',
    'help': 'git-help'
}

success, path, error = create_powershell_module("GitNav", directories, aliases)
```

## 🎯 使用场景

### 开发环境管理
```powershell
# 快速在不同开发目录间切换
fe      # 前端项目
be      # 后端项目  
db      # 数据库脚本
docs    # 文档目录
```

### 项目结构导航
```powershell  
# 项目内部目录快速切换
src     # 源码目录
test    # 测试目录
build   # 构建输出
conf    # 配置文件
```

### 系统目录快速访问
```powershell
# 常用系统目录
desk    # 桌面
dl      # 下载目录
doc     # 文档目录
tmp     # 临时目录
```

## ⚙️ 高级配置

### 永久启用模块

1. **打开 PowerShell 配置文件**：
   ```powershell
   notepad $PROFILE
   ```

2. **添加模块导入**：
   ```powershell
   # 添加到配置文件
   Import-Module DirectorySwitch
   Import-Module DevWorkspace
   Import-Module ProjectNav
   ```

3. **重启 PowerShell** 即可永久使用

### 模块位置

模块会自动安装到：
- **用户目录** (推荐): `%USERPROFILE%\Documents\WindowsPowerShell\Modules\`
- **系统目录**: `%ProgramFiles%\WindowsPowerShell\Modules\`

### 编码处理

工具自动处理：
- UTF-8-sig 编码 (PowerShell 兼容)
- 中文字符支持
- 跨平台路径处理

## 🔍 故障排除

### 常见问题

1. **PowerShell 执行策略错误**：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **模块未找到**：
   ```powershell
   # 检查模块路径
   $env:PSModulePath -split ';'
   
   # 手动导入
   Import-Module "完整路径\DirectorySwitch"
   ```

3. **权限问题**：
   - 工具会优先使用用户目录避免权限问题
   - 如需系统级安装，请以管理员身份运行

### 调试信息

```powershell
# 查看模块信息
Get-Module DirectorySwitch -ListAvailable

# 查看可用命令
Get-Command -Module DirectorySwitch

# 查看别名
Get-Alias | Where-Object Source -eq DirectorySwitch
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境
```bash
# 克隆项目
git clone <repo-url>
cd company-cli

# 安装依赖
pip install click questionary

# 运行测试
python -m change_dir.change_plugin_proxy_dir
```

## 📄 许可证

MIT License

## 🔗 相关链接

- [PowerShell 模块开发文档](https://docs.microsoft.com/powershell/scripting/developer/module/writing-a-windows-powershell-module)
- [Click 框架文档](https://click.palletsprojects.com/)
- [Questionary 交互工具](https://github.com/tmbo/questionary)

---

💡 **提示**: 这个工具的核心理念是"一次配置，到处使用"。通过简单的 Python 配置就能生成强大的 PowerShell 目录切换工具！
