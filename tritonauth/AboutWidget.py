from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from .PixmapButton import PixmapButton
from .TritonWidget import TritonWidget
import os

class AboutWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)

        self.setWindowTitle('About TritonAuth')
        self.setBackgroundColor(self, Qt.white)

        self.widget = QWidget(self)
        self.widget.setContentsMargins(20, 20, 20, 20)

        self.image = PixmapButton(QPixmap(os.path.join('assets', 'logo.png')))

        self.boxLayout = QVBoxLayout()

        font = QFont('Helvetica', 13)
        font.setBold(True)

        self.title = QLabel('TritonAuth')
        self.title.setFont(font)

        font = QFont('Helvetica', 13)
        font.setBold(True)

        self.subtitle = QLabel('Your one stop shop for two factor authentication')
        self.subtitle.setFont(font)

        self.label = QLabel('Written by\nDerzsi Dániel and Sallai József\nSapientia, 2022')
        self.label.setFont(QFont('Helvetica', 11))
        self.label.setAlignment(Qt.AlignCenter)

        self.boxLayout.addWidget(self.image, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.title, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.subtitle, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.label)

        self.widget.setLayout(self.boxLayout)
        self.setFixedSize(self.widget.sizeHint())
        self.center()
        self.show()
