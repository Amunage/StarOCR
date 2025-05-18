@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 사용자 정보 (최초 1회만 필요)
:: git config user.name "Amunage"
:: git config user.email "goodwin952@gmail.com"

set /p commit_msg="커밋 메시지를 입력하세요: "

:: 추적 중인 민감 파일 제거 (단, 로컬에는 그대로 유지됨)
git rm -r --cached Tesseract-OCR >nul 2>&1
git rm --cached upload_to_github.bat >nul 2>&1

:: Git 초기화 및 최초 연결 (최초 1회만 실행)
:: if not exist .git (
::     echo "# starocr" > README.md
::     git init
::     git add README.md
::     git commit -m "first commit"
::     git branch -M main
::     git remote add origin https://github.com/Amunage/starocr.git
::     git push -u origin main
:: )

echo ⚙️ 현재 git 상태:
git status

echo ▶ 변경사항 스테이징 중...
git add .

echo 📝 커밋 중...
git commit -m "%commit_msg%"

echo 🚀 GitHub로 푸시 중...
git push origin main

echo ✅ 업로드 완료! 깃허브로 출동 완료입니다~☆
pause


