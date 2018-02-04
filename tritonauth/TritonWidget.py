from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class TritonWidget(QWidget):

    def __init__(self, base, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.base = base

    def setBackgroundColor(self, widget, color):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), color)
        widget.setPalette(palette)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TextboxWidget(TritonWidget):

    def __init__(self, base, name):
        TritonWidget.__init__(self, base)
        self.name = name
        self.setBackgroundColor(self, Qt.white)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setText(name)
        self.label.setFont(QFont('SansSerif', 10))

        self.box = QLineEdit()
        self.box.setFixedWidth(250)
        self.box.setFont(QFont('SansSerif', 10))

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.box)

class EditableLabel(QLabel):

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.editor = QLineEdit(self)
        self.editor.setWindowFlags(Qt.Popup)
        self.editor.setFocusProxy(self)
        self.editor.editingFinished.connect(self.handleEditingFinished)
        self.editor.installEventFilter(self)
        self.callback = lambda text: 0

    def eventFilter(self, widget, event):
        if ((event.type() == QEvent.MouseButtonPress and not self.editor.geometry().contains(event.globalPos())) or (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape)):
            self.editor.hide()
            return True

        return QLabel.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        rect = self.rect()
        self.editor.setFixedSize(rect.size())
        self.editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self.editor.setText(self.text())

        if not self.editor.isVisible():
            self.editor.show()

    def handleEditingFinished(self):
        text = self.editor.text()
        self.editor.hide()
        self.setText(text)
        self.callback(text)