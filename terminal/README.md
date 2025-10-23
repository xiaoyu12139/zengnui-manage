python使用click实现的cmd命令行操作
python版本dev：3.12.7
安装，cd到当前目录后：pip install -e .

考虑兼容：cmd,powershell

| 功能          | 说明                                                         | 支持终端         |
| :------------ | :----------------------------------------------------------- | ---------------- |
| change_dir    | 通过配置文件设置命令行，使得通过别名方式快速切换当前命令行窗口所在的目录 | ps/cmd//git bash |
|               | update-change-dir: 命令行执行, 更新设置配置文件中的配置      |                  |
|               | config.json：修改添加相关的配置，执行update-change-dir生效   |                  |
| clash         | 在命令行快速开启关闭终端clash代理                            | ps/cmd/git bash  |
|               | update-clash-proxy: 命令行执行，更新加载proxy-on/off的代理配置 |                  |
|               | proxy-on/off: 命令行执行，在当前终端开启/关闭clash的代理     |                  |
| command_alias | 为ps/cmd/git bash的命令别名，用于对当前所在终端进行一些修改操作 |                  |
|               | alias -p -s [cmd \| ps \| bash] ：打印指定终端别名相关配置   |                  |
|               | alias -d -s [cmd \| ps \| bash] : 删除指定终端别名相关配置   | bashps           |
|               | clear-all-alias: 删除所有终端别名相关配置                    |                  |

> 对涉及别名操作的功能，如果频繁操作修改导致配置文件紊乱的，建议清楚所有的终端别名配置后，在对应功能进行update, 后续考虑加载一键update的所有设置别名操作的功能
