@echo off
REM Party Pool Setup Script for Windows
REM This script sets up the Party Pool chat application on Windows

echo.
echo ====================================================
echo   Party Pool - Windows Setup Script
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/3] Python found. Installing dependencies...
echo.

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install packages
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo [2/3] Dependencies installed successfully!
echo.
echo [3/3] Setup complete!
echo.
echo ====================================================
echo   Setup Complete!
echo ====================================================
echo.
echo To start Party Pool, run:
echo   python main.py
echo.
echo To activate the virtual environment in future sessions:
echo   venv\Scripts\activate
echo.
pause
