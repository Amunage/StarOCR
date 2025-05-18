from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QImage
from tesseract import best_image_for_ocr
from style import UIstyle 


def open_preview_window():
    img = best_image_for_ocr()
    viewer = ImagePreview(img)
    viewer.show()

    return viewer


class ImagePreview(QWidget):
    def __init__(self, original_image):
        super().__init__()
        self.setWindowTitle("StarOCR Preview")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(600, 400)

        self.setAttribute(Qt.WA_Hover)  #  hover 추적
        self.setMouseTracking(True)     #  커서 추적
        self.resizing = False
        self.resize_direction = None
        self.start_pos = None
        self.start_geometry = None
        self.resize_margin = 100


        self.setStyleSheet(UIstyle['container2'])

        self.original_image = original_image

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMinimumSize(1, 1)

        self.confirm_button = QPushButton("OK")
        self.confirm_button.clicked.connect(self.confirm_config)
        self.confirm_button.setStyleSheet(UIstyle['button'])

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

        self.update_image()

    def update_image(self):
        height, width = self.original_image.shape
        qimage = QImage(self.original_image.data, width, height, width, QImage.Format_Grayscale8).copy()
        pixmap = QPixmap.fromImage(qimage)
        scaled = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        self.update_image()
        super().resizeEvent(event)

    def confirm_config(self):
        self.close()



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
