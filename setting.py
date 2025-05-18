import json
import os

user_path = f"./data/user.json"
custom_dict_path = f"./data/custom_dict.json"

userdata = {}
custom_dict = {}


def load_userdata():
    global user_path, userdata

    if not os.path.exists(user_path):
        print("⚠️ user.json 파일이 없어요!")
        userdata = {}
        return userdata
    try:
        with open(user_path, "r", encoding="utf-8") as f:
            userdata = json.load(f)
            return userdata
        
    except json.JSONDecodeError:
        print("⚠️ user.json 파일이 손상되었어요!")
        userdata = {}
        return userdata


def save_userdata(data):
    global user_path, userdata
    try:
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        load_userdata()
        print("✔️ 설정이 저장되었어요!")
    except Exception as e:
        print(f"❌ 저장 중 오류 발생: {e}")


def load_custom_dict():
    global custom_dict_path, custom_dict

    if not os.path.exists(custom_dict_path):
        print("⚠️ custom_dict.json 파일이 없어요!")
        custom_dict = {}
        return custom_dict
    try:
        with open(custom_dict_path, "r", encoding="utf-8") as f:
            custom_dict = json.load(f)
            return custom_dict
        
    except json.JSONDecodeError:
        print("⚠️ custom_dict.json 파일이 손상되었어요!")
        custom_dict = {}
        return custom_dict