import binascii, base64, hashlib, hmac, time, struct

def sha1_hash(data):
    return hashlib.sha1(data).digest()

def hmac_sha1(secret, data):
    return hmac.new(secret, data, hashlib.sha1).digest()

def generateDeviceId(steamId):
    h = binascii.hexlify(sha1_hash(str(steamId).encode('ascii'))).decode('ascii')

    return "android:%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:32])

def generateCode(secret):
    try:
        secret = base64.b64decode(secret)
    except:
        pass

    hmac = hmac_sha1(bytes(secret), struct.pack('>Q', int(time.time()) // 30))
    start = ord(hmac[19:20]) & 0xF
    codeInt = struct.unpack('>I', hmac[start:start+4])[0] & 0x7fffffff

    charset = '23456789BCDFGHJKMNPQRTVWXY'
    code = ''

    for _ in range(5):
        codeInt, i = divmod(codeInt, len(charset))
        code += charset[i]

    return code