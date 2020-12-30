from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QAbstractButton

class PixmapButton(QAbstractButton):

    def __init__(self, pixmap, parent=None):
        QAbstractButton.__init__(self, parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QRect(0, 0, self.pixmap.width(), self.pixmap.height()), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
