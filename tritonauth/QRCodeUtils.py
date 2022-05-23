
from PySide6.QtGui import QImage
from PIL import Image
import zxingcpp, pyotp
import base64

def convertQtImageToPillow(image: QImage):
    return Image.frombuffer('RGBA', (image.width(), image.height()), image.constBits(), 'raw', 'RGBA', 0, 1)

def isTextBase32(text: str):
    try:
        base64.b32decode(text)
        return True
    except:
        return False

def convertTextToSecret(text: str):
    if isTextBase32(text):
        return pyotp.TOTP(text, name=-1)

    try:
        return pyotp.parse_uri(text)
    except:
        return None

def captureSecretFromImage(image):
    if isinstance(image, QImage):
        image = convertQtImageToPillow(image)

    code = zxingcpp.read_barcode(image, zxingcpp.BarcodeFormats(zxingcpp.BarcodeFormat.QRCode))

    if not code.valid:
        return None

    return convertTextToSecret(code.text)
