# Windows 文件监控服务

这是一个基于Python的Windows服务程序，用于监控指定文件夹中的文件变化，包括文件的创建、删除、修改和移动操作。

## 功能特性

- 🔍 **实时监控**: 监控指定文件夹中的所有文件变化
- 📁 **递归监控**: 支持监控子文件夹中的文件变化
- 🔄 **多种事件**: 监控文件创建、删除、修改、移动等操作
- 🪟 **Windows服务**: 可作为Windows系统服务运行
- 📝 **日志记录**: 详细的日志记录，便于调试和监控
- 🛠️ **调试模式**: 支持调试模式，便于开发和测试

## 安装依赖

在运行服务之前，请先安装所需的Python依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：使用批处理脚本（推荐）

1. **以管理员身份**运行 `service_manager.bat`
2. 根据菜单提示选择相应操作：
   - `1` - 安装服务
   - `2` - 启动服务
   - `3` - 停止服务
   - `4` - 卸载服务
   - `5` - 查看服务状态
   - `6` - 以调试模式运行

### 方法二：使用命令行

#### 调试模式运行
```bash
python main.py
```

#### 安装为Windows服务
```bash
# 安装服务（需要管理员权限）
python main.py install

# 启动服务
python main.py start

# 停止服务
python main.py stop

# 卸载服务
python main.py remove
```

## 配置说明

### 监控文件夹配置

在 `main.py` 文件中，可以修改以下配置：

```python
# 在 FileMonitorService 类的 __init__ 方法中
self.watch_folder = r"C:\Users\xiaoyu\Desktop\Code\zengnui-manage\utools"

# 在 main 函数中（调试模式）
watch_folder = r"C:\Users\xiaoyu\Desktop\Code\zengnui-manage\utools"
```

### 自定义处理逻辑

在 `FileChangeHandler` 类的 `handle_file_change` 方法中添加你的业务逻辑：

```python
def handle_file_change(self, action, src_path, dest_path=None):
    """处理文件变化事件"""
    try:
        if action == 'created':
            # 添加文件创建后的处理逻辑
            pass
            
        elif action == 'deleted':
            # 添加文件删除后的处理逻辑
            pass
            
        elif action == 'modified':
            # 添加文件修改后的处理逻辑
            pass
            
        elif action == 'moved':
            # 添加文件移动后的处理逻辑
            pass
            
    except Exception as e:
        logger.error(f"处理文件变化事件时出错: {e}")
```

## 日志文件

服务运行时会生成日志文件 `file_monitor_service.log`，记录所有的文件变化事件和服务状态。

## 注意事项

1. **管理员权限**: 安装、启动、停止Windows服务需要管理员权限
2. **文件夹路径**: 确保监控的文件夹路径存在且可访问
3. **性能考虑**: 监控大量文件时可能会影响系统性能
4. **防火墙**: 如果需要网络通信，请确保防火墙设置正确

## 故障排除

### 服务安装失败
- 确保以管理员身份运行命令
- 检查Python环境是否正确配置
- 确保所有依赖包已正确安装

### 服务启动失败
- 检查监控文件夹路径是否存在
- 查看日志文件中的错误信息
- 确保没有其他程序占用相同的服务名称

### 文件变化未被检测到
- 确认文件确实发生了变化
- 检查文件是否在监控文件夹范围内
- 查看日志文件确认服务是否正常运行

## 开发说明

### 项目结构
```
server/
├── main.py              # 主程序文件
├── requirements.txt     # Python依赖包
├── service_manager.bat  # 服务管理脚本
├── README.md           # 说明文档
└── file_monitor_service.log  # 日志文件（运行时生成）
```

### 扩展功能

可以根据需要扩展以下功能：
- 添加邮件通知
- 集成数据库记录
- 添加Web界面监控
- 支持多文件夹监控
- 添加文件过滤规则

## 许可证

本项目采用 MIT 许可证。