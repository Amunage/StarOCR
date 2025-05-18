import re
from difflib import SequenceMatcher
import setting

last_lines = []
MAX_HISTORY = 10


def custom_translate(new_lines):
    translated_lines = []
    # 긴 단어부터 먼저 처리
    sorted_dict = sorted(setting.custom_dict.items(), key=lambda x: -len(x[0]))
    
    for line in new_lines:
        for eng, kor in sorted_dict:
            line = re.sub(rf'\b{re.escape(eng)}\b', kor, line, flags=re.IGNORECASE)
        translated_lines.append(line)
    return translated_lines


def normalize_line(line):
    line = line.lower()
    line = re.sub(r'[^a-z0-9\s]', '', line)  # 특수문자 제거
    line = re.sub(r'\s+', ' ', line)         # 공백 정리
    return line.strip()


def is_similar(a, b):
    threshold = 0.6
    na, nb = normalize_line(a), normalize_line(b)
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def is_line_valid(line):
    line = line.strip()
    if len(line) < 4:
        return False
    alphabetic_ratio = len(re.findall(r'[A-Za-z]', line)) / len(line)
    if alphabetic_ratio < 0.6:
        return False
    if not re.search(r'[aeiouAEIOU]', line):
        return False
    return True

def clean_line(text):
    global last_lines

    # 전처리: 빈 줄 제거
    clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    current_lines = clean_text.splitlines()

    # 유효한 줄만 필터링
    valid_lines = [line for line in current_lines if is_line_valid(line)]

    # 중복 탐색
    match_index = None
    for i in range(len(valid_lines) - 1, -1, -1):
        if any(is_similar(valid_lines[i], prev) for prev in last_lines):
            match_index = i
            break

    # 신규 문장 추출
    new_sentences = valid_lines[match_index + 1:] if match_index is not None else valid_lines
    last_lines[:] = (last_lines + new_sentences)[-MAX_HISTORY:]

    custom_sentences = custom_translate(new_sentences)
    return custom_sentences