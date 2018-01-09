from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget

class ShowSecretWidget(TritonWidget):

    def __init__(self, base, key, name, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.setWindowTitle(name)
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel()
        self.label.setText('Your secret key is:')
        self.label.setFont(QFont('SansSerif', 10))

        self.secretBox = QLineEdit()
        self.secretBox.setText(key)
        self.secretBox.setFixedWidth(220)
        self.secretBox.setFont(QFont('SansSerif', 10))
        self.secretBox.setAlignment(Qt.AlignCenter)

        self.boxLayout.addWidget(self.label)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.secretBox)

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()
