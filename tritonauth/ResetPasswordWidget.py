from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from .TritonWidget import TritonWidget, TextboxWidget
from password_strength import PasswordStats

class ResetPasswordWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)

        self.setWindowTitle('Reset Password')
        self.setBackgroundColor(self, Qt.white)

        self.widget = QWidget(self)
        self.widget.setContentsMargins(20, 20, 20, 20)

        self.boxLayout = QVBoxLayout()

        self.label = QLabel("Please choose a new, strong password that you won't forget!")
        self.label.setFont(QFont('Helvetica', 13))

        self.passwordWidget = TextboxWidget(base, 'Password:')
        self.repeatPasswordWidget = TextboxWidget(base, 'Repeat Password:')

        self.passwordWidget.box.setEchoMode(QLineEdit.Password)
        self.passwordWidget.box.returnPressed.connect(self.handleReset)

        self.repeatPasswordWidget.box.setEchoMode(QLineEdit.Password)
        self.repeatPasswordWidget.box.returnPressed.connect(self.handleReset)

        self.passwordWidget.box.textChanged.connect(self.updateStrengthLabel)
        self.repeatPasswordWidget.box.textChanged.connect(self.updateStrengthLabel)

        self.setBackgroundColor(self.passwordWidget.box, QColor(238, 238, 238))
        self.setBackgroundColor(self.repeatPasswordWidget.box, QColor(238, 238, 238))

        self.strengthLabel = QLabel()
        self.strengthLabel.setFont(QFont('Helvetica', 10))

        self.proceedButton = QPushButton('Reset Password')
        self.proceedButton.setEnabled(False)
        self.proceedButton.setFixedSize(100, 50)
        self.proceedButton.clicked.connect(self.handleReset)

        self.boxLayout.addWidget(self.label)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.passwordWidget)
        self.boxLayout.addWidget(self.repeatPasswordWidget)
        self.boxLayout.addWidget(self.strengthLabel)
        self.boxLayout.addWidget(self.proceedButton, 0, Qt.AlignCenter)

        self.widget.setLayout(self.boxLayout)
        self.setFixedSize(self.widget.sizeHint())
        self.center()
        self.show()

        self.passwordWidget.box.setFocus(Qt.MouseFocusReason)

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

        try:
            entropy = PasswordStats(password).strength()
        except:
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

    def handleReset(self):
        if not self.proceedButton.isEnabled():
            return

        self.base.resetKey(self.passwordWidget.box.text())
        QMessageBox.information(self, 'TritonAuth', 'Your password has been successfuly changed!')
        self.close()