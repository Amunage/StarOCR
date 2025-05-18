
menu = """
    QMenu {
        border: None;
        background-color: rgba(40, 40, 40, 1);
        color: white;
    }

    QMenu::item:selected {
        background-color: rgba(30, 30, 30, 1);
        color: #7bdf08;
    }
"""

container1 = """
    QWidget#containerWidget {
        border: None;
        border-radius: 10px;
        color: white;
        background-color: rgba(40, 40, 40, 1);
    }
"""

container2 = """
    QWidget {
        border: None;
        border-radius: 10px;
        background-color: rgba(35, 35, 35, 1);
    }
"""

slider = """
    QSlider {
        padding: 10px;
        background: transparent;
    }
    QSlider::groove:horizontal {
        border: none;
        height: 10px;
        margin: 0px;
        border-radius: 5px;
        background: rgba(220, 220, 220, 1);
    }
    QSlider::handle:horizontal {
        background: #7bdf08;
        border: none;
        width: 20px;
        margin: -5px -5px -5px -5px;
        border-radius: 10px;
    }
""" 

combobox = """
    QComboBox {
        border: None;
        border-radius: 3px;
        background-color: rgba(30, 30, 30, 1);
        padding: 5px;
        color : white;
    }
    QComboBox::drop-down {
        border: none;
    } 
    QComboBox::down-arrow {
        color : white;
    }
    QComboBox QAbstractItemView {
        border: None;
        background-color: rgba(20, 20, 20, 1);
        color : white;
        padding: 5px;
        selection-background-color: transparent;
        selection-color: #7bdf08;
        min-height: 50px;
    }
    
    QScrollBar:vertical {
        width: 15px;
        background: transparent;
    }
    QScrollBar::handle:vertical {
        background: #7bdf08;
        border-radius: 7px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        width: 0px;
        height: 0px;
        background: none;
    }
"""


label = """
    QLabel {
        color: white;
        background-color: transparent;
    }
"""

button = """
    QPushButton {
        border: None;
        border-radius: 15px;
        padding: 10px;
        color: white;
        background-color: rgba(30, 30, 30, 1);
    }
    QPushButton:hover {
        color: #7bdf08;
        background-color: rgba(20, 20, 20, 1);
    }
"""

circlebutton = """
    QPushButton {
        border: 1px solide rgba(210, 210, 210, 1);
        border-radius: 10px;
        color: rgba(210, 210, 210, 1);
        background-color: rgba(30, 30, 30, 1);
    }
    QPushButton:hover {
        color: #7bdf08;
        background-color: rgba(20, 20, 20, 1);
    }
    QPushButton:focus {
        color: white;
        background-color: rgba(20, 20, 20, 1);
    }
        """

sizebutton = """
    QPushButton {
        border: None;
        border-radius: 15px;
        color: white;
        background-color: rgba(30, 30, 30, 1);
    }
    QPushButton:hover {
        color: #7bdf08;
        background-color: rgba(20, 20, 20, 1);
    }
    QPushButton:focus {
        color: white;
        background-color: rgba(20, 20, 20, 1);
    }
"""

togglebutton = """
    QPushButton {
        border: None;
        border-radius: 15px;
        padding: 10px;
        color: white;
        background-color: rgba(123, 223, 8, 1);
    }
    QPushButton:hover {
        color: white;
        background-color: rgba(20, 20, 20, 1);
    }
"""

textedit = """
    QTextEdit {
        border: none;
        border-radius: 10px;
        padding: 10px;
        color: rgba(210, 210, 210, 1);
        background: rgba(30, 30, 30, 1);
    }
    QTextEdit QScrollBar:vertical {
        width: 15px;
        background: transparent;
    }
    QTextEdit QScrollBar::handle:vertical {
        background: #7bdf08;
        border-radius: 7px;
        min-height: 20px;
    }
    QTextEdit QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QTextEdit QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        width: 0px;
        height: 0px;
        background: none;
    }
    QPlainTextEdit {
        background-color: #2b2b2b;
        color: #d4f4dd;
        font-size: 12pt;
        border: 1px solid #555;
        padding: 8px;
    }

"""
lineedit = """
    QLineEdit {
        border: none;
        border-radius: 10px;
        padding-left: 12px;
        color: rgba(210, 210, 210, 1);
        background: rgba(30, 30, 30, 1);
    }
"""

scrollarea = """
    QScrollArea {
        border: none;
        border-radius: 10px;
        background-color: rgba(30, 30, 30, 1);
    }
    QScrollBar:vertical {
        width: 15px;
        background: transparent;
    }
    QScrollBar::handle:vertical {
        background: #7bdf08;
        border-radius: 7px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        width: 0px;
        height: 0px;
        background: none;
    }
"""

logspeaker = """
    QLabel {
        color: #794016;
        background-color: lightblue;
        border-radius: 10px;
        padding: 5px;
        margin: 2px;
    }
"""

logtalker = """
    QLabel {
        color: #794016;
        background-color: pink;
        border-radius: 10px;
        padding: 5px;
        margin: 2px;
    }
"""

loglabel = "color: white; background: transparent;"

messagebox = """
    QMessageBox {
        background-color: rgba(35, 35, 35, 1);
        color: white;
        font-size: 12pt;
    }
    QLabel {
        color: white;
    }
    QPushButton {
        background-color: rgba(30, 30, 30, 1);
        color: white;
        border-radius: 5px;
        padding: 5px 12px;
    }
    QPushButton:hover {
        background-color: rgba(20, 20, 20, 1);
        color: #7bdf08;
    }
"""

##################################################################

UIstyle = {
    'menu': menu,
    'container1' : container1,
    'container2' : container2,
    'slider' : slider,
    'combobox' : combobox,
    'label' : label,
    'button' : button,
    'circlebutton' : circlebutton,
    'sizebutton' : sizebutton,
    'togglebutton' : togglebutton,
    'textedit' : textedit,
    'lineedit' : lineedit,
    'scrollarea' : scrollarea,
    'logspeaker' : logspeaker,
    'logtalker' : logtalker,
    'loglabel' : loglabel,
    'messagebox' : messagebox,
}
