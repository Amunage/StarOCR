
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect

from capture import capture_monitor
import setting


class ScreenSelector(QWidget):
    def __init__(self, background_image):
        super().__init__()
        self.setWindowTitle("Drag Capture Area")
        self.start = None
        self.end = None
        self.selection = None  # 선택 영역 결과 저장

        self.qpixmap = QPixmap.fromImage(background_image)

        # 전체 모니터 해상도 계산
        from PyQt5.QtWidgets import QApplication
        screens = QApplication.screens()
        total_rect = screens[0].geometry()
        for screen in screens[1:]:
            total_rect = total_rect.united(screen.geometry())

        self.setGeometry(total_rect)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.show()

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = self.start
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x = min(self.start.x(), self.end.x())
        y = min(self.start.y(), self.end.y())
        w = abs(self.start.x() - self.end.x())
        h = abs(self.start.y() - self.end.y())

        self.selection = (x, y, w, h)
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.qpixmap)

        if self.start and self.end:
            pen = QPen(Qt.green, 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start, self.end)
            painter.drawRect(rect)

def get_area_coordinates():

    app = QApplication.instance()
    if not app:
        raise RuntimeError("Not QApplication Instance!")

    img = capture_monitor()
    qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGB888)

    selector = ScreenSelector(qimage)
    selector.show()

    def wait_for_close():
        while selector.isVisible():
            QApplication.processEvents()
        return selector.selection

    coords = wait_for_close()
    if coords:
        save_ocrarea_to_json(coords)  # 여기서 저장!
    return coords


def save_ocrarea_to_json(area_coords):
    data = setting.userdata
    data["ocrarea"] = list(area_coords)
    setting.save_userdata(data)


