from S_AES import *
import time


# 中间相遇攻击
def hack(plaintext_group, ciphertext_group):
    # 重置密钥
    Key1 = "0000000000000000"
    Key2 = "0000000000000000"
    # 密钥空间
    fre = 2 ** len(Key1)
    key_group = []
    plaintext_dic = {}
    ciphertext_dic = {}

    for i in range(fre):
        middle_text_encode = encode(plaintext_group[0], Key1)
        if middle_text_encode in plaintext_dic:
            plaintext_dic[middle_text_encode].append(Key1)
        else:
            plaintext_dic[middle_text_encode] = [Key1]
        # 将二进制字符串转换为整数
        Key1_int = int(Key1, 2)
        Key1_int += 1
        # 将结果转换回二进制字符串并保持固定长度
        Key1 = format(Key1_int, '016b')

        middle_text_decode = decode(ciphertext_group[0], Key2)
        if middle_text_decode in ciphertext_dic:
            ciphertext_dic[middle_text_decode].append(Key2)
        else:
            ciphertext_dic[middle_text_decode] = [Key2]
        # 将二进制字符串转换为整数
        Key2_int = int(Key2, 2)
        Key2_int += 1
        # 将结果转换回二进制字符串并保持固定长度
        Key2 = format(Key2_int, '016b')

    # 遍历第一个字典的键
    for key in plaintext_dic:
        # 检查第二个字典是否有相同的键
        if key in ciphertext_dic:
            for K1 in plaintext_dic[key]:
                for K2 in ciphertext_dic[key]:
                    flag = 0
                    for i in range(len(plaintext_group)):
                        middle_text_encode = encode(plaintext_group[i], K1)
                        middle_text_decode = decode(ciphertext_group[i], K2)
                        if middle_text_encode != middle_text_decode:
                            flag = 1
                            break
                    if flag == 0:
                        key_group.append([K1, K2])

    return key_group


if __name__ == '__main__':
    plaintext1 = "1100100101000111"
    ciphertext1 = "1001010011000101"

    plaintext2 = "1110100010010111"
    ciphertext2 = "1011011110100110"

    plaintext3 = "0101101101100101"
    ciphertext3 = "0111110001000111"

    Key_1 = "0010110101010101"
    Key_2 = "0101011010101001"
    print(f"原始密钥对{[Key_1, Key_2]}")

    plaintext_group_1 = [plaintext1]
    ciphertext_group_1 = [ciphertext1]

    plaintext_group_2 = [plaintext1, plaintext2]
    ciphertext_group_2 = [ciphertext1, ciphertext2]

    plaintext_group_3 = [plaintext1, plaintext2, plaintext3]
    ciphertext_group_3 = [ciphertext1, ciphertext2, ciphertext3]

    # 得到一对明密文对时，进行交叉攻击
    print("------------------------------------------得到一对明密文对时，进行交叉攻击------------------------------------------")
    time_start_1 = time.time()
    key_group_1 = hack(plaintext_group_1, ciphertext_group_1)
    time_end_1 = time.time()
    print(key_group_1)
    print(f"解密得到的密钥数量:{len(key_group_1)}, 共用时:{time_end_1 - time_start_1}s")

    # 得到两对明密文对时，进行交叉攻击
    print("------------------------------------------得到两对明密文对时，进行交叉攻击------------------------------------------")
    time_start_2 = time.time()
    key_group_2 = hack(plaintext_group_2, ciphertext_group_2)
    time_end_2 = time.time()
    print(key_group_2)
    print(f"解密得到的密钥数量:{len(key_group_2)}, 共用时:{time_end_2 - time_start_2}s")

    # 得到三对明密文对时，进行交叉攻击
    print("------------------------------------------得到三对明密文对时，进行交叉攻击------------------------------------------")
    time_start_3 = time.time()
    key_group_3 = hack(plaintext_group_3, ciphertext_group_3)
    time_end_3 = time.time()
    print(key_group_3)
    print(f"解密得到的密钥数量:{len(key_group_3)}, 共用时:{time_end_3 - time_start_3}s")