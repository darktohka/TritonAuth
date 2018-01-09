from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget
from .PixmapButton import PixmapButton
from .ShowSecretWidget import ShowSecretWidget
from qroundprogressbar import QRoundProgressBar
import time

class EntryWidget(TritonWidget):

    def __init__(self, base, account):
        TritonWidget.__init__(self, base)
        self.account = account
        self.type = account['type']
        self.name = account['name']
        self.key = account['key']
        self.icon = account['icon']
        self.timer = None
        self.secretWidget = None

        self.closeEvent = self.widgetDeleted

        self.boxLayout = QHBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)

        self.image = QLabel()
        pixmap = QPixmap('icons/WinAuthIcon.png').scaled(48, 48)
        self.image.setPixmap(pixmap)
        self.image.setFixedSize(48, 48)

        self.detailWidget = QWidget()
        self.detailLayout = QVBoxLayout(self.detailWidget)
        self.detailLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLabel = QLabel()
        self.nameLabel.setText(self.name)
        self.nameLabel.setAlignment(Qt.AlignTop)
        self.nameLabel.setFont(QFont('SansSerif', 11))

        self.passLabel = QLabel()
        self.passLabel.setAlignment(Qt.AlignBottom)

        self.detailLayout.addWidget(self.nameLabel)
        self.detailLayout.addWidget(self.passLabel)

        self.showButton = PixmapButton(QPixmap('icons/RefreshIcon.png').scaled(48, 48))
        self.showButton.clicked.connect(self.buttonPressed)

        self.timerProgress = QRoundProgressBar()
        self.timerProgress.setBarStyle(QRoundProgressBar.BarStyle.PIE)
        self.timerProgress.setFixedSize(48, 48)
        self.timerProgress.setFormat('')
        self.timerProgress.mouseReleaseEvent = self.buttonPressed
        palette = QPalette()
        brush = QBrush(QColor(155, 183, 214))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

        self.timerProgress.setPalette(palette)
        self.timerProgress.hide()

        self.boxLayout.addWidget(self.image)
        self.boxLayout.addSpacing(5)
        self.boxLayout.addWidget(self.detailWidget)
        self.boxLayout.addWidget(self.showButton, 0, Qt.AlignRight)
        self.boxLayout.addWidget(self.timerProgress, 0, Qt.AlignRight)
        self.setFixedSize(360, 48)
        self.hidePassword()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)
        self.menu = QMenu(self)
        self.removeAction = QAction('Remove')
        self.removeAction.triggered.connect(self.removeAccount)
        self.showAction = QAction('Show secret key')
        self.showAction.triggered.connect(self.showSecretKey)
        self.menu.addAction(self.removeAction)
        self.menu.addSeparator()
        self.menu.addAction(self.showAction)

    def getValue(self):
        return self.base.getAuthCode(self.type, self.key)

    def getAccount(self):
        return {'name': self.name, 'type': self.type, 'key': self.key, 'icon': self.icon}

    def widgetDeleted(self, *args):
        self.stopTimer()
        self.name = None
        self.key = None

    def buttonPressed(self, *args):
        if self.timer:
            self.hidePassword()
        else:
            self.showPassword()

    def openContextMenu(self, point):
        self.menu.exec_(self.mapToGlobal(point))

    def stopTimer(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

    def hidePassword(self):
        self.stopTimer()
        self.passLabel.setText('* ' * 5)
        self.passLabel.setFont(QFont('SansSerif', 9, weight=QFont.Bold))
        self.showButton.show()
        self.timerProgress.hide()

    def showPassword(self):
        self.passLabel.setText(self.getValue())
        self.passLabel.setFont(QFont('SansSerif', 12, weight=QFont.Bold))
        self.showButton.hide()
        self.timerProgress.show()
        self.timerEnd = time.time() + 15

        if not self.timer:
            self.timerProgress.setValue(100)
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateProgress)
            self.timer.start(100)

    def updateProgress(self):
        if self.timerProgress.isHidden() or self.timerEnd <= time.time():
            self.hidePassword()
            return

        delta = (self.timerEnd - time.time()) / 15 * 100
        self.timerProgress.setValue(delta)

    def removeAccount(self):
        reply = QMessageBox.question(self, self.name, 'ATTENTION! Deleting this account is an irreversible action!\n\nAre you absolutely sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.base.deleteAccount(self.getAccount())

    def showSecretKey(self):
        self.secretWidget = ShowSecretWidget(self.base, self.key, self.name)