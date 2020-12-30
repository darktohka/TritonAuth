from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QFont
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton
from .TritonWidget import TritonWidget, TextboxWidget
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

        self.nameWidget = TextboxWidget(base, 'Name:')

        self.secretLabel = QLabel()
        self.secretLabel.setText('Enter the Secret Code. If you have a QR code,\nyou can paste the URL of the image instead.')
        self.secretLabel.setFont(QFont('Helvetica', 10))

        self.secretBox = QLineEdit()
        self.secretBox.setFixedWidth(300)
        self.secretBox.setFont(QFont('Helvetica', 10))
        self.secretBox.textChanged.connect(lambda text: self.invalidateSecret())

        self.verifyLabel = QLabel()
        self.verifyLabel.setText('Click the Verify button to check the first code.')
        self.verifyLabel.setFont(QFont('Helvetica', 10))

        self.verifyBox = QLineEdit()
        self.verifyBox.setFixedWidth(150)
        self.verifyBox.setFont(QFont('Helvetica', 10))
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

    def getName(self):
        return self.nameWidget.box.text()

    def getAccount(self):
        return {'name': self.getName(), 'type': self.type, 'key': self.key, 'icon': 'icons/WinAuthIcon.png'}

    def invalidateSecret(self, value=''):
        self.key = None
        self.verifyBox.setText(value)

    def checkVerify(self):
        self.key = self.secretBox.text()

        if not self.key:
            self.invalidateSecret('Invalid')
            return

        self.key = self.base.readQRLink(self.key) or self.key
        self.key = self.key.upper().replace(' ', '')

        try:
            self.verifyBox.setText(self.base.getAuthCode(self.getAccount()))
        except:
            self.invalidateSecret('Invalid')

    def add(self):
        if not self.key or not self.getName():
            return

        self.base.addAccount(self.getAccount())
        self.close()
