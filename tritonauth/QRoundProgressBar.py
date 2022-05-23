from PySide6.QtCore import Slot, QPointF, Qt, QRectF
from PySide6.QtGui import (QPalette, QConicalGradient, QGradient, QRadialGradient,
                           QFontMetricsF, QFont, QPainter, QPen, QPainterPath, QImage,
                           QPaintEvent)
from PySide6.QtWidgets import QWidget
from enum import Enum

class QRoundProgressBar(QWidget):
    PositionLeft = 180
    PositionTop = 90
    PositionRight = 0
    PositionBottom = -90

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.min = 0
        self.max = 100
        self.value = 25
        self.nullPosition = QRoundProgressBar.PositionTop
        self.barStyle = self.BarStyle.DONUT
        self.outlinePenWidth = 1
        self.dataPenWidth = 1
        self.rebuildBrush = False
        self.format = '%p%'
        self.decimals = 1
        self.updateFlags = self.UpdateFlags.PERCENT
        self.gradientData = None

    class BarStyle(Enum):
        DONUT = 0,
        PIE = 1,
        LINE = 2,
        EXPAND = 3

    class UpdateFlags(Enum):
        VALUE = 0,
        PERCENT = 1,
        MAX = 2

    def minimum(self):
        return self.min

    def maximum(self):
        return self.max

    def setNullPosition(self, position: float):
        if position != self.nullPosition:
            self.nullPosition = position
            self.rebuildBrush = True
            self.update()

    def setBarStyle(self, style: BarStyle):
        if style != self.barStyle:
            self.barStyle = style
            self.rebuildBrush = True
            self.update()

    def setOutlinePenWidth(self, width: float):
        if width != self.outlinePenWidth:
            self.outlinePenWidth = width
            self.update()

    def setDataPenWidth(self, width: float):
        if width != self.dataPenWidth:
            self.dataPenWidth = width
            self.update()

    def setDataColors(self, stopPoints: list):
        if stopPoints != self.gradientData:
            self.gradientData = stopPoints
            self.rebuildBrush = True
            self.update()

    def setFormat(self, val: str):
        if val != self.format:
            self.format = val
            self.valueFormatChanged()

    def resetFormat(self):
        self.format = None
        self.valueFormatChanged()

    def setDecimals(self, count: int):
        if count >= 0 and count != self.decimals:
            self.decimals = count
            self.valueFormatChanged()

    @Slot(float, float)
    def setRange(self, minval: float, maxval: float):
        self.min = minval
        self.max = maxval

        if self.max < self.min:
            self.min = maxval
            self.max = minval
        if self.value < self.min:
            self.value = self.min
        elif self.value > self.max:
            self.value = self.max

        self.rebuildBrush = True
        self.update()

    @Slot(float)
    def setMinimum(self, val: float):
        self.setRange(val, self.max)

    @Slot(float)
    def setMaximum(self, val: float):
        self.setRange(self.min, val)

    @Slot(int)
    def setValue(self, val: int):
        if self.value != val:
            if val < self.min:
                self.value = self.min
            elif val > self.max:
                self.value = self.max
            else:
                self.value = val

            self.update()

    def paintEvent(self, event: QPaintEvent):
        outerRadius = min(self.width(), self.height())
        baseRect = QRectF(1, 1, outerRadius - 2, outerRadius - 2)
        buffer = QImage(outerRadius, outerRadius, QImage.Format_ARGB32_Premultiplied)

        p = QPainter(buffer)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        self.rebuildDataBrushIfNeeded()
        self.drawBackground(p, buffer.rect())
        self.drawBase(p, baseRect)

        if self.value > 0:
            delta = (self.max - self.min) / (self.value - self.min)
        else:
            delta = 0

        self.drawValue(p, baseRect, self.value, delta)

        innerRect, innerRadius = self.calculateInnerRect(outerRadius)

        self.drawInnerBackground(p, innerRect)
        self.drawText(p, innerRect, innerRadius, self.value)
        p.end()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(baseRect, self.palette().window())
        painter.drawImage(0, 0, buffer)

    def drawBackground(self, p: QPainter, baseRect: QRectF):
        p.fillRect(baseRect, self.palette().window())

    def drawBase(self, p: QPainter, baseRect: QRectF):
        if self.barStyle == self.BarStyle.DONUT:
            p.setPen(QPen(self.palette().shadow().color(), self.outlinePenWidth))
            p.setBrush(self.palette().base())
            p.drawEllipse(baseRect)
        elif self.barStyle == self.BarStyle.LINE:
            p.setPen(QPen(self.palette().base().color(), self.outlinePenWidth))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(baseRect.adjusted(self.outlinePenWidth / 2, self.outlinePenWidth / 2,
                                            -self.outlinePenWidth / 2, -self.outlinePenWidth / 2))
        elif self.barStyle in (self.BarStyle.PIE, self.BarStyle.EXPAND):
            p.setPen(QPen(self.palette().base().color(), self.outlinePenWidth))
            p.setBrush(self.palette().base())
            p.drawEllipse(baseRect)

    def drawValue(self, p: QPainter, baseRect: QRectF, value: float, delta: float):
        if value == self.min:
            return

        if self.barStyle == self.BarStyle.EXPAND:
            p.setBrush(self.palette().highlight())
            p.setPen(QPen(self.palette().shadow().color(), self.dataPenWidth))
            radius = (baseRect.height() / 2) / delta
            p.drawEllipse(baseRect.center(), radius, radius)
            return
        elif self.barStyle == self.BarStyle.LINE:
            p.setPen(QPen(self.palette().highlight().color(), self.dataPenWidth))
            p.setBrush(Qt.NoBrush)

            if value == self.max:
                p.drawEllipse(baseRect.adjusted(self.outlinePenWidth / 2, self.outlinePenWidth / 2,
                                                -self.outlinePenWidth / 2, -self.outlinePenWidth / 2))
            else:
                arcLength = 360 / delta
                p.drawArc(baseRect.adjusted(self.outlinePenWidth / 2, self.outlinePenWidth / 2,
                                            -self.outlinePenWidth / 2, -self.outlinePenWidth / 2),
                          int(self.nullPosition * 16),
                          int(-arcLength * 16))

            return

        dataPath = QPainterPath()
        dataPath.setFillRule(Qt.WindingFill)

        if value == self.max:
            dataPath.addEllipse(baseRect)
        else:
            arcLength = 360 / delta
            dataPath.moveTo(baseRect.center())
            dataPath.arcTo(baseRect, self.nullPosition, -arcLength)
            dataPath.lineTo(baseRect.center())

        p.setBrush(self.palette().highlight())
        p.setPen(QPen(self.palette().shadow().color(), self.dataPenWidth))
        p.drawPath(dataPath)

    def calculateInnerRect(self, outerRadius: float):
        if self.barStyle in (self.BarStyle.LINE, self.BarStyle.EXPAND):
            innerRadius = outerRadius - self.outlinePenWidth
        else:
            innerRadius = outerRadius * 0.75

        delta = (outerRadius - innerRadius) / 2
        innerRect = QRectF(delta, delta, innerRadius, innerRadius)
        return innerRect, innerRadius

    def drawInnerBackground(self, p: QPainter, innerRect: QRectF):
        if self.barStyle == self.BarStyle.DONUT:
            p.setBrush(self.palette().alternateBase())
            p.drawEllipse(innerRect)

    def drawText(self, p: QPainter, innerRect: QRectF, innerRadius: float, value: float):
        if not self.format:
            return

        f = QFont(self.font())
        f.setPixelSize(10)

        fm = QFontMetricsF(f)
        maxWidth = fm.width(self.valueToText(self.max))
        delta = innerRadius / maxWidth
        fontSize = f.pixelSize() * delta * 0.75
        f.setPixelSize(int(fontSize))
        p.setFont(f)

        textRect = QRectF(innerRect)
        p.setPen(self.palette().text().color())
        p.drawText(textRect, Qt.AlignCenter, self.valueToText(value))

    def valueToText(self, value: float):
        textToDraw = self.format

        if self.updateFlags == self.UpdateFlags.VALUE:
            textToDraw = textToDraw.replace('%v', str(round(value, self.decimals)))
        elif self.updateFlags == self.UpdateFlags.PERCENT:
            procent = (value - self.min) / (self.max - self.min) * 100
            textToDraw = textToDraw.replace('%p', str(round(procent, self.decimals)))
        elif self.updateFlags == self.UpdateFlags.MAX:
            textToDraw = textToDraw.replace('%m', str(round(self.max - self.min + 1, self.decimals)))

        return textToDraw

    def valueFormatChanged(self):
        if '%v' in self.format:
            self.updateFlags = self.UpdateFlags.VALUE
        elif '%p' in self.format:
            self.updateFlags = self.UpdateFlags.PERCENT
        elif '%m' in self.format:
            self.updateFlags = self.UpdateFlags.MAX

        self.update()

    def rebuildDataBrushIfNeeded(self):
        if not self.rebuildBrush or not self.gradientData or self.barStyle == self.BarStyle.LINE:
            return

        self.rebuildBrush = False
        p = self.palette()

        if self.barStyle == self.BarStyle.EXPAND:
            dataBrush = QRadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
            dataBrush.setCoordinateMode(QGradient.StretchToDeviceMode)

            for i in range(0, len(self.gradientData)):
                dataBrush.setColorAt(self.gradientData[i][0], self.gradientData[i][1])

            p.setBrush(QPalette.Highlight, dataBrush)
        else:
            dataBrush = QConicalGradient(QPointF(0.5, 0.5), self.nullPosition)
            dataBrush.setCoordinateMode(QGradient.StretchToDeviceMode)

            for i in range(0, len(self.gradientData)):
                dataBrush.setColorAt(1 - self.gradientData[i][0], self.gradientData[i][1])

            p.setBrush(QPalette.Highlight, dataBrush)

        self.setPalette(p)
