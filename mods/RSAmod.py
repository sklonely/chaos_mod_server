import rsa
import os
import sys


# rsa加密
def rsaEncrypt(str):
    # 生成公钥、私钥
    (pubkey, privkey) = rsa.newkeys(1024)
    print(pubkey, privkey)
    print(type(pubkey))
    # 明文编码格式
    content = str.encode('utf-8')
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return (crypto, privkey)


# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode('utf-8')
    return con


pubkey = 0
privkey = 0
print(os.path.abspath('.'))
with open(os.path.abspath('.') + '\key\public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    print(pubkey)
with open(os.path.abspath('.') + '\key\private.pem') as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    print(type(privkey))

message = 'hello'

print("明文", message)
crypto = rsa.encrypt(message.encode('utf-8'), pubkey)
print("密文", crypto)
message = rsa.decrypt(crypto, privkey).decode('utf-8')
print("明文", message)
