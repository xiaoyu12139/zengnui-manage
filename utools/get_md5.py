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
    # 打印新的md5
    orig_md5: str = "2a9c5028f045d57e633e0487f50977ac"
    orig_enc_md5 = encode_utools_md5(orig_md5, 0x3E)
    print("新的MD5：" + orig_md5)
    print("编码后的新的MD5：")
    print(bytes_to_hex_str(orig_enc_md5[0:16]))
    print(bytes_to_hex_str(orig_enc_md5[16:32]))