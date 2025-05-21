from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue
import time

from tesseract import capture_and_ocr
from nllbtrans import run_translation

import traceback



ocr_queue = Queue(maxsize=20)  # 최대 20문장까지만 저장

class OCRWorker(QThread):
    def __init__(self, run_loop=True):
        super().__init__()
        self._is_running = True
        self.interval = 3
        self.run_loop = run_loop
        self.queue_threshold = 10  # 10개 이하로 줄어들면 재개

    def stop(self):
        self._is_running = False

    def run(self):
        while self._is_running:
            if ocr_queue.qsize() >= ocr_queue.maxsize:
                while ocr_queue.qsize() > self.queue_threshold:
                    if not self._is_running:
                        return
                    time.sleep(1)

            try:
                sentences = capture_and_ocr()
                for sentence in sentences:
                    if not self._is_running:
                        break
                    if sentence.strip():
                        if ocr_queue.full():
                            ocr_queue.get()
                        ocr_queue.put(sentence.strip())
                    else:
                        ocr_queue.put("")
            except Exception as e:
                tb = traceback.format_exc()
                ocr_queue.put(f"❌ Error: {tb}")
            finally:
                if not self.run_loop:
                    break
                for _ in range(int(self.interval * 10)):
                    if not self._is_running:
                        break
                    time.sleep(0.1)


        self.quit()

class TranslatorWorker(QThread):
    line_translated = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True

    def stop(self):
        self._is_running = False

    def run(self):
        while self._is_running:
            if not ocr_queue.empty():
                if not self._is_running:
                    break
                line = ocr_queue.get()
                # print(f"{ocr_queue.qsize()}:{line}")
                if line.startswith("❌ Error:"):
                    self.error_occurred.emit(line)
                if line:
                    try:
                        trans = run_translation(line)
                        if not self._is_running:
                            break
                        self.line_translated.emit(trans)
                    except Exception as e:
                        tb = traceback.format_exc()
                        self.line_translated.emit(f"❌ Error:\n{tb}")
                else:
                    self.line_translated.emit("")
            else:
                time.sleep(0.1)
        self.quit()
