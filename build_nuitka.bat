@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion


set /p DELETE_CACHE=# 이전 Nuitka 빌드 캐시를 삭제하시겠어요? (Y/N): 
if /i "%DELETE_CACHE%"=="Y" (
    echo # 캐시 삭제 중...
    rmdir /s /q ".nuitka-cache"
    rmdir /s /q "%LOCALAPPDATA%\Nuitka\Nuitka\Cache"
    echo # 캐시 삭제 완료!
)

echo.
set /p venv_name=# 사용할 가상환경 폴더명을 입력해주세요 (예: testvenv): 
set venv_path=!venv_name!\Scripts\activate.bat

if not exist "!venv_path!" (
    echo # 해당 가상환경이 존재하지 않아요: !venv_path!
    pause
    exit /b
)

powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned"
call "!venv_path!"


pip show nuitka >nul 2>&1
if errorlevel 1 (
    echo.
    echo Nuitka가 없네요! 자동 설치합니다
    pip install nuitka
)

:: 여기서부터 빌드 시작
echo.
set /p USER_INPUT=# Nuitka 빌드를 시작할까요? (Y/N): 
if /i "!USER_INPUT!" neq "Y" (
    echo # 빌드를 취소했어요!
    pause
    exit /b
)

echo.
echo # Nuitka 빌드 시작!

nuitka ^
  __init__.py ^
  --standalone ^
  --output-dir=dist ^
  --output-filename=StarOCR ^
  --windows-icon-from-ico=./data/scricon.ico ^
  --enable-plugin=pyqt5 ^
  --include-data-dir=./data=data ^
  --include-data-dir=./Tesseract-OCR=tesseract ^
  --nofollow-import-to=tkinter,test,torchvision,matplotlib,torch_tb_profiler ^
  --noinclude-default-mode=error ^
  --lto=no ^
  --remove-output ^
  --assume-yes-for-downloads ^
  --windows-console-mode=disable ^
  --mingw64 ^
  --jobs=12

echo # 빌드 완료!
pause
