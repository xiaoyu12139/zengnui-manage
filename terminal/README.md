python使用click实现的cmd命令行操作
python版本dev：3.12.7
安装，cd到当前目录后：pip install -e .

考虑兼容：cmd,powershell

| 功能        | 说明                                                         | 支持终端        |
| :---------- | :----------------------------------------------------------- | --------------- |
| change-dir  | 通过配置文件设置命令行，使得通过别名方式快速切换当前命令行窗口所在的目录<br />命令行执行update-change-dir更新设置配置文件中的配置 | ps/cmd          |
| clash-proxy | 在命令行快速开启关闭终端clash代理                            | ps/cmd/git bash |
|             |                                                              |                 |

