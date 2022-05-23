from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QAction
from PySide6.QtWidgets import QMenuBar, QWidget, QScrollArea, QVBoxLayout, QFileDialog, QMessageBox
from tritonauth.ResetPasswordWidget import ResetPasswordWidget
from .TritonWidget import TritonWidget
from .EntryWidget import EntryWidget
from .EmptyTutorialWidget import EmptyTutorialWidget
from .AddOTPWidget import AddOTPWidget
from .AddSteamWidget import AddSteamWidget
from .AboutWidget import AboutWidget
from .ResetPasswordWidget import ResetPasswordWidget
from . import Globals
import base64, webbrowser, json

class MainWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)
        self.subWindow = None
        self.closeEvent = self.widgetDeleted

        self.setWindowTitle('TritonAuth')
        self.setBackgroundColor(self, Qt.white)

        self.menu = QMenuBar()
        self.addMenu = self.menu.addMenu('Add')
        self.authAction = QAction('Authenticator', self)
        self.authAction.triggered.connect(self.openAddOTP)
        self.steamAction = QAction('Steam', self)
        self.steamAction.triggered.connect(self.openAddSteam)

        self.addMenu.addAction(self.authAction)
        self.addMenu.addAction(self.steamAction)

        self.manageMenu = self.menu.addMenu('Manage')
        self.nameAction = QAction('Sort By Name...', self)
        self.nameAction.triggered.connect(self.sortByName)
        self.andOTPAction = QAction('Export To andOTP...', self)
        self.andOTPAction.triggered.connect(self.exportToAndOTP)
        self.resetPasswordAction = QAction('Reset Password...', self)
        self.resetPasswordAction.triggered.connect(self.openResetPassword)

        self.manageMenu.addAction(self.nameAction)
        self.manageMenu.addAction(self.resetPasswordAction)
        self.manageMenu.addAction(self.andOTPAction)

        self.aboutMenu = self.menu.addMenu('Help')
        self.documentationAction = QAction('Open Documentation...')
        self.documentationAction.triggered.connect(self.openDocumentation)
        self.aboutProgramAction = QAction('About TritonAuth...')
        self.aboutProgramAction.triggered.connect(self.openAboutProgram)
        self.aboutQtAction = QAction('About Qt...')
        self.aboutQtAction.triggered.connect(lambda: QMessageBox.aboutQt(self))

        self.aboutMenu.addAction(self.documentationAction)
        self.aboutMenu.addAction(self.aboutProgramAction)
        self.aboutMenu.addAction(self.aboutQtAction)

        self.widget = QWidget()
        self.widget.setContentsMargins(10, 10, 10, 10)

        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedSize(400, 495)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignTop)

        self.createAccounts()

        self.scrollArea.setWidget(self.scrollWidget)

        self.widgetLayout = QVBoxLayout(self.widget)
        self.widgetLayout.addWidget(self.scrollArea)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 5, 0, 0)
        self.boxLayout.addWidget(self.menu)
        self.boxLayout.addWidget(self.widget)

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()

    def keyPressEvent(self, event):
        if type(event) != QKeyEvent:
            return

        letter = event.text().strip().lower()

        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i).widget()

            if widget is None or isinstance(widget, EmptyTutorialWidget) or widget.name[0].lower() != letter:
                continue

            self.scrollArea.verticalScrollBar().setValue(widget.geometry().top())
            break

    def widgetDeleted(self, arg):
        self.closeSubWindow()

    def closeSubWindow(self):
        if self.subWindow:
            self.subWindow.close()
            self.subWindow = None

    def addAccount(self, account):
        if self.scrollLayout.count() == 1 and isinstance(self.scrollLayout.itemAt(0).widget(), EmptyTutorialWidget):
            self.clearAccounts()

        entry = EntryWidget(self.base, account)
        self.scrollLayout.addWidget(entry)

    def deleteAccount(self, account):
        for i in range(self.scrollLayout.count()):
            item = self.scrollLayout.itemAt(i)
            widget = item.widget()

            if (not isinstance(widget, EmptyTutorialWidget)) and widget.account == account:
                widget.close()
                self.scrollLayout.removeItem(self.scrollLayout.itemAt(i))
                break

        if self.scrollLayout.count() == 0:
            self.scrollLayout.addWidget(EmptyTutorialWidget(self.base, self))

    def clearAccounts(self):
        for i in range(self.scrollLayout.count()):
            item = self.scrollLayout.itemAt(i)

            item.widget().close()
            self.scrollLayout.removeItem(item)

    def createAccounts(self):
        self.clearAccounts()

        accounts = self.base.getAccounts()

        for account in accounts:
            self.addAccount(account)

        if not accounts:
            self.scrollLayout.addWidget(EmptyTutorialWidget(self.base, self))

    def openDocumentation(self):
        webbrowser.open(Globals.DocumentationURL)

    def openResetPassword(self):
        self.closeSubWindow()
        self.subWindow = ResetPasswordWidget(self.base)

    def openAboutProgram(self):
        self.closeSubWindow()
        self.subWindow = AboutWidget(self.base)

    def openAddOTP(self):
        self.closeSubWindow()
        self.subWindow = AddOTPWidget(self.base)

    def openAddSteam(self):
        self.closeSubWindow()
        self.subWindow = AddSteamWidget(self.base)

    def sortByName(self):
        self.base.sortAccountsByName()
        self.createAccounts()

    def exportToAndOTP(self):
        accounts = []

        for account in self.base.getAccounts():
            type = account['type']

            if type == Globals.OTPAuth:
                accounts.append({'secret': account['key'], 'digits': 6, 'period': 30, 'label': account['name'], 'type': 'TOTP', 'algorithm': 'SHA1', 'thumbnail': 'Default', 'last_used': 0, 'tags': []})
            elif type == Globals.SteamAuth:
                accounts.append({'secret': base64.b32encode(base64.b64decode(account['sharedSecret'])).decode('utf-8'), 'digits': 5, 'period': 30, 'label': account['name'], 'type': 'STEAM', 'algorithm': 'SHA1', 'thumbnail': 'Default', 'last_used': 0, 'tags': []})

        accounts = json.dumps(accounts)
        filename, _ = QFileDialog.getSaveFileName(self, 'Export to andOTP JSON file', '', 'All Files (*)')

        if filename:
            with open(filename, 'w') as file:
                file.write(accounts)
