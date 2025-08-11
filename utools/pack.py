# python执行命令行命令
import subprocess
import re

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

print("打包app")
subprocess.run('asar p --unpack-dir "{node_modules/addon,node_modules/leveldown,node_modules/configuration}" ./app ./app.asar', shell=True)

print("获取md5")
result = subprocess.run('openssl dgst -md5 ./app.asar', shell=True, capture_output=True, text=True)
md5_output = result.stdout.strip()
print(md5_output)

# 提取MD5值
md5_match = re.search(r'([a-f0-9]{32})', md5_output)
if md5_match:
    new_md5 = md5_match.group(1)
    print(f"\n提取的MD5值: {new_md5}")
    
    # 显示原始MD5和编码结果
    orig_md5 = "c95bd24c8e6b2454b838bf3afa6b700c"
    print(f"\n原始MD5: {orig_md5}")
    orig_encoded_md5 = encode_utools_md5(orig_md5, 0x3E)
    print("编码后的原始MD5:")
    print(bytes_to_hex_str(orig_encoded_md5[0:16]))
    print(bytes_to_hex_str(orig_encoded_md5[16:32]))
    
    # 编码新的MD5
    encoded_md5 = encode_utools_md5(new_md5, 0x3E)
    print(f"\n新的MD5: {new_md5}")
    print("编码后的新的MD5:")
    print(bytes_to_hex_str(encoded_md5[0:16]))
    print(bytes_to_hex_str(encoded_md5[16:32]))
    
    # 修改win32-x64.node文件中的MD5编码
    node_file_path = "./app.asar.unpacked/node_modules/addon/win32-x64.node"
    try:
        with open(node_file_path, "rb") as f:
            file_data = bytearray(f.read())
        
        # 查找原始编码的位置
        orig_encoded_bytes = bytes(orig_encoded_md5)
        new_encoded_bytes = bytes(encoded_md5)
        
        # 先尝试查找完整的32字节编码
        pos = file_data.find(orig_encoded_bytes)
        if pos != -1:
            file_data[pos:pos+32] = new_encoded_bytes
            
            # 写回文件
            with open(node_file_path, "wb") as f:
                f.write(file_data)
            print(f"\n成功修改 {node_file_path}")
            print(f"在位置 {pos} 处替换了完整的32字节MD5编码")
        else:
            # 尝试分别查找前16字节和后16字节
            orig_first_half = bytes(orig_encoded_md5[0:16])
            orig_second_half = bytes(orig_encoded_md5[16:32])
            new_first_half = bytes(encoded_md5[0:16])
            new_second_half = bytes(encoded_md5[16:32])
            
            pos1 = file_data.find(orig_first_half)
            pos2 = file_data.find(orig_second_half)
            
            replaced = False
            if pos1 != -1:
                file_data[pos1:pos1+16] = new_first_half
                print(f"\n在位置 {pos1} 处替换了前16字节MD5编码")
                replaced = True
            
            if pos2 != -1:
                file_data[pos2:pos2+16] = new_second_half
                print(f"在位置 {pos2} 处替换了后16字节MD5编码")
                replaced = True
            
            if replaced:
                # 写回文件
                with open(node_file_path, "wb") as f:
                    f.write(file_data)
                print(f"成功修改 {node_file_path}")
            else:
                print(f"\n在 {node_file_path} 中未找到原始MD5编码（完整或分段）")
                # 显示文件大小和一些调试信息
                print(f"文件大小: {len(file_data)} 字节")
                print(f"查找的原始编码前16字节: {bytes_to_hex_str(orig_first_half)}")
                print(f"查找的原始编码后16字节: {bytes_to_hex_str(orig_second_half)}")
    except FileNotFoundError:
        print(f"\n文件 {node_file_path} 不存在")
    except Exception as e:
        print(f"\n修改文件时出错: {e}")
else:
    print("无法提取MD5值")


