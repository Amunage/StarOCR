@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set /p user_input=# PyInstaller 빌드를 시작할까요? (Y/N): 
if /i "!user_input!" neq "Y" (
    echo # 빌드를 취소했어요
    pause
    exit /b
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

echo.
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo # PyInstaller가 없네요! 자동 설치합니다
    pip install pyinstaller
)

echo.
echo # PyInstaller 빌드 시작

pyinstaller ^
  __init__.spec

echo.
echo # 빌드 완료!
pause
