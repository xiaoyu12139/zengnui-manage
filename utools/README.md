## 环境

| 描述 | 说明                          |
| :--- | :---------------------------- |
| OS   | Windows 10                    |
| 程序 | uTools v6.1.0                 |
| 工具 | x64dbg, asar, openssl，nodejs |

## 准备工作

搜索下载nvm一键安装https://github.com/coreybutler/nvm-windows/releases

nvm list available 查看nodejs可用版本

nvm install 22.18.0 安装指定版本

nvm list 查看已安装版本

nvm use 22.18.0 使用指定版本

npm install -g @electron/asar --force

asar extract app.asar destination_folder

## 过程

安装utools，然后进入目录C:\Users\xiaoyu\AppData\Local\Programs\utools\resources

备份app.asar.unpacked目录

asar extract app.asar app报错找不到C:\Users\xiaoyu\AppData\Local\Programs\utools\resources\app.asar.unpacked\node_modules\leveldown\deps\leveldb\leveldb-1.20\LICENSE

进入app.asar.unpacked\node_modules目录：npm install leveldown

然后将app.asar.unpacked备份目录下的node_modules/addon粘贴到原来的app.asar.unpacked\node_modules目录下

然后执行asar extract app.asar即可解包成功