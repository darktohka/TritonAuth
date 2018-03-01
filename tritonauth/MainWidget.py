from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget
from .EntryWidget import EntryWidget
from .AddOTPWidget import AddOTPWidget
from .AddSteamWidget import AddSteamWidget
from . import Globals
import base64, json

class MainWidget(TritonWidget):

    def __init__(self, base):
        TritonWidget.__init__(self, base)
        self.addOTP = None
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
        
        self.sortMenu = self.menu.addMenu('Sort')
        self.nameAction = QAction('Sort by name', self)
        self.nameAction.triggered.connect(self.sortByName)
        
        self.sortMenu.addAction(self.nameAction)

        self.exportMenu = self.menu.addMenu('Export')
        self.andOTPAction = QAction('Export to andOTP', self)
        self.andOTPAction.triggered.connect(self.exportToAndOTP)
        
        self.exportMenu.addAction(self.andOTPAction)
        
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

    def widgetDeleted(self, arg):
        self.closeAddOTP()

    def closeAddOTP(self):
        if self.addOTP:
            self.addOTP.close()
            self.addOTP = None

    def addAccount(self, account):
        entry = EntryWidget(self.base, account)
        self.scrollLayout.addWidget(entry)

    def deleteAccount(self, account):
        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i).widget()

            if widget.account == account:
                widget.close()
    
    def clearAccounts(self):
        for i in range(self.scrollLayout.count()):
            self.scrollLayout.itemAt(i).widget().close()
    
    def createAccounts(self):
        for account in self.base.getAccounts():
            self.addAccount(account)

    def openAddOTP(self):
        self.closeAddOTP()
        self.addOTP = AddOTPWidget(self.base)

    def openAddSteam(self):
        self.closeAddOTP()
        self.addOTP = AddSteamWidget(self.base)
    
    def sortByName(self):
        self.base.sortAccountsByName()
        self.clearAccounts()
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