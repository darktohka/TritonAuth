from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QFont
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from .TritonWidget import TritonWidget, TextboxWidget
from .ScanQRWidget import ScanQRWidget
from .QRCodeUtils import captureSecretFromImage
from . import Globals

class AddOTPWidget(TritonWidget):

    def __init__(self, base, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.key = None
        self.scanWindow = None
        self.type = Globals.OTPAuth

        self.setWindowTitle('Add Authenticator')
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(20, 20, 20, 20)

        self.nameWidget = TextboxWidget(base, 'Name:')
        self.nameWidget.box.textChanged.connect(self.reconsiderButtons)

        self.secretLabel = QLabel()
        self.secretLabel.setText('Enter the Secret Code. If you have a QR code,\nyou can scan the QR code instead.')
        self.secretLabel.setFont(QFont('Helvetica', 10))

        self.secretBox = QLineEdit()
        self.secretBox.setFixedWidth(220)
        self.secretBox.setFont(QFont('Helvetica', 10))
        self.secretBox.textChanged.connect(lambda text: self.invalidateSecret())

        self.scanButton = QPushButton('Scan QR')
        self.scanButton.clicked.connect(self.openScanWindow)

        self.secretWidget = QWidget()
        self.secretLayout = QHBoxLayout()
        self.secretLayout.setContentsMargins(0, 0, 0, 0)

        self.secretLayout.addWidget(self.secretBox)
        self.secretLayout.addWidget(self.scanButton)

        self.secretWidget.setLayout(self.secretLayout)

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
        self.addButton.setEnabled(False)

        self.boxLayout.addWidget(self.nameWidget)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.secretLabel)
        self.boxLayout.addWidget(self.secretWidget)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.verifyLabel)
        self.boxLayout.addWidget(self.verifyBox, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.verifyButton, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.addButton, 0, Qt.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scanDesktops)
        self.timer.start(1000)

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()

    def stopTimer(self):
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()

        self.timer = None

    def closeEvent(self, event):
        self.cleanupWindows()
        self.stopTimer()
        event.accept()

    def scanDesktops(self):
        if self.secretBox.text().strip():
            return

        for screen in self.base.app.screens():
            geom = screen.geometry()
            screenshot = screen.grabWindow(0, geom.x(), geom.y(), geom.width(), geom.height())
            secret = captureSecretFromImage(screenshot)

            if secret:
                self.__onScanComplete(secret)
                break

    def cleanupWindows(self):
        if self.scanWindow:
            self.scanWindow.close()

        self.scanWindow = None

    def getName(self):
        return self.nameWidget.box.text()

    def getAccount(self):
        return {'name': self.getName(), 'type': self.type, 'key': self.key, 'icon': 'icons/WinAuthIcon.png'}

    def invalidateSecret(self, value=''):
        self.key = None
        self.verifyBox.setText(value)
        self.reconsiderButtons()

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

        self.reconsiderButtons()

    def isButtonValid(self):
        return bool(self.key and self.getName())

    def reconsiderButtons(self):
        self.addButton.setEnabled(self.isButtonValid())

    def add(self):
        if not self.isButtonValid():
            return

        self.base.addAccount(self.getAccount())
        self.close()

    def openScanWindow(self):
        self.cleanupWindows()
        self.scanWindow = ScanQRWidget(self.base, self.__onScanComplete)

    def __onScanComplete(self, code):
        if code.name != -1 and not self.nameWidget.box.text().strip():
            self.nameWidget.box.setText(code.name)

        self.secretBox.setText(code.secret.upper())