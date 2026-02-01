@echo off
TITLE SOPHIA 5.0 - INCARNATE LAUNCHER

REM Change to the script's directory
cd /d "%~dp0"

REM Run launcher directly (batch file is already in a terminal)
python launch_sophia.py
pause
