from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from .TritonWidget import TritonWidget
from .PixmapButton import PixmapButton
import os

class EditIconWidget(TritonWidget):

    def __init__(self, base, name, callback, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.callback = callback

        self.setWindowTitle(name)
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 5, 0, 0)
        layout = None
        
        for i, icon in enumerate(os.listdir('icons')):
            if (not layout) or i % 10 == 0:
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(5, 5, 5, 5)
                self.boxLayout.addWidget(widget)

            name = os.path.join('icons', icon)
            button = PixmapButton(QPixmap(name).scaled(48, 48))
            button.clicked.connect(self.makeIconCallback(name))
            button.setToolTip(icon)
            layout.addWidget(button)

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()

    def makeIconCallback(self, name):
        def iconCallback():
            self.callback(name)
            self.close()

        return iconCallback
