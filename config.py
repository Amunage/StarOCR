from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox, QSlider,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from style import UIstyle

import re

from setting import user_data, load_user_data, save_user_data


class ConfigUI(QWidget):
    settings_applied = pyqtSignal()
    append_output = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("StarOCR Config")
        self.setWindowIcon(QIcon("./data/scricon.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(250, 400)

        data = load_user_data()

        # 위젯 생성
        self.label_config = QLabel("Prerefences")
        self.label_config.setAlignment(Qt.AlignCenter)
        self.label_config.setFont(QFont("Consolas", 12))

        self.label_fontsize = QLabel("Font Size")
        self.combo_fontsize = QComboBox()
        self.combo_fontsize.addItems([str(i) for i in range(10, 21)])
        self.combo_fontsize.setCurrentText(str(data.get("font_size", 10)))

        self.label_fontcolor = QLabel("Font Color")
        self.input_fontcolor = QLineEdit()
        self.input_fontcolor.setText(data.get("font_color", "d4f4dd"))

        self.label_tesseract = QLabel("Tesseract")
        self.combo_tesseract = QComboBox()
        self.combo_tesseract.addItems(["eng", "eng_fast"])
        self.combo_tesseract.setCurrentText(data.get("tesseract_lang", "eng"))

        self.label_opacity = QLabel("Opacity")
        self.label_opacity.setAlignment(Qt.AlignCenter)
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(1, 100)
        self.slider_opacity.setValue(data.get("background_opacity", 100))
        self.opacity_value_label = QLabel(str(data.get("background_opacity", 100)))
        self.opacity_value_label.setAlignment(Qt.AlignCenter)
        self.slider_opacity.valueChanged.connect(self.update_opacity_label)

        self.label_threads = QLabel("Threads")
        self.label_threads.setAlignment(Qt.AlignCenter)
        self.slider_threads = QSlider(Qt.Horizontal)
        self.slider_threads.setRange(1, 4)
        self.slider_threads.setValue(data.get("thread_count", 2))
        self.threads_value_label = QLabel(str(data.get("thread_count", 2)))
        self.threads_value_label.setAlignment(Qt.AlignCenter)
        self.slider_threads.valueChanged.connect(self.update_threads_label)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_settings)
        self.btn_cancel = QPushButton("Cancle")
        self.btn_cancel.clicked.connect(self.close)
        self.btn_confirm = QPushButton("OK")
        self.btn_confirm.clicked.connect(self.save_settings)

        # 스타일 적용
        self.setStyleSheet(UIstyle['container2'])
        self.label_config.setStyleSheet(UIstyle['label'])
        self.label_fontsize.setStyleSheet(UIstyle['label'])
        self.label_fontcolor.setStyleSheet(UIstyle['label'])
        self.label_tesseract.setStyleSheet(UIstyle['label'])
        self.label_opacity.setStyleSheet(UIstyle['label'])
        self.opacity_value_label.setStyleSheet(UIstyle['label'])
        self.label_threads.setStyleSheet(UIstyle['label'])
        self.threads_value_label.setStyleSheet(UIstyle['label'])

        self.combo_fontsize.setStyleSheet(UIstyle['combobox'])
        self.input_fontcolor.setStyleSheet(UIstyle['lineedit'])
        self.combo_tesseract.setStyleSheet(UIstyle['combobox'])
        self.slider_opacity.setStyleSheet(UIstyle['slider'])
        self.slider_threads.setStyleSheet(UIstyle['slider'])
        self.btn_reset.setStyleSheet(UIstyle['button'])
        self.btn_cancel.setStyleSheet(UIstyle['button'])
        self.btn_confirm.setStyleSheet(UIstyle['button'])

        # 레이아웃 구성
        # --- 폰트 구역 ---
        grid = QGridLayout()
        grid.setHorizontalSpacing(60)
        grid.addWidget(self.label_fontsize, 0, 0)
        grid.addWidget(self.combo_fontsize, 0, 1)
        grid.addWidget(self.label_fontcolor, 1, 0)
        grid.addWidget(self.input_fontcolor, 1, 1)
        grid.addWidget(self.label_tesseract, 2, 0)
        grid.addWidget(self.combo_tesseract, 2, 1)

        # --- Opacity 구역 ---
        opacity_frame = QFrame()
        opacity_frame.setFrameShape(QFrame.Box)
        opacity_layout = QVBoxLayout(opacity_frame)
        opacity_layout.setSpacing(0)
        opacity_layout.setContentsMargins(5, 5, 5, 5)
        opacity_layout.addWidget(self.label_opacity)
        opacity_layout.addWidget(self.slider_opacity)
        opacity_layout.addWidget(self.opacity_value_label)

        # --- Performance 구역 ---
        threads_frame = QFrame()
        threads_frame.setFrameShape(QFrame.Box)
        threads_layout = QVBoxLayout(threads_frame)
        threads_layout.setSpacing(0)
        threads_layout.setContentsMargins(5, 5, 5, 5)
        threads_layout.addWidget(self.label_threads)
        threads_layout.addWidget(self.slider_threads)
        threads_layout.addWidget(self.threads_value_label)

        # --- 버튼 구역 ---
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.btn_cancel)
        hbox_buttons.addWidget(self.btn_confirm)
        vbox_buttons = QVBoxLayout()
        vbox_buttons.addWidget(self.btn_reset)
        vbox_buttons.addLayout(hbox_buttons)

        # --- 레이아웃 배치 ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_config)
        main_layout.addSpacing(10)
        main_layout.addLayout(grid)
        main_layout.addSpacing(10)
        main_layout.addWidget(opacity_frame)
        main_layout.addWidget(threads_frame)
        main_layout.addSpacing(10)
        main_layout.addLayout(vbox_buttons)

        self.setLayout(main_layout)

    def update_opacity_label(self, value):
        self.opacity_value_label.setText(str(value))

    def update_threads_label(self, value):
        self.threads_value_label.setText(str(value))

    def reset_settings(self):
        self.combo_fontsize.setCurrentText("12")
        self.input_fontcolor.setText("d4f4dd")
        self.combo_tesseract.setCurrentText("eng")
        self.slider_opacity.setValue(50)
        self.opacity_value_label.setText("50")
        self.slider_threads.setValue(1)
        self.threads_value_label.setText("1")

        

    def save_settings(self):
        data = user_data or {}
        data["font_size"] = int(self.combo_fontsize.currentText())

        raw = self.input_fontcolor.text().lower().lstrip('#')
        data["font_color"] = raw if isinstance(raw, str) and re.fullmatch(r"[0-9a-fA-F]{6}", raw) else "d4f4dd"

        data["tesseract_lang"] = self.combo_tesseract.currentText()

        data["background_opacity"] = self.slider_opacity.value()

        old_threads_value = data.get("thread_count", 1)
        new_threads_value = self.slider_threads.value()
        data["thread_count"] = new_threads_value

        save_user_data(data)
        self.settings_applied.emit()
        
        if old_threads_value != new_threads_value:
            text = "Please restart the program." 
            self.append_output.emit(text)

        self.close()
