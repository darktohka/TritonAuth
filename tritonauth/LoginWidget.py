from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QFont, QColor
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from .TritonWidget import TritonWidget

class LoginWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)

        self.setWindowTitle('TritonAuth')
        self.setBackgroundColor(self, Qt.white)

        self.widget = QWidget(self)
        self.widget.setContentsMargins(20, 20, 20, 20)

        self.boxLayout = QVBoxLayout()

        font = QFont('Helvetica', 13)
        font.setBold(True)

        self.title = QLabel('Unlock TritonAuth Database')
        self.title.setFont(font)

        self.label = QLabel('Enter Password:')
        self.label.setFont(QFont('Helvetica', 10))

        self.passwordWidget = QWidget()
        self.passLayout = QHBoxLayout()
        self.passLayout.setContentsMargins(0, 5, 0, 0)

        self.passBox = QLineEdit()
        self.passBox.setEchoMode(QLineEdit.Password)
        self.passBox.setFixedWidth(250)
        self.passBox.setFont(QFont('Helvetica', 10))
        self.passBox.returnPressed.connect(self.handleLogin)
        self.setBackgroundColor(self.passBox, QColor(238, 238, 238))

        self.unlockButton = QPushButton('Unlock')
        self.unlockButton.clicked.connect(self.handleLogin)

        self.passLayout.addWidget(self.passBox)
        self.passLayout.addWidget(self.unlockButton)
        self.passwordWidget.setLayout(self.passLayout)

        self.wrongLabel = QLabel()
        self.wrongLabel.setFont(QFont('Helvetica', 10))
        palette = self.wrongLabel.palette()
        palette.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.wrongLabel.setPalette(palette)

        self.boxLayout.addWidget(self.title)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.label)
        self.boxLayout.addWidget(self.passwordWidget)
        self.boxLayout.addWidget(self.wrongLabel)

        self.widget.setLayout(self.boxLayout)
        self.setFixedSize(self.widget.sizeHint())
        self.center()
        self.show()

    def handleLogin(self):
        response = self.base.authenticate(self.passBox.text())

        if response is not True:
            self.wrongLabel.setText(self.base.getError(response))
        else:
            self.base.stopLogin()
            self.base.startMain()
