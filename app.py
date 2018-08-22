# 渾沌加密外掛程式(免key的版本
# by sklonely
# import自動修復 程式碼片段Stste
lestModName = ""
while 1:
    try:
        import sys
        import os
        sys.path.append(sys.path[0] + '/mods/')  # 將自己mods的路徑加入倒python lib裡面
        # 要import的東西放這下面
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        from HENMAP_chaos_model import Chaos
        from AESmod import AEScharp
        import PNG_io
        import random
        import json
        import rsa
        import time
        import threading
        import copy
        import hashlib
        from PIL import Image
        import numpy as np
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
app = Flask(__name__)
# 變數
CORS(app)
RSAauth = 0


@app.route("/")
def hello():
    return str("歡迎來到渾沌加解密測試首頁")


@app.route("/RSA_pubkey", methods=['GET'])
def RSA_pubkey():
    global RSAauth
    (pubkey, RSAprivkey) = rsa.newkeys(1024)
    RSAauth = RSAprivkey
    return str(pubkey)


# @app.route("/encrypt", methods=['POST'])
@app.route("/encrypt")
def encrypt():
    temp_Um = Um
    return ("key: " + str(X[0]) + " Um:" + str(temp_Um))


@app.route("/AES_encrypt", methods=['POST'])
def AES_encrypt(data="這是測試用的訊息"):
    # s = time.time()
    # 初始化加密資料
    temp_Um = copy.deepcopy(Um)
    key = copy.deepcopy(X[0])
    aes = AEScharp()
    try:
        dict1 = json.loads(request.get_data())
        data = dict1['data']
        use_key = hashlib.sha256(dict1['key'].encode('utf-8')).digest()
        use_key = list(use_key)
        for i in range(32):
            temp_Um[i] = round(temp_Um[i] + use_key[i], 7)
        # print(temp_Um)
    except:
        return str("err: 資料格式不正確，請確認json格式")
    # 加密資料
    sendData = aes.encrypt_ECB(data, key)
    # json 黨製作
    sendData = {'encrypt_text': str(sendData), 'Um': str(temp_Um)}
    # e = time.time()
    # print(e - s)
    return json.dumps(sendData)


@app.route("/AES_decrypt", methods=['POST'])
def decrypt():
    # 初始化解碼資料
    # s = time.time()
    try:
        # 嘗試
        dict1 = json.loads(request.get_data())
        data = dict1['data']
        data = eval(data)
        temp_Um = dict1['Um']
        temp_Um = temp_Um[1:-1].split(", ")
        use_key = hashlib.sha256(dict1['key'].encode('utf-8')).digest()
        use_key = list(use_key)
        # 加密Um
        for i in range(len(temp_Um)):
            temp_Um[i] = float(temp_Um[i])
            temp_Um[i] -= float(use_key[i])
    except:
        return str("err: 資料格式不正確，請確認json格式")
    # 開始同步
    async_flag = False  # 同步旗標
    times = 0  # 同步失敗次數
    while async_flag is False:

        Y = [random.random(), random.random(), random.random()]
        client = Chaos()
        chck = 0
        for i in range(len(temp_Um) - 1, -1, -1):
            Y = client.runSlave(2, Y, temp_Um[i])
            if i == 1:
                chck = client.createUs(Y)
        # 判斷有沒有同步
        if round(temp_Um[0] + chck, 6):
            # print(temp_X, Y[0], client.createUs(Y), temp_Um[0] + chck)
            async_flag = False
            if times > 12:
                break
            times += 1
            print(round(temp_Um[0] + chck, 6))

        else:
            async_flag = True

    # 解密
    aes = AEScharp()
    getData = aes.decrypt_ECB(data, Y[0])
    # json 檔製作
    getData = {'decrypt_text': str(getData), 'flag': str(async_flag)}
    return json.dumps(getData)


# st type: base64 str
@app.route("/AES_encrypt_png", methods=['POST'])
def AES_encrypt_png():
    # 資料判斷
    dict1 = json.loads(request.get_data())
    st = eval(dict1['data'])
    try:
        img = PNG_io.base64_to_image(st.hex())
        img.save("png/555.png")
        st = PNG_io.image_to_base64(img)
        st = PNG_io.conv(st, 16)
    except TypeError:
        return str("需傳送base64後的圖片檔")

    # 基本圖片判斷
    (W, H) = img.size
    if W % 16 and H % 16:
        return str("圖片寬高必須能被16整除")

    # 開始加密-資料準備階段
    temp_Um = copy.deepcopy(Um)  # Um
    key = copy.deepcopy(X)  # key
    aes = AEScharp()  # aes宣告
    # 開始加密-加密階段
    senddata_hex = ""
    for i in st:
        senddata = aes.encrypt_ECB_by(i, key[0])
        senddata_hex += senddata.hex()

    img_array = []
    for i in bytes.fromhex(senddata_hex):
        img_array.append(i)
    img_array = PNG_io.chunks(img_array, 3)
    img_size = int(len(img_array)**0.5)
    img_array = PNG_io.chunks(img_array, img_size)
    if len(img_array) > img_size:
        img_array = img_array[:img_size]

    img_array = np.array(img_array).astype('uint8')
    im = Image.fromarray(img_array)
    im.save("png/im.png")
    return str(PNG_io.image_to_base64(img))


@app.route("/AES_decrypt_png", methods=['POST'])
def AES_decrypt_png():
    pass


def chaos():
    # 初始化 準備Um buff
    sys_chaos = Chaos()
    global X, Um
    # X = [random.random(), random.random(), random.random()]
    X = [0.1, 0.1, 0.1]
    Um = []
    for i in range(32):
        Um.append(0)
    Um[0] = sys_chaos.createUm(X)
    X = sys_chaos.runMaster(0, X)
    # 進入迴圈開始跑渾沌
    while 1:
        for i in range(31, 0, -1):
            Um[i] = Um[i - 1]
        Um[0] = sys_chaos.createUm(X)
        X = sys_chaos.runMaster(1, X)

        # time.sleep(0.001)


def show(times=50):
    # 測試寒士
    time.sleep(.2)
    x = 0
    for i in range(times):
        AES_encrypt()
        time.sleep(.05)
        if (decrypt()[1]):
            x += 1
            print(i, True)
        else:
            print(i, False)
    print("成功:", x, "失敗:", times - x, "同步率:", (x / times) * 100, "%")


if __name__ == "__main__":
    try:
        # 啟動本機系統的混沌系統
        sys_chaos = threading.Thread(target=chaos)
        sys_chaos.setDaemon(True)
        sys_chaos.start()
        print("SYS_Chaos 初始化完成 進入本機伺服器...")
        # AES_encrypt()
        port = int(os.environ.get('PORT', 5000))
        app.run("0.0.0.0", port)
        # show()
    except:
        print("退出渾沌加密系統")
# host = https://chaos-mod-sever.herokuapp.com/
