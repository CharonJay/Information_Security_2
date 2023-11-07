import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import re


# 异或加
def xor(x, y):
    ans = ''
    for i, j in zip(x, y):
        if i == j:
            ans += '0'
        else:
            ans += '1'
    return ans


# GF域基础相乘
def gf_mul(x, y):
    if x == 0 or y == 0:
        return '0000'
    x = bin(x)[2:]
    y = bin(y)[2:]
    y = y[::-1]
    mul_list = []
    for i, y_i in enumerate(y):
        if y_i == '1':
            temp = x.zfill(len(x) + len(y) - 1 - i)
            temp = temp[::-1]
            temp = temp.zfill(len(x) + len(y) - 1)
            temp = temp[::-1]
            mul_list.append(temp)
    mul = mul_list[0]
    for i in range(len(mul_list) - 1):
        mul = xor(mul, mul_list[i + 1])
    mul = mul.lstrip('0')
    return mul


# GF域取余
def gf_mod(mul, gf=19):
    gf = bin(gf)[2:]
    while len(mul) >= len(gf):
        temp = mul[:len(gf)]
        ans = xor(temp, gf).lstrip('0')
        mul = ans + mul[len(gf):]
    return mul.zfill(4)


def multi_gf(x, y, gf=19):
    mul = gf_mul(x, y)
    ans = gf_mod(mul, gf)
    return ans


# 密钥加
def Ak(state_matrix, round_key):
    new_metrix = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            new_metrix[i][j] = xor(state_matrix[i][j], round_key[i][j])
    return new_metrix


s_box = [['1001', '0100', '1010', '1011'],
         ['1101', '0001', '1000', '0101'],
         ['0110', '0010', '0000', '0011'],
         ['1100', '1110', '1111', '0111']]

inv_s_box = [['1010', '0101', '1001', '1011'],
             ['0001', '0111', '1000', '1111'],
             ['0110', '0000', '0010', '0011'],
             ['1100', '0100', '1101', '1110']]


# 半字节代替
def NS(state_matrix, s_box):
    new_metrix = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            temp = state_matrix[i][j]
            new_metrix[i][j] = s_box[int(temp[:2], 2)][int(temp[2:], 2)]
    return new_metrix


# 行移位
def SP(state_matrix):
    new_metrix = [[state_matrix[0][0], state_matrix[0][1]], [
        state_matrix[1][1], state_matrix[1][0]]]
    return new_metrix


# 列混淆
def MC(state_matrix, confuse_matrix):
    temp = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            temp[i][j] = int(state_matrix[i][j], 2)
    new_metrix = [[
        xor(multi_gf(confuse_matrix[0][0], temp[0][0]), multi_gf(confuse_matrix[0][1], temp[1][0])),
        xor(multi_gf(confuse_matrix[0][0], temp[0][1]), multi_gf(confuse_matrix[0][1], temp[1][1]))
    ],
        [
            xor(multi_gf(confuse_matrix[1][0], temp[0][0]), multi_gf(confuse_matrix[1][1], temp[1][0])),
            xor(multi_gf(confuse_matrix[1][0], temp[0][1]), multi_gf(confuse_matrix[1][1], temp[1][1]))
        ]]
    return new_metrix


# 函数g
def g(w, i, s_box):
    N0, N1 = w[:4], w[4:]
    N1 = s_box[int(N1[:2], 2)][int(N1[2:], 2)]
    N0 = s_box[int(N0[:2], 2)][int(N0[2:], 2)]
    xn = '1'.zfill(i + 3)
    xn = gf_mod(xn[::-1]) + '0000'
    w = xor(N1 + N0, xn)
    return w


# 密钥扩展
def expand_key(round_key, s_box):
    round_key_list = []
    w0, w1 = round_key[:8], round_key[8:]
    i = 1
    w2 = xor(w0, g(w1, i, s_box))
    w3 = xor(w2, w1)
    i = 2
    w4 = xor(w2, g(w3, i, s_box))
    w5 = xor(w4, w3)
    round_key_list.append(w0 + w1)
    round_key_list.append(w2 + w3)
    round_key_list.append(w4 + w5)
    return round_key_list


# 加密
def encode(plain_text, round_key):
    s_box = [['1001', '0100', '1010', '1011'],
             ['1101', '0001', '1000', '0101'],
             ['0110', '0010', '0000', '0011'],
             ['1100', '1110', '1111', '0111']]

    confuse_matrix = [[1, 4], [4, 1]]

    state_matrix = [[plain_text[:4], plain_text[8:12]], [plain_text[4:8], plain_text[12:]]]
    round_key_list = expand_key(round_key, s_box)

    k0, k1, k2 = round_key_list[0], round_key_list[1], round_key_list[2]
    k0 = [[k0[:4], k0[8:12]], [k0[4:8], k0[12:]]]
    k1 = [[k1[:4], k1[8:12]], [k1[4:8], k1[12:]]]
    k2 = [[k2[:4], k2[8:12]], [k2[4:8], k2[12:]]]

    # 轮密钥加
    state_matrix = Ak(state_matrix, k0)

    # ==========第一轮==========

    # 半字节代替
    state_matrix = NS(state_matrix, s_box)

    # 行位移
    state_matrix = SP(state_matrix)

    # 列混淆
    state_matrix = MC(state_matrix, confuse_matrix)

    # 轮密钥加
    state_matrix = Ak(state_matrix, k1)

    # ==========第二轮==========

    # 半字节代替
    state_matrix = NS(state_matrix, s_box)

    # 行位移
    state_matrix = SP(state_matrix)

    # 轮密钥加
    state_matrix = Ak(state_matrix, k2)

    cipher_text = state_matrix[0][0] + state_matrix[1][0] + state_matrix[0][1] + state_matrix[1][1]
    return cipher_text


# 解密
def decode(cipher_text, round_key):
    state_matrix = [[cipher_text[:4], cipher_text[8:12]], [cipher_text[4:8], cipher_text[12:]]]
    round_key_list = expand_key(round_key, s_box)

    k0, k1, k2 = round_key_list[0], round_key_list[1], round_key_list[2]
    k0 = [[k0[:4], k0[8:12]], [k0[4:8], k0[12:]]]
    k1 = [[k1[:4], k1[8:12]], [k1[4:8], k1[12:]]]
    k2 = [[k2[:4], k2[8:12]], [k2[4:8], k2[12:]]]

    inv_s_box = [['1010', '0101', '1001', '1011'],
                 ['0001', '0111', '1000', '1111'],
                 ['0110', '0000', '0010', '0011'],
                 ['1100', '0100', '1101', '1110']]

    inv_confuse_matrix = [[9, 2], [2, 9]]

    # 轮密钥加
    state_matrix = Ak(state_matrix, k2)

    # ==========第一轮==========

    # 逆行位移
    state_matrix = SP(state_matrix)

    # 逆半字节代替
    state_matrix = NS(state_matrix, inv_s_box)

    # 轮密钥加
    state_matrix = Ak(state_matrix, k1)

    # 逆列混淆
    state_matrix = MC(state_matrix, inv_confuse_matrix)

    # ==========第二轮==========

    # 逆行位移
    state_matrix = SP(state_matrix)

    # 逆半字节代替
    state_matrix = NS(state_matrix, inv_s_box)

    # 轮密钥加
    state_matrix = Ak(state_matrix, k0)

    plain_text = state_matrix[0][0] + state_matrix[1][0] + state_matrix[0][1] + state_matrix[1][1]
    return plain_text


# 将Unicode字符转换成二进制
def Unicode_trans_binary(A_str):
    binary = ''
    for c in A_str:
        c_int = ord(c)
        c_binary = format(c_int, '016b')
        binary = ' '.join([binary, c_binary])
    return binary


# 将二进制转换成Unicode
def binary_trans_Unicode(binary):
    binary_bytes = binary.split()
    A_characters = [chr(int(x, 2)) for x in binary_bytes]
    A_str = ''.join(A_characters)
    return A_str


# 窗口类
class S_AES_window(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.num = 0
        # 输入框
        self.plain_text = ttk.StringVar(value="")
        self.cipher_text = ttk.StringVar(value="")
        self.key = ttk.StringVar(value="")
        # 文本信息
        hdr_txt = "请输入明文与密钥获取密文，或输入密文与密钥获取明文"
        hdr = ttk.Label(master=self, text=hdr_txt, width=100)
        hdr.pack(fill=X, pady=10)
        # 组合文本
        self.create_form_entry("明文", self.plain_text)
        self.create_form_entry("密文", self.cipher_text)
        self.create_form_entry("密钥", self.key)
        result_txt = " "
        self.result_label = ttk.Label(master=self, text=result_txt, width=100)
        self.result_label.pack(fill=X, pady=10)
        self.iv_default = ttk.IntVar()
        self.create_radiobuttonbox()
        self.create_buttonbox()

    # 创建组合容器
    def create_form_entry(self, label, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)
        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # 创建单选框
    def create_radiobuttonbox(self):
        """Create the application radiobuttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        rb_default = ttk.Radiobutton(master=container, text='原始加密', command=self.change_num, value=1,
                                     variable=self.iv_default)
        rb_default.pack(side=RIGHT, padx=5)
        rb_default.focus_set()
        rb_double = ttk.Radiobutton(master=container, text='双重加密', command=self.change_num, value=2,
                                    variable=self.iv_default)
        rb_double.pack(side=RIGHT, padx=5)
        rb_double.focus_set()
        rb_triple = ttk.Radiobutton(master=container, text='三重加密', command=self.change_num, value=3,
                                    variable=self.iv_default)
        rb_triple.pack(side=RIGHT, padx=5)
        rb_triple.focus_set()
        self.iv_default.set(1)

    # 创建按钮
    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        sub_btn = ttk.Button(master=container, text="加密", command=self.act_encode, bootstyle=SUCCESS, width=6)
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()
        cnl_btn = ttk.Button(master=container, text="解密", command=self.act_decode, bootstyle=DANGER, width=6)
        cnl_btn.pack(side=RIGHT, padx=5)

    # 更换num值
    def change_num(self):
        value = self.iv_default.get()
        print(value)
        if value == 1:
            self.num = 0
        elif value == 2:
            self.num = 1
        else:
            self.num = 2

    # 与按钮组件绑定的加密操作
    def act_encode(self):
        try:
            plain_str = self.plain_text.get()
            key_str = self.key.get()
            if plain_str == "" and key_str == "":  # 当明文或密钥未输入时扔出异常
                raise Exception('明文或密钥未输入')
            key_list = ['无', '无', '无']
            key_index = 0
            while len(key_str) / 16 != 0:
                key = key_str[:16]
                key_str = key_str[16:]
                key_list[key_index] = key
                key_index += 1
            if key_index - 1 != self.num:  # 当密钥格式不对时扔出异常
                raise Exception('密钥格式错误')
            if bool(re.match('^[01]*$', plain_str)) and len(plain_str) == 16:  # 如果输入是十六位二进制字符串, 则直接进行加密操作
                ciper_text_str = encode(plain_str, key_list[0])
                # 多重加密
                for i in range(self.num):
                    ciper_text_str = encode(ciper_text_str, key_list[i + 1])
                self.result_label[
                    'text'] = f"加密结果: {ciper_text_str},已复制在密文框中, KEY1={key_list[0]}, KEY2={key_list[1]}, KEY3={key_list[2]}"  # 将结果显示在GUI界面上
                self.cipher_text.set(ciper_text_str)  # 将结果复制在密文框中
            else:  # 如果输入不是，则先进行Unicode转码
                P_binary = Unicode_trans_binary(plain_str)
                P_binary_list = P_binary.split()
                ciper_text_binary = ""
                for P in P_binary_list:
                    ciper_text_binary = ' '.join([ciper_text_binary, encode(P, key_list[0])])
                ciper_text_str = binary_trans_Unicode(ciper_text_binary)
                # 多重加密
                for i in range(self.num):
                    C_binary = Unicode_trans_binary(ciper_text_str)
                    C_binary_list = C_binary.split()
                    ciper_text_binary = ""
                    for C in C_binary_list:
                        ciper_text_binary = ' '.join([ciper_text_binary, encode(C, key_list[i + 1])])
                    ciper_text_str = binary_trans_Unicode(ciper_text_binary)
                self.result_label[
                    'text'] = f"加密结果: {ciper_text_str},已复制在密文框中, KEY1={key_list[0]}, KEY2={key_list[1]}, KEY3={key_list[2]}"  # 将结果显示在GUI界面上
                self.cipher_text.set(ciper_text_str)  # 将结果复制在密文框中
        except:
            messagebox.showerror(title="错误", message="请检查明密文和密钥是否正确输入!")

    # 与按钮组件绑定的解密操作
    def act_decode(self):
        try:
            cipher_str = self.cipher_text.get()
            key_str = self.key.get()
            key_list = ['无', '无', '无']
            key_index = 0
            if cipher_str == "" and key_str == "":  # 当密文或密钥未输入时扔出异常
                raise Exception('密文或密钥未输入')
            while len(key_str) / 16 != 0:
                key = key_str[:16]
                key_str = key_str[16:]
                key_list[key_index] = key
                key_index += 1
            if key_index - 1 != self.num:  # 当密钥格式不对时扔出异常
                raise Exception('密钥格式错误')
            if bool(re.match('^[01]*$', cipher_str)) and len(cipher_str) == 16:  # 如果输入是十六位二进制字符串, 则直接进行解密操作
                plain_text_str = decode(cipher_str, key_list[key_index - 1])
                # 多重解密
                for i in range(self.num):
                    plain_text_str = decode(plain_text_str, key_list[key_index - i - 2])
                self.result_label[
                    'text'] = f"解密结果: {plain_text_str},已复制在明文框中, KEY1={key_list[0]}, KEY2={key_list[1]}, KEY3={key_list[2]}"  # 将结果显示在GUI界面上
                self.plain_text.set(plain_text_str)  # 将结果复制在明文框中
            else:  # 如果输入不是，则先进行Unicode转码
                C_binary = Unicode_trans_binary(cipher_str)
                C_binary_list = C_binary.split()
                plain_text_binary = ""
                for C in C_binary_list:
                    plain_text_binary = ' '.join([plain_text_binary, decode(C, key_list[key_index - 1])])
                plain_text_str = binary_trans_Unicode(plain_text_binary)
                # 多重解密
                for i in range(self.num):
                    P_binary = Unicode_trans_binary(plain_text_str)
                    P_binary_list = P_binary.split()
                    plain_text_binary = ""
                    for P in P_binary_list:
                        plain_text_binary = ' '.join([plain_text_binary, decode(P, key_list[key_index - i - 2])])
                    plain_text_str = binary_trans_Unicode(plain_text_binary)
                self.result_label[
                    'text'] = f"解密结果: {plain_text_str},已复制在明文框中, KEY1={key_list[0]}, KEY2={key_list[1]}, KEY3={key_list[2]}"  # 将结果显示在GUI界面上
                self.plain_text.set(plain_text_str)  # 将结果复制在明文框中
        except:
            messagebox.showerror(title="错误", message="请检查明密文和密钥是否正确输入!")


if __name__ == "__main__":
    # plain_text = '1100100101000111'
    # round_key1 = '0010110101010101'
    # round_key2 = '00101101010101010101011010101001'
    # round_key3 = '001011010101010110101000101001011010100110110101'

    app = ttk.Window("S-AES加解密器", "superhero", resizable=(False, False))
    S_AES_window(app)
    app.mainloop()
