from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .TritonWidget import TritonWidget
from .EntryWidget import EntryWidget
from .AddOTPWidget import AddOTPWidget

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

        self.addMenu.addAction(self.authAction)
        self.addMenu.addAction(self.steamAction)
        
        self.widget = QWidget()
        self.widget.setContentsMargins(10, 10, 10, 10)

        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedSize(400, 495)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignTop)

        for account in self.base.getAccounts():
            self.addAccount(account)

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

            if widget.getAccount() == account:
                widget.close()

    def openAddOTP(self):
        self.closeAddOTP()
        self.addOTP = AddOTPWidget(self.base)