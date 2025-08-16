## 环境

| 描述 | 说明                          |
| :--- | :---------------------------- |
| OS   | Windows 10                    |
| 程序 | uTools v6.1.0                 |
| 工具 | x64dbg, asar, openssl，nodejs |

教程：

https://www.52pojie.cn/thread-2003165-1-1.html

https://www.52pojie.cn/thread-1910115-1-1.html

## 准备工作

搜索下载nvm一键安装https://github.com/coreybutler/nvm-windows/releases

nvm list available 查看nodejs可用版本

nvm install 22.18.0 安装指定版本

nvm list 查看已安装版本

nvm use 22.18.0 使用指定版本

npm install -g @electron/asar --force

asar extract app.asar destination_folder

## 解包过程

安装utools，然后进入目录C:\Users\xiaoyu\AppData\Local\Programs\utools\resources

备份app.asar.unpacked目录

asar extract app.asar app报错找不到C:\Users\xiaoyu\AppData\Local\Programs\utools\resources\app.asar.unpacked\node_modules\leveldown\deps\leveldb\leveldb-1.20\LICENSE

进入app.asar.unpacked\node_modules目录：npm install leveldown

然后将app.asar.unpacked备份目录下的node_modules/addon粘贴到原来的app.asar.unpacked\node_modules目录下

然后执行asar extract app.asar即可解包成功

## 修改源码破解

vscode搜索`getUser: (e) => { `定位到main.js文件中

注释这个函数中的内容，修改为：

```
getUser: (e) => {
    // const t = this.accountCmp.getAccountInfo();
    // if (t)
    //   return U()
    //     ? (this.accountCmp.pingAccessTokenValid(),
    //       void (t.extend
    //         ? (e.returnValue = { avatar: t.avatar, ...t.extend })
    //         : (e.returnValue = {
    //             avatar: t.avatar,
    //             nickname: t.nickname,
    //           })))
    //     : void (e.returnValue = {
    //         avatar: t.avatar,
    //         nickname: t.nickname,
    //         type: 1 === t.type ? "member" : "user",
    //       });
    // e.returnValue = null;
    e.returnValue = 1;
  },
```

搜索`isPurchasedUser: (e, t) => {`定位修改为

```
isPurchasedUser: (e, t) => {
            // const i = this.accountCmp.getAccountInfo();
            // if (i) {
            //   if (
            //     (t.startsWith("dev_") && (t = t.replace("dev_", "")),
            //     i.purchased_apps)
            //   ) {
            //     const n = i.purchased_apps[t];
            //     if (!n) return void (e.returnValue = !1);
            //     if (!0 === n) return void (e.returnValue = !0);
            //     if (new Date(n) > new Date()) return void (e.returnValue = n);
            //   } else if (
            //     i.purchased &&
            //     Array.isArray(i.purchased) &&
            //     i.purchased.includes(t)
            //   )
            //     return void (e.returnValue = !0);
            //   e.returnValue = !1;
            // } else e.returnValue = !1;
            e.returnValue = 1;
          },
```

## 打包

将修改后的app解包文件打包成asar文件

asar p --unpack-dir "{node_modules\addon,node_modules\leveldown,node_modules\configuration}" .\app\ .\app.asar

替换md5

openssl dgst -md5 .\app.asar 

将得到的md5替换 `win32-x64.node` 里的值, 用 ida 也可以用其他 hex 编辑器替换

这里使用上面吾爱破解的python文件查看老的md5和新的md5的16进值

```
def bytes_to_hex_str(bs: bytes) -> str:
    # 将bytes转成16进制表示的字符串，方便查看和patch进文件
    return " ".join([f"{b:0{2}X}" for b in bs])

def decode_utools_md5(enc_md5: list, start_byte: int) -> list:
    # 复刻 win32-x64.node 中的解码
    # 异或
    dec_md5 = enc_md5
    for i in range(32):
        dec_md5[i] = dec_md5[i] ^ start_byte
        start_byte = start_byte + 1
    return dec_md5

def encode_utools_md5(md5: str, start_byte: int) -> list:
    # 把MD5编码回去，方便进行 patch
    # 根据异或的特性，其实就是再异或一次，写个函数方便调用而已
    enc_md5: list = list(bytes(md5.lower(), encoding="ascii"))  # str转 int list
    return decode_utools_md5(enc_md5, start_byte)

if __name__ == "__main__":
    # 先把原来的MD5编码出来看看
    orig_md5: str = "c95bd24c8e6b2454b838bf3afa6b700c"
    orig_enc_md5 = encode_utools_md5(orig_md5, 0x3E)
    print("原始MD5：" + orig_md5)
    print("编码后的原始MD5：")
    print(bytes_to_hex_str(orig_enc_md5[0:16]))
    print(bytes_to_hex_str(orig_enc_md5[16:32]))
```

修改win32-x64.node，这个文件在打包后会出现在app.asar同级目录下的app.asar.unpacked中

这里在vscode安装hex editor插件，双击打开，点击open anyway选择hex编辑器，然后搜索对应的16进制进行替换即可（直接搜索的是16进制解码得到的文本，所以我们需要搜索md5的16进制转成文本后的字符串）

> 注意：搜索只能一行一行搜索。也就是说我转换的字节的一行要和编辑器打开显示的一行的字节数要对上

16进制转字符串网站：

https://www.bejson.com/convert/ox2str/

查看后发现只有一个匹配的，所以可以直接在代码中进行搜索替换

然后将得到的app.asar和app.asar.unpacked文件替换原来的目录下的文件和文件夹即可正常使用utools

## 更新搜索框的占位符

修改C:\Users\xiaoyu\AppData\Local\Programs\utools\resources\app.asar.unpacked\node_modules\configuration\index.js

文件中的placeholder即可修改utools搜索框的占位符

修改 newestVersionURL 即可修改新版本的url文件

## 修改添加 添加本地快捷方式的api接口

修改的代码在main.json中

以 `自定义添加 start`注释行标记
