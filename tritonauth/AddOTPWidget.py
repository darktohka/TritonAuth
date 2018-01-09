from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget
from . import Globals

class AddOTPWidget(TritonWidget):

    def __init__(self, base, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.key = None
        self.type = Globals.OTPAuth

        self.setWindowTitle('Add Authenticator')
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(20, 20, 20, 20)

        self.nameWidget = QWidget()
        self.nameLayout = QHBoxLayout(self.nameWidget)
        self.nameLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLabel = QLabel()
        self.nameLabel.setText('Name:')
        self.nameLabel.setFont(QFont('SansSerif', 10))

        self.nameBox = QLineEdit()
        self.nameBox.setFixedWidth(250)
        self.nameBox.setFont(QFont('SansSerif', 10))

        self.nameLayout.addWidget(self.nameLabel) 
        self.nameLayout.addWidget(self.nameBox)

        self.secretLabel = QLabel()
        self.secretLabel.setText('Enter the Secret Code. If you have a QR code,\nyou can paste the URL of the image instead.')
        self.secretLabel.setFont(QFont('SansSerif', 10))

        self.secretBox = QLineEdit()
        self.secretBox.setFixedWidth(300)
        self.secretBox.setFont(QFont('SansSerif', 10))
        self.secretBox.textChanged.connect(self.invalidateSecret)

        self.verifyLabel = QLabel()
        self.verifyLabel.setText('Click the Verify button to check the first code.')
        self.verifyLabel.setFont(QFont('SansSerif', 10))

        self.verifyBox = QLineEdit()
        self.verifyBox.setFixedWidth(150)
        self.verifyBox.setFont(QFont('SansSerif', 10))
        self.verifyBox.setEnabled(False)

        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.black)
        self.verifyBox.setPalette(palette)
        self.verifyBox.setAlignment(Qt.AlignCenter)

        self.verifyButton = QPushButton('Verify')
        self.verifyButton.clicked.connect(self.checkVerify)
        self.verifyButton.setFixedWidth(150)

        self.addButton = QPushButton('OK')
        self.addButton.clicked.connect(self.add)

        self.boxLayout.addWidget(self.nameWidget)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.secretLabel)
        self.boxLayout.addWidget(self.secretBox)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.verifyLabel)
        self.boxLayout.addWidget(self.verifyBox, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.verifyButton, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.addButton, 0, Qt.AlignRight)
        
        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()

    def getAccount(self):
        return {'name': self.name, 'type': self.type, 'key': self.key}

    def invalidateSecret(self):
        self.key = None
        self.verifyBox.setText('')

    def checkVerify(self):
        key = self.secretBox.text()

        if not key:
            self.verifyBox.setText('Invalid')
            return

        key = self.base.readQRLink(key) or key

        try:
            self.verifyBox.setText(self.base.getAuthCode(self.type, key))
            self.key = key
        except:
            self.verifyBox.setText('Invalid')
            self.key = None

    def add(self):
        name = self.nameBox.text()

        if name and self.key:
            self.name = name
            self.base.addAccount(self.getAccount())
            self.close()
