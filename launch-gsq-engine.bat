@echo off
cd /d "%~dp0"

where mshta >nul 2>&1
if %errorlevel% equ 0 (
    mshta "%~dp0launch-gsq-engine.hta"
) else (
    echo mshta.exe is not available.
    echo The launcher requires Windows with Internet Explorer components.
    pause
)
