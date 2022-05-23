from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QFont
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton
from .TritonWidget import TritonWidget, TextboxWidget
from . import Globals

class AddSteamWidget(TritonWidget):

    def __init__(self, base, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.sharedSecret = None
        self.identitySecret = None
        self.steamId = None
        self.type = Globals.SteamAuth

        self.setWindowTitle('Add Steam')
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(20, 20, 20, 20)

        self.nameWidget = TextboxWidget(base, 'Name:')
        self.steamIdWidget = TextboxWidget(base, 'Steam ID:')
        self.sharedWidget = TextboxWidget(base, 'Shared Secret:')
        self.identityWidget = TextboxWidget(base, 'Identity Secret:')

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
        self.boxLayout.addWidget(self.steamIdWidget)
        self.boxLayout.addWidget(self.sharedWidget)
        self.boxLayout.addWidget(self.identityWidget)
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
        return {'name': self.getName(), 'type': self.type, 'sharedSecret': self.sharedSecret, 'identitySecret': self.identitySecret, 'steamId': self.steamId, 'icon': 'icons/SteamIcon.png'}

    def invalidateSecret(self, text=''):
        self.sharedSecret = None
        self.identitySecret = None
        self.steamId = None
        self.verifyBox.setText(text)

    def checkVerify(self):
        self.sharedSecret = self.sharedWidget.box.text()
        self.identitySecret = self.identityWidget.box.text()
        self.steamId = self.steamIdWidget.box.text()

        if not self.sharedSecret or not self.identitySecret or not self.steamId:
            self.invalidateSecret('Invalid')
            return

        code = self.base.getAuthCode(self.getAccount())

        try:
            self.verifyBox.setText(code)
        except:
            self.invalidateSecret('Invalid')

    def add(self):
        if not self.sharedSecret or not self.getName():
            return

        self.base.addAccount(self.getAccount())
        self.close()
