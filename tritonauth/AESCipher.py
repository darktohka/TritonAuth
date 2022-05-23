from Crypto import Random
from Crypto.Cipher import AES
import hashlib, base64

def _pad(s):
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

def getKey(s):
    if len(s) == 32:
        return s

    return hashlib.sha256(s.encode()).digest()

def encrypt(key, raw):
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(getKey(key), AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8'))).decode('utf-8')

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(getKey(key), AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
