from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StarOCR")
        self.setWindowIcon(QIcon("./data/scricon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(300, 120)
        self.setStyleSheet("background-color: #2c2c2c; color: white; ")
        

        self.label = QLabel("StarOCR")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Consolas", 30))

        self.waitlabel = QLabel("App Start.")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.waitlabel)
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def update_progress(self, percent, text):
        self.progress.setValue(percent)
        message = f"{text} loading... please wait"
        self.waitlabel.setText(message)
        QApplication.processEvents()
