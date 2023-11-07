

# S-AES用户手册

## 目标受众

本开发手册适用于学习AES算法的Python开发人员，帮助他们理解和使用S-AES算法

## 安装和配置

需要基础Python 3.x 环境，无其他特殊安装与配置

## 函数概述

| 函数名称             | 描述                       |
| -------------------- | -------------------------- |
| multi_gf             | GF2^4有限域乘法            |
| expand_key           | 密钥拓展                   |
| encode               | 单16位明文编码             |
| decode               | 单16位密文解码             |
| Unicode_trans_binary | 将Unicode字符转换成二进制  |
| binary_trans_Unicode | 将二进制转换成Unicode字符  |
| hack                 | 中间相遇攻击               |
| plaintext2P          | 长明文分组                 |
| get_C0               | C0获取                     |
| CBC_encode           | 长明文分组编码             |
| CBC_decode           | 长明文分组解码             |
| language2plaintext   | 自然语言生成16*n长度明文串 |
| plaintext2language   | 16*n长度明文串生成自然语言 |

## 类概述

| 类名称       | 描述                  |
| ------------ | --------------------- |
| S_AES_window | 创建用户交互的GUI界面 |

## 各算法描述

| 函数   | multi_gf(x,y , gf=19)                                        |
| :----- | ------------------------------------------------------------ |
| 描述   | GF2^4有限域乘法                                              |
| 参数   | x, y（整数）: 需要计算有限域乘法的两个数<br />gf（整数）：当乘积超过2^4时求余数的不可约多项式权值和 |
| 返回值 | ans（字符串）：四位二进制字符串，表示有限域乘法结果          |
| 示例   | ans = gf_mul(5, 5)<br/>print(f'answer is {ans}')             |

| 函数   | expand_key(round_key, s_box)                                 |
| :----- | ------------------------------------------------------------ |
| 描述   | 密钥拓展                                                     |
| 参数   | round_key（字符串）：十六位二进制轮密钥<br />s_box（4*4二维字符串数组）：可逆替换盒，每个元素为四位二进制字符串 |
| 返回值 | round_key_list（字符串列表）：共三个元素，依次为w0+w1,w2+w3,w4+w5的十六位二进制密码字符串 |
| 示例   | round_key_list = expand_key(round_key, s_box)<br/>print(f"w0={round_key_list\[0][:8]},\nw1={round_key_list\[0][8:]},\n<br />w2={round_key_list\[1][:8]},\nw3={round_key_list\[1][8:]},\n<br />w4={round_key_list\[2][:8]},\nw5={round_key_list\[2][8:]}") |

| 函数   | encode(plain_text, round_key)                                |
| :----- | ------------------------------------------------------------ |
| 描述   | 单16位明文编码                                               |
| 参数   | plain_text（字符串）：需要加密的十六位二进制明文字符串<br />round_key（字符串）：用于加密的十六位二进制密钥字符串 |
| 返回值 | cipher_text（字符串）：加密得到的十六位二进制密文字符串      |
| 示例   | plain_text = '1100100101000111'<br/>round_key='0010110101010101'<br/>cipher_text = encode(plain_text, round_key)<br/>print(f"{plain_text} is encode with {round_key} to {cipher_text}") |

| 函数   | decode(cipher_text, round_key)                               |
| :----- | ------------------------------------------------------------ |
| 描述   | 单16位密文解码                                               |
| 参数   | cipher_text（字符串）：需要解密的十六位二进制明文字符串<br />round_key（字符串）：用于解密的十六位二进制密钥字符串 |
| 返回值 | plain_text（字符串）：解密得到的十六位二进制密文字符串       |
| 示例   | cipher_text = '1010011001111101'<br/>round_key = '0010110101010101'<br/>plain_text_decode = decode(cipher_text, round_key)<br/>print(f"{cipher_text} is decode with {round_key} to {plain_text_decode}") |

| 函数   | Unicode_trans_binary(A_str)                        |
| :----- | -------------------------------------------------- |
| 描述   | 将Unicode字符转换成二进制                          |
| 参数   | A_str（字符串）：在unicode范围内的字符组成的字符串 |
| 返回值 | binary（字符串）：转换得到的16*n长度的二进制字符串 |
| 示例   | print(Unicode_trans_binary("Hello world!"))        |

| 函数   | binary_trans_Unicode(binary)                                 |
| :----- | ------------------------------------------------------------ |
| 描述   | 将二进制转换成Unicode字符                                    |
| 参数   | binary（字符串）：16*n长度的二进制字符串                     |
| 返回值 | A_str（字符串）：转换得到的在unicode范围内的字符组成的字符串 |
| 示例   | print(binary_trans_Unicode("0100101001010010"))              |

| 函数   | hack(plain_text)                                             |
| :----- | ------------------------------------------------------------ |
| 描述   | 对一个或多个已知明、密文对进行中间相遇攻击破解密钥           |
| 参数   | plaintext_group（列表）：已知的明文组<br />ciphertext_group（列表）：已知的密文组 |
| 返回值 | key_group（列表）：攻击后得到的所有密钥                      |
| 示例   | key_group_3 = hack(plaintext_group_3, ciphertext_group_3)<br />print(f"解密得到的密钥数量:{len(key_group_3)}") |

| 函数   | plaintext2P(plain_text)                                      |
| :----- | ------------------------------------------------------------ |
| 描述   | 长明文分组                                                   |
| 参数   | plain_text（字符串）：16*n长度的二进制明文字符串             |
| 返回值 | P（列表）：n个16位长度的分组二进制明文字符串                 |
| 示例   | long_plain_text = ''<br/>for i in range(16):<br/>    temp = bin(i)<br/>    long_plain_text += temp[2:].zfill(4)<br/>P = plaintext2P(plain_text)<br/>for i in range(len(P)):<br/>    print(P[i]) |

| 函数   | get_C0(seed)                                                 |
| :----- | ------------------------------------------------------------ |
| 描述   | C0获取                                                       |
| 参数   | seed（整数）：用于获取随机初始密文C0的种子                   |
| 返回值 | C0（字符串）：根据种子生成十六位长度二进制字符串             |
| 示例   | seed = 2023<br/>C0 = get_C0(seed)<br/>print(f"seed {seed} get {C0}") |

| 函数   | CBC_encode(plain_text, K, C0)                                |
| :----- | ------------------------------------------------------------ |
| 描述   | 长明文分组编码                                               |
| 参数   | plain_text（字符串）：需要加密的16*n长度的二进制明文字符串<br />K（字符串）：用于加密的十六位密钥<br />C0（字符串）：用get_C0获取的初始密文 |
| 返回值 | C（列表）：得到的C1~Cn共n个密文块列表                        |
| 示例   | K = '0010110101010101'<br/>C = CBC_encode(plain_text, K, C0)<br/>print(C) |

| 函数   | CBC_decode(C, K, C0)                                         |
| :----- | ------------------------------------------------------------ |
| 描述   | 长明文分组解码                                               |
| 参数   | C（列表）：需要解密的的C1~Cn共n个密文块列表<br />K（字符串）：用于解密的十六位密钥<br />C0（字符串）：用get_C0获取的初始密文 |
| 返回值 | p（字符串）：解码得到的长明文字符串                          |
| 示例   | K = '0010110101010101'<br/>new_p = CBC_decode(C, K, C0)<br/>print(new_p) |

| 函数   | language2plaintext(language)                          |
| :----- | ----------------------------------------------------- |
| 描述   | 自然语言生成16*n长度明文串                            |
| 参数   | language（字符串）：在unicode范围内的字符组成的字符串 |
| 返回值 | p（字符串）：转换得到的16*n长度的明文二进制字符串     |
| 示例   | print(language2plaintext("Hello world!"))             |

| 函数   | plaintext2language(plain_text)                               |
| :----- | ------------------------------------------------------------ |
| 描述   | 明文串生成自然语言                                           |
| 参数   | plain_text（字符串）：16*n长度的二进制字符串                 |
| 返回值 | p（字符串）：转换得到的在unicode范围内的字符组成的字符串     |
| 示例   | print(plaintext2language(language2plaintext('Hello World!'))) |

| 类   | S_AES_window                                                 |
| ---- | ------------------------------------------------------------ |
| 描述 | 创建用户交互的GUI界面                                        |
| 参数 | ttk.Window()创建的实例                                       |
| 示例 | app = ttk.Window("S-AES加解密器", "superhero", resizable=(False, False)) <br />S_AES_window(app) |