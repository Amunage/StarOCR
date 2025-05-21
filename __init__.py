import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
app = QApplication(sys.argv)

import splash
loader = splash.SplashScreen()
loader.show()


import os
from PyQt5.QtCore import Qt
import importlib

modules = [
    "area",
    "capture",
    "cleaner",
    "config",
    "datapath",
    "nllbtrans",
    "preview",
    "setting",
    "style",
    "tesseract",
    "update",
    "workers",
    "torch"
]

for i, modname in enumerate(modules):
    loader.update_progress(int((i+1)/len(modules)*100), modname)
    globals()[modname] = importlib.import_module(modname)



# 성능 옵션 적용

import torch
from setting import user_data
thread_count = user_data.get("thread_count", 1)
print(f"Thread Count : {thread_count}")

os.environ["OMP_NUM_THREADS"] = f"{thread_count}"
os.environ["MKL_NUM_THREADS"] = f"{thread_count}"
torch.set_num_threads(thread_count)
torch.set_num_interop_threads(thread_count)

# GPU 제한 (있는 경우)
if torch.cuda.is_available():
    torch.cuda.set_per_process_memory_fraction(0.5, 0)


# 트레이스백
import traceback
open("./data/error.log", "w", encoding="utf-8").close()

def exception_hook(exctype, value, tb):
    try:
        with open("./error.log", "a", encoding="utf-8", errors="ignore") as f:
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
        print("❌ log failed!:", e)

sys.excepthook = exception_hook




# 메인 윈도우 시작
import main
loader.close()
QApplication.processEvents()
win = main.MainWindow()
win.show()

sys.exit(app.exec_())
