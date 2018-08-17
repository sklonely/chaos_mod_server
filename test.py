import sys
import os
sys.path.append(sys.path[0] + '/mods/')  # 將自己mods的路徑加入倒python lib裡面
from AESmod import AEScharp
import hashlib
from HENMAP_chaos_model import Chaos
import random
import time
X = [-1.3156345, -1.84, 0.5624]
aes = AEScharp()

Um = 0
Us = 0

sendData = ''
getData = ''

impData = '1111111111111111111111111111111111111111111111111111111111111111111111'
key = hashlib.sha256("dwdwd4".encode('utf-8')).digest()
data = hashlib.sha256(impData.encode('utf-8')).digest()
print(data)
"""
print("key:", key, len(key))
print("data:", data, len(data))
key = list(key)
data = list(data)
print("key:", key, len(key))
print("data:", data, len(data))
key_f = "1234"
"""
errorCount = 0
succsCount = 0
syncCount = 0

a = Chaos()
b = Chaos()


def show_data(X, Y, Um, Us, UK, sendData, getData, j):
    print("Um:", round(Um, 4), "Us:", round(Us, 4), "Uk:", round(UK, 4))
    print("X[" + str(j + 1) + "]", X[0])
    print("Y[" + str(j + 1) + "]", Y[0])
    if (UK == 0):
        print("======同步完成======")
        print("bytes: ", sendData.hex())
        print("sss", bytes.fromhex(sendData.hex()))
        print("org",sendData)
        """
        temp =""
        for i in sendData:
            temp +=hex(i)[2:]
        print(temp)
        """
        print("密文:  ", str(sendData, encoding='utf-8', errors="ignore"))
        print("密文做utf8回來 bytes: ", str(sendData, encoding='utf-8', errors="ignore").encode("utf-8"))
        print("解密文:  ", getData)
        return True
    print("----------------", j, "----------------")


tryy = 1
times = 0.0
MaxTimes = 0

for j in range(tryy):
    Y = [random.random(), random.random(), random.random()]
    for i in range(100):
        UK = a.createUk(X, Y)
        Um = a.createUm(X)
        X = a.runMaster(i, X)
        sendData = aes.encrypt_ECB(impData, 22)
        # print(int(impData.encode('utf-8')))
        Us = b.createUs(Y)
        Y = b.runSlave(i, Y, Um)
        getData = aes.decrypt_ECB(sendData, 22)
        # show data
        if (show_data(X, Y, Um, Us, UK, sendData, getData, j)):
            print("----------------------------------------------")
            print("同步所需次數", i + 1)
            if (MaxTimes <= i):
                MaxTimes = i
            times += (i + 1)
            break
print("平均同步次數:", times / tryy, "最大次數:", MaxTimes)
# a.show()
