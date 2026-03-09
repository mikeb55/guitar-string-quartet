@echo off
REM Run composition file organiser
REM Moves loose files into correct composition folders and updates _index.md
cd /d "%~dp0"
py scripts\organise-compositions.py
pause
