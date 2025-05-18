import mss
from PIL import Image, ImageEnhance

import numpy as np

import setting

def capture_monitor():
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # 0번 = 전체 모니터 모두
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

        # 이미지 어둡게 조절
        enhancer = ImageEnhance.Brightness(img)
        darken_factor = 0.8
        dark_img = enhancer.enhance(darken_factor)

        return dark_img

def capture_area():
    data = setting.userdata
    area = data.get("ocrarea", None)
    if not area:
        raise ValueError("저장된 OCR 영역이 없어요!")

    x, y, w, h = area

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": w, "height": h}
        sct_img = sct.grab(monitor)

    img_np = np.array(sct_img)

    return img_np
