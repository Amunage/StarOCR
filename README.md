## 주요 기능

- OCR 기반 채팅 번역기입니다.
- 영어 → 한국어 실시간 로컬번역 ([NLLB 모델 사용](https://huggingface.co/facebook/nllb-200-distilled-600M))
- 이전에 번역한 문장은 넘기고 새로 인식한 문장만 번역합니다.


## 사용 방법

- 마우스 우클릭으로 메뉴 호출
- 마우스 우클릭 드래그로 화면이동, 모서리를 좌클릭으로 크기를 조절할 수 있습니다.
- "Set Area": 번역할 영역을 지정합니다.
- "Start": 실시간 번역을 시작합니다.
- "Snapshot": 한번만 번역을 할 수 있습니다.
- "Preview": OCR이 어떻게 보이고 있는지 이미지를 확인할 수 있습니다.
- "Preference": 폰트, 번역주기, 투명도를 조절할 수 있습니다.
- "./data/custom_dict.json" 을 편집하여 고유어 교정사전을 만들 수 있습니다.



## 기타 정보

- 소스코드의 경우 `./Tesseract-OCR`이 필요합니다.
- https://github.com/tesseract-ocr/tesseract
