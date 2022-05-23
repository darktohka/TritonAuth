from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QFont, QPixmap, QBrush, QColor, QAction, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMenu, QMessageBox, QPushButton
from .TritonWidget import TritonWidget, EditableLabel
from .PixmapButton import PixmapButton
from .ShowSecretWidget import ShowSecretWidget
from .EditIconWidget import EditIconWidget
from . import Globals
from .QRoundProgressBar import QRoundProgressBar
import pyperclip
import time, os

class EmptyTutorialWidget(TritonWidget):

    def __init__(self, base, mainWidget):
        TritonWidget.__init__(self, base)
        self.mainWidget = mainWidget

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont('Helvetica', 11)

        self.image = PixmapButton(QPixmap(os.path.join('assets', 'empty.png')))

        self.label = QLabel('You have no authentication entries so far...')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont('Helvetica', 14)
        font.setBold(True)

        self.subtext = QLabel('Get started by adding an authenticator!')
        self.subtext.setFont(font)
        self.subtext.setAlignment(Qt.AlignCenter)

        self.button = QPushButton('Add Authenticator')
        self.button.setFixedSize(125, 50)
        self.button.clicked.connect(self.mainWidget.openAddOTP)

        self.boxLayout.addWidget(self.image, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(20)
        self.boxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.subtext, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(10)
        self.boxLayout.addWidget(self.button, 0, Qt.AlignCenter)