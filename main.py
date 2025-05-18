from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QMenu, QAction, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QIcon
from queue import Queue
import time

from area import get_area_coordinates
from preview import open_preview_window
from tesseract import capture_and_ocr
from config import ConfigUI

import nllbtrans

import setting
setting.load_userdata()
setting.load_custom_dict()

from style import UIstyle
import traceback

ocr_queue = Queue(maxsize=100)  # 최대 100문장까지만 저장

class OCRWorker(QThread):
    def __init__(self):
        super().__init__()
        self._is_running = True

    def stop(self):
        self._is_running = False

    def run(self):
        try:
            sentences = capture_and_ocr()
            for sentence in sentences:
                if not self._is_running:
                    break
                if sentence.strip():
                    if ocr_queue.full():
                        ocr_queue.get()  # 가장 오래된 항목 제거
                    ocr_queue.put(sentence.strip())
                else:
                    ocr_queue.put("")
        except Exception as e:
            tb = traceback.format_exc()
            ocr_queue.put(f"❌ Error: {tb}")
        finally:
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
                line = ocr_queue.get()
                print(line)
                if line.startswith("❌ Error:"):
                    self.error_occurred.emit(line)
                if line:
                    try:
                        trans = nllbtrans.run_translation(line)
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



class DragPassTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.mouse_press_time = None
        self.drag_start_pos = None
        self.dragPosition = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.mouse_press_time = time.time()
            self.dragPosition = event.globalPos() - self.parent_widget.frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.parent_widget.move(event.globalPos() - self.dragPosition)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.mouse_press_time is not None:
            elapsed = time.time() - self.mouse_press_time
            
            if elapsed < 0.2:
                self.parent_widget.show_context_menu(event.pos())
            event.accept()
        else:
            super().mouseReleaseEvent(event)
        self.mouse_press_time = None


class MainWindow(QWidget):
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("StarOCR")
        self.setWindowIcon(QIcon("./data/scricon.ico"))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        self.resize(500, 400)

        self.resizing = False
        self.resize_direction = None
        self.start_pos = None
        self.start_geometry = None
        self.resize_margin = 100

        self.viewer = None
        self.is_running = False

        self.setStyleSheet(UIstyle['container2'])

        self.ocr_timer = QTimer()
        self.ocr_timer.timeout.connect(self.run_ocr_worker)

        data = setting.userdata
        font_size = data.get("fontsize", 12)
        font_color = data.get("fontcolor", "d4f4dd")
        background_opacity = int(data.get("background_opacity", 70) * 2.55)

        self.output_box = DragPassTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setContextMenuPolicy(Qt.NoContextMenu)
        self.output_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_box.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: rgba(43, 43, 43, {background_opacity});
                color: #{font_color};
                font-size: {font_size}pt;
                border: 1px solid #555;
                padding: 8px;
            }}
        """)
        font = QFont("Consolas", font_size)
        self.output_box.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.output_box)
        self.setLayout(layout)


    def detect_resize_direction(self, pos):
        rect = self.rect()
        x, y = pos.x(), pos.y()
        margin = self.resize_margin
        directions = []

        if x < margin:
            directions.append("left")
        elif x > rect.width() - margin:
            directions.append("right")
        if y < margin:
            directions.append("top")
        elif y > rect.height() - margin:
            directions.append("bottom")

        return "-".join(directions)


    def cursor_for_direction(self, direction):
        return {
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "top-left": Qt.SizeFDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
        }.get(direction, Qt.ArrowCursor)

    def perform_resize(self, global_pos):
        dx = global_pos.x() - self.start_pos.x()
        dy = global_pos.y() - self.start_pos.y()
        geom = self.start_geometry

        new_rect = QRect(geom)

        if "right" in self.resize_direction:
            new_rect.setWidth(max(200, geom.width() + dx))
        if "bottom" in self.resize_direction:
            new_rect.setHeight(max(200, geom.height() + dy))
        if "left" in self.resize_direction:
            new_rect.setLeft(min(geom.right() - 200, geom.left() + dx))
        if "top" in self.resize_direction:
            new_rect.setTop(min(geom.bottom() - 200, geom.top() + dy))

        self.setGeometry(new_rect)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            direction = self.detect_resize_direction(event.pos())
            if direction:
                self.resizing = True
                self.resize_direction = direction
                self.start_pos = event.globalPos()
                self.start_geometry = self.geometry()

    def mouseMoveEvent(self, event):
        if self.resizing:
            self.perform_resize(event.globalPos())
        else:
            direction = self.detect_resize_direction(event.pos())
            self.setCursor(self.cursor_for_direction(direction))

    def mouseReleaseEvent(self, event):
        if self.resizing:
            self.resizing = False
            self.resize_direction = None
            self.setCursor(Qt.ArrowCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)


    def show_context_menu(self, pos):
        menu = QMenu()
        menu.setStyleSheet(UIstyle['menu'])  #  메뉴 스타일 적용

        toggle_action = QAction("Start" if not self.is_running else "Stop", self)
        toggle_action.triggered.connect(self.toggle_running)
        menu.addAction(toggle_action)

        snapshot_action = QAction("Snapshot", self)
        snapshot_action.triggered.connect(self.snapshot)
        menu.addAction(snapshot_action)

        area_action = QAction("Set Area", self)
        area_action.triggered.connect(self.select_area)
        menu.addAction(area_action)

        test_action = QAction("Preview", self)
        test_action.triggered.connect(self.ocr_preview)
        menu.addAction(test_action)

        config_action = QAction("Preference", self)
        config_action.triggered.connect(self.open_config_window)
        menu.addAction(config_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)

        menu.exec_(self.output_box.mapToGlobal(pos))

    def toggle_running(self):
        if not self.is_running:
            self.is_running = True

            self.trans_worker = TranslatorWorker()
            self.trans_worker.line_translated.connect(self.append_output)
            self.trans_worker.error_occurred.connect(self.append_output)
            self.trans_worker.start()

            interval = setting.userdata.get("interval", 3000)
            self.ocr_timer.start(interval)
            self.append_output(f"▶ Start Translation.")
        else:
            self.stop_ocr()
            self.is_running = False  # ← 여기서 나중에 꺼지게!



    def stop_ocr(self):
        was_running = self.is_running  # 현재 상태 저장

        self.ocr_timer.stop()
        self.is_running = False

        try:
            if hasattr(self, 'ocr_worker') and self.ocr_worker and self.ocr_worker.isRunning():
                self.ocr_worker.stop()
        except RuntimeError:
            pass
        try:
            if hasattr(self, 'trans_worker') and self.trans_worker and self.trans_worker.isRunning():
                self.trans_worker.stop()
        except RuntimeError:
            pass
  
        with ocr_queue.mutex:
            ocr_queue.queue.clear()

        if was_running:
            self.append_output("■ Stop Translation.")

    def select_area(self):
        self.stop_ocr()
        coords = get_area_coordinates()
        if coords:
            x, y, w, h = coords
            self.append_output(f"📐 Set Area → x:{x}, y:{y}, w:{w}, h:{h}")

    def ocr_preview(self):
        self.stop_ocr()
        try:
            if self.viewer:
                self.viewer.close()
            self.viewer = open_preview_window()
        except Exception as e:
            self.append_output(f"❌ Error: {e}")
            
    def snapshot(self):
        self.stop_ocr()

        # 번역 스레드가 없거나 이미 꺼졌다면 새로 실행
        if not hasattr(self, 'trans_worker') or not self.trans_worker.isRunning():
            self.trans_worker = TranslatorWorker()
            self.trans_worker.line_translated.connect(self.append_output)
            self.trans_worker.error_occurred.connect(self.append_output)
            self.trans_worker.start()

        self.run_ocr_worker()
        self.append_output("▷ Snapshot")


    def run_ocr_worker(self):
        try:
            if not hasattr(self, 'ocr_worker') or not self.ocr_worker.isRunning():
                self.ocr_worker = OCRWorker()
                self.ocr_worker.start()
        except RuntimeError:
            pass

    def open_config_window(self):
        self.stop_ocr()

        self.config_window = ConfigUI()
        self.config_window.settings_applied.connect(self.apply_settings)
        self.config_window.show()

    def append_output(self, text, max_lines=100):
        self.output_box.appendPlainText(text)
        doc = self.output_box.document()
        while doc.blockCount() > max_lines:
            cursor = self.output_box.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    def apply_settings(self):
        data = setting.load_userdata()
        background_opacity = int(data.get("background_opacity", 70) * 2.55)
        font_size = data.get("fontsize", 12)
        font_color = data.get("fontcolor", "d4f4dd")

        self.output_box.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: rgba(43, 43, 43, {background_opacity});
                color: #{font_color};
                font-size: {font_size}pt;
                border: 1px solid #555;
                padding: 8px;
            }}
        """)
        
        self.append_output(f"✔️ Save Setting")