from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QFont, QColor, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from .PixmapButton import PixmapButton
from .TritonWidget import TritonWidget, TextboxWidget
from password_strength import PasswordStats
import os

class WelcomeWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)

        self.setWindowTitle('Welcome!')
        self.setBackgroundColor(self, Qt.white)

        self.widget = QWidget(self)
        self.widget.setContentsMargins(20, 20, 20, 20)

        self.image = PixmapButton(QPixmap(os.path.join('assets', 'logo.png')))

        self.boxLayout = QVBoxLayout()

        font = QFont('Helvetica', 17)
        font.setBold(True)

        self.title = QLabel('Welcome to TritonAuth!')
        self.title.setFont(font)

        font = QFont('Helvetica', 13)
        font.setBold(True)

        self.subtitle = QLabel('Your one stop shop for two factor authentication')
        self.subtitle.setFont(font)

        self.label = QLabel('TritonAuth is a two-factor authentication application for Windows.\nIt generates Time-based One-time Passwords (TOTP) for you.\n\nTo get started, choose a secure password:')
        self.label.setFont(QFont('Helvetica', 11))

        self.passwordWidget = TextboxWidget(base, 'Password:')
        self.repeatPasswordWidget = TextboxWidget(base, 'Repeat Password:')

        self.passwordWidget.box.setEchoMode(QLineEdit.Password)
        self.passwordWidget.box.returnPressed.connect(self.handleLogin)

        self.repeatPasswordWidget.box.setEchoMode(QLineEdit.Password)
        self.repeatPasswordWidget.box.returnPressed.connect(self.handleLogin)

        self.passwordWidget.box.textChanged.connect(self.updateStrengthLabel)
        self.repeatPasswordWidget.box.textChanged.connect(self.updateStrengthLabel)

        self.setBackgroundColor(self.passwordWidget.box, QColor(238, 238, 238))
        self.setBackgroundColor(self.repeatPasswordWidget.box, QColor(238, 238, 238))

        self.strengthLabel = QLabel()
        self.strengthLabel.setFont(QFont('Helvetica', 10))

        self.proceedButton = QPushButton('Continue')
        self.proceedButton.setEnabled(False)
        self.proceedButton.setFixedSize(100, 50)
        self.proceedButton.clicked.connect(self.handleLogin)

        self.boxLayout.addWidget(self.image, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.title, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.subtitle, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.label)
        self.boxLayout.addWidget(self.passwordWidget)
        self.boxLayout.addWidget(self.repeatPasswordWidget)
        self.boxLayout.addWidget(self.strengthLabel)
        self.boxLayout.addWidget(self.proceedButton, 0, Qt.AlignCenter)

        self.widget.setLayout(self.boxLayout)
        self.setFixedSize(self.widget.sizeHint())
        self.center()
        self.show()

        self.updateStrengthLabel()

    def setStrengthLabelColor(self, color):
        palette = self.strengthLabel.palette()
        palette.setColor(QPalette.WindowText, color)
        self.strengthLabel.setPalette(palette)

    def updateStrengthLabel(self):
        password = self.passwordWidget.box.text()
        repeatPassword = self.repeatPasswordWidget.box.text()

        if repeatPassword and password != repeatPassword:
            self.strengthLabel.setText('Password mismatch')
            self.setStrengthLabelColor(QColor(255, 0, 0))
            self.proceedButton.setEnabled(False)
            return

        if password:
            entropy = PasswordStats(password).strength()
        else:
            entropy = 0

        if entropy < 0.33:
            self.strengthLabel.setText('Weak password')
            self.setStrengthLabelColor(QColor(255, 0, 0))
        elif entropy < 0.66:
            self.strengthLabel.setText('Moderate password')
            self.setStrengthLabelColor(QColor(255, 165, 0))
        else:
            self.strengthLabel.setText('Strong password')
            self.setStrengthLabelColor(QColor(0, 165, 0))

        self.proceedButton.setEnabled(entropy >= 0.33 and password == repeatPassword)

    def handleLogin(self):
        if not self.proceedButton.isEnabled():
            return

        response = self.base.authenticate(self.passwordWidget.box.text())

        if response is not True:
            self.strengthLabel.setText(self.base.getError(response))
            return

        self.base.stopLogin()
        self.base.startMain()
