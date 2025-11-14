# ZengNUI Manage GUI 核心架构与使用教程

## 概览
- 核心以“命令驱动 + 事件驱动”双通道为基础，解耦插件之间以及同一插件内不同功能块（feat）之间的通信。
- 命令通道用于明确的动作触发和跨插件协作，事件通道用于异步广播、松耦合联动和请求-响应。
- 主要组件：`Global`、`PluginManager`、`CommandManager`、`ViewsManager`、`EventBus`、`Context`、`Command`、`CommandContext`。

## 核心组件
- Global
  - 单例，承载全局管理器与总线：`GUI/src/core/app_global.py:12-17, 36-38`
  - 属性：`plugin_manager`、`command_manager`、`views_manager`、`event_bus`
- PluginManager
  - 插件加载与生命周期管理（略）
- CommandManager
  - 命令注册与执行：`GUI/src/core/command_manager.py:15-49`
  - 通过 `cmd(cmd_id)` 或终端名 `execute_command(name)` 执行
- ViewsManager
  - 视图类型注册、实例化、展示、销毁：`GUI/src/core/views_manager.py:16-56, 69-111, 113-122`
  - 复用时返回 `win_id`；模态仅对 `QDialog` 调用 `exec()`；非模态统一 `show()`
  - 视图嵌入：`fill_widget_with_execution` 支持以方法名填充：`GUI/src/core/views_manager.py:124-146`
- EventBus
  - 轻量事件总线，支持订阅、发布、一次性订阅、请求-响应：`GUI/src/core/event_bus.py`
- Context
  - 在启动阶段创建，集成全局总线并提供插件级总线：`GUI/src/core/context.py:4-26`
  - 便捷方法：`on`/`emit`/`ask`；插件内使用 `get_plugin_bus('PluginName')`
- Command
  - 封装命令信息与可调用对象：`GUI/src/core/command.py`
- CommandContext
  - 线程本地存储当前正在装配的插件实例：`GUI/src/core/command_context.py`

## 命令系统
- 定义命令
  - 全局命令（类或静态方法）使用装饰器 `core.cmd(cmd_id, terminal_name)`：
    - 示例：主窗口命令组装 `GUI/src/plugins/main_window_plugin/constructors/main_window/main_window_cmd_handler.py:29-57`
  - 本地命令（实例方法）在 `assembled(context)` 中用 `self.cmd(cmd_id)` 收集并注册，框架自动完成注册：`GUI/src/core/plugin.py:52-73`
- 执行命令
  - 通过 `Global().command_manager.cmd(cmd_id, *args)` 或 `execute_command(terminal_name, *args)` 调用：`GUI/src/core/command_manager.py:27-49`
- 命名规范（建议）
  - 终端名采用 `plugin.feature.action`，示例：`main_window.activate`、`dashboard.activate`
  - `cmd_id` 用 UUID 保证稳定唯一，与终端名映射：`GUI/src/core/command_manager.py:24-26`

## 视图管理
- 注册视图类型
  - 在插件初始化中注册：`GUI/src/plugins/main_window_plugin/main_window_plugin.py:45-54`
- 实例化与复用
  - `win_id = Global().views_manager.instance_view(str(hash(ViewType)), view_model)`：`GUI/src/core/views_manager.py:28-56`
  - 复用逻辑返回已有窗口的 `win_id`，避免把窗口对象误当作 ID 使用
- 展示与关闭
  - `show(win_id)` 统一展示非模态；`exec(win_id)` 仅对 `QDialog` 调用 `exec()`：`GUI/src/core/views_manager.py:69-99`
  - `close(win_id)`/`destroy(win_id)` 按需关闭与销毁
- 视图嵌入
  - `fill_widget_with_execution(outer_win_id, inner_win_id, method_name)` 将内嵌视图以指定方法填充至外部视图：`GUI/src/core/views_manager.py:124-146`

## 事件总线
- 全局事件
  - 订阅：`Global().event_bus.subscribe('ui/theme/toggled', handler)`
  - 发布：`Global().event_bus.publish('ui/theme/toggled', payload)`
  - 请求-响应：`Global().event_bus.request('settings/query', key='theme')`
- 插件内事件
  - 获取插件级总线：`bus = context.get_plugin_bus('MainWindow')`
  - 订阅：`bus.subscribe('menu/selected', handler)`
  - 发布：`bus.publish('menu/selected', pane_id)`
- 主题命名建议
  - 全局：`domain/subdomain/event`，如 `ui/theme/toggled`、`diagnostics/new_message`
  - 插件内：`feat/event`，如 `menu/selected`、`status_bar/progress_update`
  - 请求：动词短语，如 `settings/query`、`project/resolve_path`

## 插件装配与上下文
- 装配阶段
  - 框架在 `assembled(context)` 调用前设置当前插件实例到命令上下文，并为实例保存上下文引用：`GUI/src/core/plugin.py:57-69`
- 启动过程注入总线到上下文
  - 在 `startup` 命令中创建 `Context(Global().event_bus)`，形成共享事件域：`GUI/src/plugins/main_window_plugin/main_window_plugin.py:79`

## 用法示例
- 示例 1：跨插件主题切换
  - 顶部栏触发主题切换（发布事件）：
    ```python
    # TopBarViewModel 或命令处理器中
    from core import Global
    Global().event_bus.publish('ui/theme/toggled', mode='dark')
    ```
  - 设置插件订阅并应用主题：
    ```python
    from core import Global
    def apply_theme(mode=None, **kwargs):
        # 更新样式、刷新视图
        ...
    Global().event_bus.subscribe('ui/theme/toggled', apply_theme)
    ```
- 示例 2：同插件内菜单与面板联动
  - 菜单项选择发布本地事件：
    ```python
    bus = self._context.get_plugin_bus('MainWindow')
    bus.publish('menu/selected', pane_id)
    ```
  - 面板控制器订阅并切换：
    ```python
    bus = self._context.get_plugin_bus('MainWindow')
    bus.subscribe('menu/selected', self.load_pane)
    ```
- 示例 3：命令驱动的窗口激活与嵌入
  - 激活主窗口并装配子视图：`GUI/src/plugins/main_window_plugin/constructors/main_window/main_window_cmd_handler.py:31-57`
  - 顶部栏激活与嵌入：`GUI/src/plugins/main_window_plugin/constructors/top_bar/top_bar_cmd_handler.py:26-36`

## 选择指南：命令 vs 事件
- 使用命令
  - 需要明确执行者与时序且可追踪：窗口打开/关闭、导航跳转、最小化/最大化、注册/激活某视图
- 使用事件
  - 需要广播或松耦合联动：主题变化、诊断消息、数据刷新、状态提示、插件内多面板联动
- 请求-响应事件适用于查询型交互：配置查询、路径解析、状态判定

## 迁移注意事项
- 视图复用返回值统一为 `win_id`，修复了返回窗口对象导致的后续异常：`GUI/src/core/views_manager.py:32-36`
- 非 `QDialog` 模态展示逻辑改为 `show()`，避免调用不存在的 `execNormal`：`GUI/src/core/views_manager.py:96-99`
- 主窗口屏幕变化分支需导入 `QTimer`：`GUI/src/plugins/main_window_plugin/views/main_window_view.py:20`

## 最佳实践
- 为常见系统事件建立统一主题清单（如 `ui/theme/*`, `diagnostics/*`, `navigation/*`），减少歧义
- 在每个插件的 `assembled(context)` 中订阅必要的全局/本地事件，并在命令处理器中发布对应事件
- 命令终端名保持稳定语义，日志通过 `CommandManager` 统一输出，便于排查问题
- 视图嵌入统一使用 `fill_widget_with_execution`，避免直接持有子视图实例带来的耦合

## 参考代码位置
- Global：`GUI/src/core/app_global.py:12-17, 36-38`
- CommandManager：`GUI/src/core/command_manager.py:27-49`
- ViewsManager：`GUI/src/core/views_manager.py:28-56, 69-99, 124-146`
- EventBus：`GUI/src/core/event_bus.py`
- Context：`GUI/src/core/context.py:4-26`
- Plugin 装配：`GUI/src/core/plugin.py:57-69`
- 主窗口命令：`GUI/src/plugins/main_window_plugin/constructors/main_window/main_window_cmd_handler.py:29-57`
- 顶部栏命令：`GUI/src/plugins/main_window_plugin/constructors/top_bar/top_bar_cmd_handler.py:26-36`
