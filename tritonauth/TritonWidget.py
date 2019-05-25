from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QLabel, QLineEdit, QHBoxLayout
import os

class TritonWidget(QWidget):

    def __init__(self, base, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.base = base

        self.setWindowIcon(QIcon(os.path.join('icons', 'RefreshIconWithLock.png')))

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

    def __init__(self, save, failCallback, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.save = save
        self.editable = True
        self.failCallback = failCallback
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

    def disableEdit(self):
        self.editable = False
        self.editor.hide()

    def enableEdit(self):
        self.editable = True

    def mouseDoubleClickEvent(self, event=None):
        if not self.editable:
            if self.failCallback:
                self.failCallback()

            return

        rect = self.rect()
        self.editor.setFixedSize(rect.size())
        self.editor.move(self.mapToGlobal(rect.topLeft()))
        self.editor.setText(self.text())
        self.editor.setFocus(True)
        self.editor.selectAll()

        if not self.editor.isVisible():
            self.editor.show()

    def handleEditingFinished(self):
        text = self.editor.text()
        self.editor.hide()

        if self.save:
            self.setText(text)

        self.callback(text)