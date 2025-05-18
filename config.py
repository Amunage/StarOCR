from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox, QSlider,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from style import UIstyle

import re

import setting


class ConfigUI(QWidget):
    settings_applied = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("StarOCR Config")
        self.setWindowIcon(QIcon("./data/scricon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(200, 300)

        data = setting.load_userdata()

        # 위젯 생성
        self.label_fontsize = QLabel("Font Size")
        self.combo_fontsize = QComboBox()
        self.combo_fontsize.addItems([str(i) for i in range(10, 21)])
        self.combo_fontsize.setCurrentText(str(data.get("fontsize", 10)))

        self.label_fontcolor = QLabel("Font Color")
        self.input_fontcolor = QLineEdit()
        self.input_fontcolor.setText(data.get("fontcolor", "d4f4dd"))
  

        self.label_interval = QLabel("Trans Interval")
        self.input_interval = QLineEdit()
        self.input_interval.setFixedWidth(60)
        self.input_interval.setText(str(int(data.get("interval", 3000) / 1000)))
        self.label_seconds = QLabel("Sec")

        self.label_opacity = QLabel("Opacity")
        self.label_opacity.setAlignment(Qt.AlignCenter)
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(1, 100)
        self.slider_opacity.setValue(data.get("background_opacity", 100))
        self.opacity_value_label = QLabel(str(data.get("background_opacity", 100)))
        self.opacity_value_label.setAlignment(Qt.AlignCenter)

        self.slider_opacity.valueChanged.connect(self.update_opacity_label)

        self.btn_cancel = QPushButton("Cancle")
        self.btn_cancel.clicked.connect(self.close)
        self.btn_confirm = QPushButton("OK")
        self.btn_confirm.clicked.connect(self.save_settings)

        # 스타일 적용
        self.setStyleSheet(UIstyle['container2'])
        self.label_fontsize.setStyleSheet(UIstyle['label'])
        self.label_fontcolor.setStyleSheet(UIstyle['label'])
        self.label_interval.setStyleSheet(UIstyle['label'])
        self.label_seconds.setStyleSheet(UIstyle['label'])
        self.label_opacity.setStyleSheet(UIstyle['label'])
        self.opacity_value_label.setStyleSheet(UIstyle['label'])

        self.combo_fontsize.setStyleSheet(UIstyle['combobox'])
        self.input_fontcolor.setStyleSheet(UIstyle['lineedit'])
        self.input_interval.setStyleSheet(UIstyle['lineedit'])

        self.slider_opacity.setStyleSheet(UIstyle['slider'])

        self.btn_cancel.setStyleSheet(UIstyle['button'])
        self.btn_confirm.setStyleSheet(UIstyle['button'])


        # 레이아웃 구성
        grid = QGridLayout()
        grid.addWidget(self.label_fontsize, 0, 0)
        grid.addWidget(self.combo_fontsize, 0, 1)
        grid.addWidget(self.label_fontcolor, 1, 0)
        grid.addWidget(self.input_fontcolor, 1, 1)
        grid.addWidget(self.label_interval, 2, 0)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.input_interval)
        interval_layout.addWidget(self.label_seconds)
        grid.addLayout(interval_layout, 2, 1)

        opacity_layout = QVBoxLayout()
        opacity_layout.addWidget(self.label_opacity)
        opacity_layout.addWidget(self.slider_opacity)
        opacity_layout.addWidget(self.opacity_value_label)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.btn_cancel)
        hbox_buttons.addWidget(self.btn_confirm)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        main_layout.addLayout(opacity_layout)
        main_layout.addLayout(hbox_buttons)

        self.setLayout(main_layout)

    def update_opacity_label(self, value):
        self.opacity_value_label.setText(str(value))

    def save_settings(self):
        data = setting.userdata or {}
        data["fontsize"] = int(self.combo_fontsize.currentText())

        raw = self.input_fontcolor.text().lower().lstrip('#')
        data["fontcolor"] = raw if isinstance(raw, str) and re.fullmatch(r"[0-9a-fA-F]{6}", raw) else "d4f4dd"

        try:
            data["interval"] = int(float(self.input_interval.text()) * 1000)
        except ValueError:
            data["interval"] = 3000  # fallback
        data["background_opacity"] = self.slider_opacity.value()
        setting.save_userdata(data)
        self.settings_applied.emit()
        self.close()
