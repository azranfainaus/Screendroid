@echo off
title Screendroid

REM =====================================
REM Screendroid Startup Script
REM =====================================

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start Screendroid
python adb_proxy.py

pause