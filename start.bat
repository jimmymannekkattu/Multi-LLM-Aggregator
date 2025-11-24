@echo off
REM AI Nexus - Windows Launcher
REM This script launches AI Nexus on Windows systems

echo ====================================
echo   AI Nexus - Starting (Windows)
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.8+ is required but not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Run the cross-platform launcher
python start.py

pause
