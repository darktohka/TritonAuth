from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget, TextboxWidget

class ShowSecretWidget(TritonWidget):

    def __init__(self, base, keys, name, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.setWindowTitle(name)
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(20, 20, 20, 20)

        for key in keys:
            name, value = key
            widget = TextboxWidget(base, name)
            widget.box.setText(value)
            self.boxLayout.addWidget(widget)

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()
