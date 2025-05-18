import os
import sys

paths = [
    'data'
    ]

def tempPath():
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    base_path = base_path.replace('\\', '/')

    return base_path

def exePath():
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    for path in paths:
        full_path = os.path.join(base_path, path)
        sys.path.append(full_path)

    return base_path

def tesseract_path():
    base_path = tempPath()
    tessdata_path = "./tessdata"
    os.environ["TESSDATA_PREFIX"] = tessdata_path

    
    default_path = f"{base_path}/Tesseract-OCR/tesseract.exe"

    if getattr(sys, 'frozen', False):
        internal_path = os.path.join(sys._MEIPASS, "tesseract", "tesseract.exe")
        if os.path.exists(internal_path):
            return internal_path
    return default_path
