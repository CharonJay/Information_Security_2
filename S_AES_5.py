from S_AES import *
import random


# 分组
def plaintext2P(plain_text):
    P = []
    for i in range(len(plain_text) // 16):
        P.append(plain_text[i * 16:i * 16 + 16])
    return P


# 生成随机数
def get_C0(seed):
    random.seed(seed)
    temp = []
    for i in range(4):
        temp.append(random.randint(0, 16))
    C0 = ''
    for i in range(4):
        C0 += bin(temp[i])[2:].zfill(4)
    return C0


# CBC模式加密
def CBC_encode(plain_text, K, C0):
    P = plaintext2P(plain_text)
    C = []
    C.append(C0)
    for i in range(len(P)):
        temp = xor(P[i], C[i])
        temp = encode(temp, K)
        C.append(temp)
    # 删去初始C0
    return C[1:]


# CBC模式解密
def CBC_decode(C, K, C0):
    p = ''
    for i in range(len(C)):
        temp = decode(C[i], K)
        if i == 0:
            temp = xor(C0, temp)
        else:
            temp = xor(C[i - 1], temp)
        p += temp
    return p


# 自然语言转unicode明文串
def language2plaintext(language):
    p = ''
    for i in range(len(language)):
        unicode = ord(language[i])
        bin_text = bin(unicode)[2:]
        p += bin_text.zfill(16)
    return p


# unicode明文串转自然语言
def plaintext2language(plain_text):
    p = ''
    for i in range(len(plain_text) // 16):
        temp = plain_text[i * 16:i * 16 + 16]
        temp = chr(int(temp, 2))
        p += temp
    return p


if __name__ == '__main__':
    # 长明文加解密
    print("----------------------------------长明文加解密----------------------------------")
    plain_text = ''
    for i in range(16):
        temp = bin(i)
        plain_text += temp[2:].zfill(4)

    K = '0010110101010101'
    C0 = get_C0(2023)
    print(f"长明文P = {plain_text}")
    print(f"密钥K = {K}")
    print(f"初始向量C0 = {C0}")

    P = plaintext2P(plain_text)
    C = CBC_encode(plain_text, K, C0)  # 对P进行CBC加密
    cipher_text = ""
    for text in C:
        cipher_text += text
    print(f"加密后得到的密文C = {cipher_text}")
    new_p = CBC_decode(C, K, C0)  # 对加密后得到的C进行CBC解密
    # 打印并测试是否相等
    print(f"解密后得到的明文P = {new_p}")
    print(f"解密后得到的明文与原始明文是否相等: {new_p == plain_text}")
    print("----------------------------------篡改密文分组-----------------------------------")
    # 密文篡改
    attacked_C = []
    for i in range(len(C)):
        attacked_C.append(C[i])
    # 将倒数第二分组中三个二进制位取反
    for i in range(3):
        if attacked_C[2][i] == '1':
            attacked_C[2] = attacked_C[2][:i] + '0' + attacked_C[2][i + 1:]
        else:
            attacked_C[2] = attacked_C[2][:i] + '1' + attacked_C[2][i + 1:]
    attacked_p = CBC_decode(attacked_C, K, C0)
    for i in range(len(plain_text)):
        if attacked_p[i] != plain_text[i]:
            print(f"第{i}位变化")
    print(f"篡改密文前: {plain_text}")
    print(f"篡改密文后: {attacked_p}")

    # 不定长文字加密总流程
    long_plain_text = language2plaintext('Hello World!')
    K = '0010110101010101'
    C0 = get_C0(20231106)
    C = CBC_encode(long_plain_text, K, C0)
    new_plain_text = CBC_decode(C, K, C0)
    plaintext2language(new_plain_text)
