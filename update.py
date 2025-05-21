import requests
from packaging import version

CURRENT_VERSION = "1.0.3"
GITHUB_USER = "Amunage"
GITHUB_REPO = "StarOCR"

def request_version():
    try:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version = data['tag_name'].lstrip("v")  # ex: "v1.2.0" → "1.2.0"
            
            return latest_version
    except Exception as e:
        print("⚠️ 업데이트 확인 실패:", e)
    return None

def check_update():
    release_version = request_version()
    try:
        if version.parse(release_version) > version.parse(CURRENT_VERSION):
            text = f"Available Update : v{release_version}"
        else:
            text = f"You're using the latest version."
    except Exception as e:
        return f"❌ Failed checking update : {e}"
    return text
