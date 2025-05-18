from transformers import pipeline
import torch
import os

import setting

setting.load_userdata()
thread_count = setting.userdata.get("performence", 1)
print(f"Thread Count : {thread_count}")

os.environ["OMP_NUM_THREADS"] = f"{thread_count}"
os.environ["MKL_NUM_THREADS"] = f"{thread_count}"
torch.set_num_threads(thread_count)
torch.set_num_interop_threads(thread_count)

# import psutil
# p = psutil.Process(os.getpid())
# p.cpu_affinity([0])

# GPU 제한 (있는 경우)
if torch.cuda.is_available():
    torch.cuda.set_per_process_memory_fraction(0.5, 0)


translator = pipeline(
    'translation',
    model='NHNDQ/nllb-finetuned-en2ko',
    device = "cuda" if torch.cuda.is_available() else "cpu",
    src_lang='eng_Latn',
    tgt_lang='kor_Hang',
    max_length=128,
    do_sample=False,  # greedy decoding
    num_beams=1,      # 빔서치 비활성화
)

def run_translation(text):
    output = translator(text)
    translatedText = output[0]['translation_text']
    return translatedText


# 테스트용
# if __name__ == "__main__":
#     import time
#     print("🔁 테스트 (종료하려면 'exit' 입력)")
#     while True:
#         text = input("입력: ")
#         if text.lower() == "exit":
#             break
#         start_time = time.time()
#         result = run_translation(text)
#         print("🈯 결과:", result)
#         end_time = time.time()
#         elapsed = round(end_time - start_time, 3)
#         print(f"🕒 소요 시간: {elapsed}초")
