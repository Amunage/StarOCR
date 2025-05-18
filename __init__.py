import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

import datapath
datapath.exePath()

# 준비
app = QApplication(sys.argv)

import splash
loader = splash.SplashScreen()
loader.show()

# 트레이스백

open("error.log", "w", encoding="utf-8").close()

def exception_hook(exctype, value, tb):
    try:
        with open("error.log", "a", encoding="utf-8", errors="ignore") as f:
            f.write("".join(traceback.format_exception(exctype, value, tb)))

        error_msg = "".join(traceback.format_exception(exctype, value, tb))
        print("Unhandled exception:", error_msg)

        msgbox = QMessageBox()
        msgbox.setWindowTitle("Error!")
        msgbox.setText("Error during the Application")
        msgbox.setDetailedText(error_msg)
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowFlag(Qt.WindowStaysOnTopHint)
        msgbox.exec_()

    except Exception as e:
        print("❌ 로그 기록 실패:", e)

sys.excepthook = exception_hook


# 메인 윈도우 시작
import main
loader.close()
QApplication.processEvents()
win = main.MainWindow()
win.show()

sys.exit(app.exec_())
