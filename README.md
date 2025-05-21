## 주요 기능

- OCR 기반 채팅 번역기입니다. (Tesseract-OCR)
- 영어 → 한국어 실시간 로컬번역 ([NLLB 한국어 파인튜닝 모델 사용](https://huggingface.co/NHNDQ/nllb-finetuned-en2ko))
- 이전에 번역한 문장은 넘기고 새로 인식한 문장만 번역합니다.


## 사용 방법

- 마우스 우클릭 드래그로 화면이동, 모서리를 좌클릭으로 크기를 조절할 수 있습니다.
- 마우스 우클릭으로 메뉴를 호출합니다.
- 메뉴의 "Set Area"로 영역을 지정 후, "Start" 또는 "Snapshot"을 실행합니다.
- 메뉴의 "Stop"으로 번역을 중지합니다.


## 메뉴 설명

- "Start/Stop": 실시간 번역을 시작/중지합니다.
- "Snapshot": 한 번만 번역을 실행합니다.
- "Set Area": 번역 할 영역을 지정합니다.
- "Preview": OCR이 어떻게 보이고 있는지 이미지를 확인할 수 있습니다.
- "Preferences": 폰트, Tesseract, 투명도, 성능옵션을 조절할 수 있습니다.
- "Exit": 프로그램을 종료합니다.


## 기타 기능

- Tesseract eng: 더 정확하지만 속도는 느립니다. eng-fast: 인식률은 조금 낮지만 속도가 빠릅니다.
- "./data/custom_dict.json" 을 편집하여 고유어 교정사전을 만들 수 있습니다.


## 기타 정보

- 소스코드의 경우 `./Tesseract-OCR`이 필요합니다.
- https://github.com/tesseract-ocr/tesseract
