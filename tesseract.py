import pytesseract
import cv2
from collections import defaultdict
import re
from capture import capture_area
from cleaner import clean_line
from setting import user_data

import datapath
pytesseract.pytesseract.tesseract_cmd = datapath.tesseract_path()
pytesseract.pytesseract.get_errors = lambda _: ""  # 에러 출력을 무시해버림!


# 기존 OCR 품질 평가 기준
def evaluate_ocr_quality(text):
    words = text.split()
    alpha_words = [w for w in words if re.search(r'[a-zA-Z]', w)]
    return len(alpha_words)



# 여러 전처리 방식 정의
def preprocess_variants(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = []

    thresholds = [80, 120, 160, 200]
    for t in thresholds:
        _, bin_img = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
        results.append((t, bin_img))

    return results


# OCR + 평균 신뢰도 기반 텍스트 추출
def extract_lines_with_avg_conf(img, lang, min_confidence=70):
    data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
    lines = defaultdict(list)
    confs = defaultdict(list)

    for i in range(len(data['text'])):
        line_id = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
        text = data['text'][i].strip()
        if text:
            lines[line_id].append(text)
            try:
                conf = int(data['conf'][i])
            except (ValueError, TypeError):
                conf = 0
            confs[line_id].append(conf)

    full_lines = []
    for line_id, words in lines.items():
        if len(confs[line_id]) == 0:
            continue
        avg_conf = sum(confs[line_id]) / len(confs[line_id])
        if avg_conf >= min_confidence:
            full_lines.append(" ".join(words))

    return "\n".join(full_lines)


# 최적 전처리 이미지 선택
def auto_preprocess_and_ocr(image):
    lang = user_data.get("eng", "eng")

    best_score = -1
    best_text = ""
    best_image = None
    best_threshold = None

    resize_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    for method, processed in preprocess_variants(resize_image):
        raw_text = extract_lines_with_avg_conf(processed, lang)
        score = evaluate_ocr_quality(raw_text)
        if score > best_score:
            best_score = score
            best_text = raw_text
            best_image = processed
            best_threshold = method
    # print(f"최적 임계값: {best_threshold}")
    return best_text, best_image

# 최종 OCR 호출 함수
def capture_and_ocr():
    img = capture_area()
    text = auto_preprocess_and_ocr(img)[0]
    new_sentences = clean_line(text)
    
    return new_sentences  # 이제 리스트 형태 반환


# 최적 이미지 호출
def best_image_for_ocr():
    img = capture_area()
    best_image = auto_preprocess_and_ocr(img)[1]

    return best_image