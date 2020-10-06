from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QFont, QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMenu, QAction, QMessageBox
from .TritonWidget import TritonWidget, EditableLabel
from .PixmapButton import PixmapButton
from .ShowSecretWidget import ShowSecretWidget
from .EditIconWidget import EditIconWidget
from . import Globals
from qroundprogressbar import QRoundProgressBar
import time

class EntryWidget(TritonWidget):

    def __init__(self, base, account):
        TritonWidget.__init__(self, base)
        self.account = account
        self.type = account['type']
        self.name = account['name']
        self.icon = account['icon'].replace('\\', '/')
        self.timer = None
        self.secretWidget = None
        self.iconWidget = None

        self.closeEvent = self.widgetDeleted

        self.boxLayout = QHBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)

        self.image = QLabel()
        self.image.setFixedSize(48, 48)
        self.reloadIcon()

        self.detailWidget = QWidget()
        self.detailLayout = QVBoxLayout(self.detailWidget)
        self.detailLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLabel = EditableLabel(True, None)
        self.nameLabel.callback = self.renameAccount
        self.nameLabel.setText(self.name)
        self.nameLabel.setAlignment(Qt.AlignTop)
        self.nameLabel.setFont(QFont('Helvetica', 11))

        self.passLabel = EditableLabel(False, self.openPassLabel)
        self.passLabel.disableEdit()
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
        self.iconAction = QAction('Edit icon')
        self.iconAction.triggered.connect(self.editIcon)
        self.showAction = QAction('Show secret key')
        self.showAction.triggered.connect(self.showSecretKey)
        self.menu.addAction(self.removeAction)
        self.menu.addSeparator()
        self.menu.addAction(self.iconAction)
        self.menu.addAction(self.showAction)

    def getValue(self):
        return self.base.getAuthCode(self.account)

    def widgetDeleted(self, *args):
        self.stopTimer()
        self.name = None
        self.account = None

    def buttonPressed(self, *args):
        if not self.timer:
            self.showPassword()

    def openPassLabel(self, *args):
        self.buttonPressed()
        self.passLabel.mouseDoubleClickEvent()

    def openContextMenu(self, point):
        self.menu.exec_(self.mapToGlobal(point))

    def reloadIcon(self):
        pixmap = QPixmap(self.icon).scaled(48, 48)
        self.image.setPixmap(pixmap)

    def stopTimer(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

    def hidePassword(self):
        font = QFont('Helvetica', 10, weight=QFont.Bold)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)

        self.stopTimer()
        self.passLabel.setText('* ' * 5)
        self.passLabel.setFont(font)
        self.passLabel.disableEdit()
        self.showButton.show()
        self.timerProgress.hide()

    def showPassword(self):
        font = QFont('Helvetica', 13, weight=QFont.Bold)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)

        self.passLabel.setText(self.getValue())
        self.passLabel.setFont(font)
        self.passLabel.enableEdit()
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
            self.base.deleteAccount(self.account)

    def renameAccount(self, name):
        index = self.base.getAccountIndex(self.account)
        self.account['name'] = name
        self.base.setAccount(index, self.account)

    def editIcon(self):
        self.iconWidget = EditIconWidget(self.base, self.name, self.editIconCallback)

    def editIconCallback(self, icon):
        index = self.base.getAccountIndex(self.account)
        self.icon = icon.replace('\\', '/')
        self.account['icon'] = icon
        self.base.setAccount(index, self.account)
        self.reloadIcon()

    def showSecretKey(self):
        if self.type == Globals.OTPAuth:
            keys = [
                ('Key', self.account['key'])
            ]
        elif self.type == Globals.SteamAuth:
            keys = [
                ('Steam ID', self.account['steamId']),
                ('Shared Secret', self.account['sharedSecret']),
                ('Identity Secret', self.account['identitySecret'])
            ]
        else:
            keys = []

        self.secretWidget = ShowSecretWidget(self.base, keys, self.name)
