from PySide6.QtWidgets import QApplication, QMessageBox
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from PIL import Image

from .Settings import Settings
from .LoginWidget import LoginWidget
from .WelcomeWidget import WelcomeWidget
from .MainWidget import MainWidget
from . import AESCipher, Globals, SteamUtils
import sys, json, re
import pyotp

class TritonAuth(object):

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loadSettings()
        self.login = None
        self.main = None
        self.key = ''
        self.data = {}

    def getAuthCode(self, account):
        type = account.get('type', None)

        if type == Globals.OTPAuth:
            return pyotp.TOTP(account['key']).now()
        elif type == Globals.SteamAuth:
            return SteamUtils.generateCode(account['sharedSecret'])
        else:
            return ''

    def getError(self, error):
        return Globals.ErrorMessages.get(error, Globals.DefaultErrorMessage)

    def isLink(self, str):
        return re.match('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', str) is not None

    def readQRLink(self, link):
        if self.isLink(link):
            try:
                with urlopen(link) as file:
                    image = Image.open(file)
                    image.load()
                return
                for code in zbarlight.scan_codes('qrcode', image):
                    try:
                        return parse_qs(urlparse(code).query)[b'secret'][0].decode('utf-8')
                    except:
                        pass
            except:
                return None

    def loadSettings(self):
        try:
            self.settings = Settings('user.json')
        except:
            QMessageBox.about(None, "Corrupt data", "It looks like your TritonAuth data has become corrupted. Please restore an earlier backup to resolve this issue.")
            sys.exit()

    def isSetup(self):
        return 'data' in self.settings

    def saveData(self):
        self.settings['data'] = AESCipher.encrypt(self.key, json.dumps(self.data))

    def loadData(self):
        self.data = json.loads(AESCipher.decrypt(self.key, self.settings['data']))

        if 'accounts' not in self.data:
            raise Exception('Invalid data given.')

    def getAccounts(self):
        return self.data['accounts']

    def sortAccountsByName(self):
        self.data['accounts'].sort(key=lambda acc: acc['name'])
        self.saveData()

    def addAccount(self, account):
        if account not in self.data['accounts']:
            self.data['accounts'].append(account)
            self.saveData()

            if self.main:
                self.main.addAccount(account)

    def deleteAccount(self, account, removeMain=True):
        if account in self.data['accounts']:
            self.data['accounts'].remove(account)
            self.saveData()

            if removeMain and self.main:
                self.main.deleteAccount(account)

    def setAccount(self, index, account):
        self.data['accounts'][index] = account
        self.saveData()

    def getAccountIndex(self, account):
        return self.data['accounts'].index(account)

    def getAccount(self, index):
        return self.data['accounts'][index]

    def startLogin(self):
        self.stopLogin()

        if self.isSetup():
            self.login = LoginWidget(self)
        else:
            self.login = WelcomeWidget(self)

    def stopLogin(self):
        if self.login:
            self.login.close()
            self.login = None

    def startMain(self):
        self.stopMain()
        self.main = MainWidget(self)

    def stopMain(self):
        if self.main:
            self.main.close()
            self.main = None

    def resetKey(self, password, save=True):
        self.key = AESCipher.getKey(password)

        if save:
            self.saveData()

    def authenticate(self, password):
        if not password:
            return Globals.ErrorNoPassword
        elif len(password) < 6:
            return Globals.ErrorShortPassword

        self.data = {'accounts': []}
        self.resetKey(password, save=not self.isSetup())

        if not self.isSetup():
            return True

        try:
            self.loadData()
            return True
        except:
            return Globals.ErrorWrongPassword

    def mainLoop(self):
        self.app.exec_()
