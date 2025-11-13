管理工具的界面

设计采用plugins的方式管理每个子功能，降低耦合性

| 功能      | 说明                         |
| :-------- | :--------------------------- |
| Dashboard | 主界面，一些常用简单功能配置 |
| Settings  | 进行一些配置操作             |
|           |                              |

#### Plugin

符合约定的目录都为plugin：一个*_plugin的目录为一个插件，一个plugin包括view（ui逻辑）、view model（业务逻辑处理）、plugin.py(用于配置管理整个插件)

#### Resource

资源通过build_all脚本统一生成。

ui文件：一个plugin目录对应一个ui文件目录（命名相同），ui文件的名称以下划线分隔命令，ui文件里面的最顶层widget使用对应于文件名的大坨峰命名。加*_widget.ui

img, qss, xml文件：目录与plugin目录对应

#### 启动

先执行install.cmd配置环境变量，运行launch.py启动