@echo off
cd /d "%~dp0"

where mshta >nul 2>&1
if %errorlevel% equ 0 (
    mshta.exe "%~dp0launch-gsq-engine.hta"
) else (
    echo mshta.exe is not available.
    echo Please run launch-gsq-engine.hta directly by double-clicking it.
    pause
)
