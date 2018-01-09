from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget

class LoginWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)

        self.setWindowTitle('TritonAuth')
        self.setBackgroundColor(self, Qt.white)
        
        self.widget = QWidget(self)
        self.widget.setContentsMargins(20, 20, 20, 20)

        self.boxLayout = QVBoxLayout()
        self.label = QLabel('Password')
        self.label.setFont(QFont('SansSerif', 10))
        
        self.passwordWidget = QWidget()
        self.passLayout = QHBoxLayout()
        self.passLayout.setContentsMargins(0, 5, 0, 0)
        
        self.passBox = QLineEdit()
        self.passBox.setEchoMode(QLineEdit.Password)
        self.passBox.setFixedWidth(250)
        self.passBox.setFont(QFont('SansSerif', 10))
        self.passBox.returnPressed.connect(self.handleLogin)
        self.setBackgroundColor(self.passBox, QColor(238, 238, 238))
        
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.handleLogin)

        self.passLayout.addWidget(self.passBox)
        self.passLayout.addWidget(self.okButton)
        self.passwordWidget.setLayout(self.passLayout)

        self.wrongLabel = QLabel()
        self.wrongLabel.setFont(QFont('SansSerif', 10))
        palette = self.wrongLabel.palette()
        palette.setColor(QPalette.Foreground, QColor(255, 0, 0))
        self.wrongLabel.setPalette(palette)

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
