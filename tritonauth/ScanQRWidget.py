from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QComboBox, QMessageBox
from PySide6.QtMultimedia import QCamera, QImageCapture, QMediaCaptureSession, QMediaDevices
from PySide6.QtMultimediaWidgets import QVideoWidget
from .QRCodeUtils import captureSecretFromImage
from .TritonWidget import TritonWidget

class ScanQRWidget(TritonWidget):

    def __init__(self, base, callback, *args, **kwargs):
        TritonWidget.__init__(self, base, *args, **kwargs)
        self.callback = callback

        self.camera = None
        self.imageCapture = None
        self.captureSession = None
        self.timer = None

        self.availableCameras = QMediaDevices.videoInputs()

        if not self.availableCameras:
            QMessageBox.critical(self, 'TritonAuth', 'No video cameras are available!', QMessageBox.Ok)
            self.close()
            return

        self.setWindowTitle('Scan QR')
        self.setBackgroundColor(self, Qt.white)

        self.boxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)

        self.cameraWidget = QVideoWidget()

        self.cameraLabel = QLabel('Camera:')

        self.cameraBox = QComboBox()
        self.cameraBox.addItems([camera.description() for camera in self.availableCameras])
        self.cameraBox.currentIndexChanged.connect(self.connectCamera)

        self.settingsWidget = QWidget()
        self.cameraLayout = QHBoxLayout()

        self.cameraLayout.addWidget(self.cameraLabel)
        self.cameraLayout.addWidget(self.cameraBox)
        self.settingsWidget.setLayout(self.cameraLayout)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.close)
        self.cancelButton.setFixedSize(200, 30)

        self.boxLayout.addWidget(self.settingsWidget, 0, Qt.AlignCenter)
        self.boxLayout.addWidget(self.cameraWidget, 1)
        self.boxLayout.addWidget(self.cancelButton, 0, Qt.AlignCenter)
        self.boxLayout.addSpacing(5)

        self.connectCamera()

        self.setFixedSize(800 * 1.25, 510 * 1.25)
        self.center()
        self.show()

    def closeEvent(self, event):
        self.cleanupCamera()
        event.accept()

    def onCameraError(self, error, errorString):
        QMessageBox.critical(self, 'TritonAuth', errorString, QMessageBox.Ok)
        self.close()

    def cleanupCamera(self):
        if self.camera:
            self.camera.stop()
            self.camera.deleteLater()

        if self.imageCapture:
            self.imageCapture.deleteLater()

        if self.captureSession:
            self.captureSession.deleteLater()

        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()

        self.camera = None
        self.imageCapture = None
        self.captureSession = None
        self.timer = None

    def connectCamera(self):
        self.cleanupCamera()
        self.camera = QCamera(self.availableCameras[self.cameraBox.currentIndex()])
        self.camera.errorOccurred.connect(self.onCameraError)
        self.imageCapture = QImageCapture(self.camera)
        self.imageCapture.imageCaptured.connect(self.onImageCaptured)
        self.imageCapture.errorOccurred.connect(self.onCameraError)
        self.captureSession = QMediaCaptureSession()
        self.captureSession.setCamera(self.camera)
        self.captureSession.setImageCapture(self.imageCapture)
        self.captureSession.setVideoOutput(self.cameraWidget)
        self.camera.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.captureCamera)
        self.timer.start(100)

    def onImageCaptured(self, id, image):
        secret = captureSecretFromImage(image)

        if not secret:
            return

        self.callback(secret)

        if self.timer:
            self.timer.stop()

        self.cleanupCamera()
        self.close()

    def captureCamera(self):
        if self.imageCapture.isReadyForCapture():
            self.imageCapture.capture()
