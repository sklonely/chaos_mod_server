# import自動修復 程式碼片段Stste
lestModName = ""
while 1:
    try:
        import sys
        import os
        sys.path.append(sys.path[0] + '/mods/')  # 將自己mods的路徑加入倒python lib裡面
        # 要import的東西放這下面
        import base64
        from io import BytesIO
        import re
        from AESmod import AEScharp
        # pip3 install pillow
        from PIL import Image
    except (ModuleNotFoundError, ImportError):  # python import error
        err = str(sys.exc_info()[1])[17:-1]
        if (lestModName != err):
            print("缺少mod: " + err + " 正在嘗試進行安裝")
            os.system("pip install " + err)
            lestModName = err
        else:
            print("無法修復import問題 請人工檢查", "mod name: " + err)
            sys.exit()
    else:
        del lestModName
        break


# import自動修復 程式碼片段
# 若img.save()报错 cannot write mode RGBA as JPEG
# 则img = Image.open(image_path).convert('RGB')
def image_to_base64(image_path):
    img = Image.open(image_path).convert('RGB')
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    base64_data = bytes.fromhex(base64_data)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img


def conv(text, lenth):
    new_text = []
    li = 0
    maxl = len(text)
    i = 0

    for i in range(lenth, maxl + 1, lenth):
        new_text.append(text[li:i])
        li = i

    if i != maxl:
        text = text[i:]
        for j in range(lenth - (maxl - i)):
            text += b" "
        new_text.append(text)
    return new_text


aes = AEScharp()
st = image_to_base64('g:/我的云端硬盘/程式/python/chaos_mod_sever/lena.png')
ssst = st
st = conv(st, 16)

TT = ""
TS = ""
# senddata = aes.encrypt_ECB_by(st, "12")
# for i in st:
#     senddata = aes.encrypt_ECB_by(i, "12")
#     TS += senddata.hex()
#     print("圖片密文：", senddata.hex())
#     getdata = aes.decrypt_ECB_by(senddata, "12")
#     TT += getdata.hex()
#     print("圖片明文：", getdata.hex())

# print(i.hex())
print(type(bytes.fromhex(TS)))
print(base64_to_image((eval(str(ssst)).hex())))
print(type(str(ssst)))
print(type(eval(str(ssst))))
