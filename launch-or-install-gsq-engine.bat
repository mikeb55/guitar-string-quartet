@echo off
setlocal

title Launch Guitar-String-Quartet Engine

cd /d "%~dp0"

echo Checking for Python...
where python >nul 2>nul
if %errorlevel%==0 goto launch

where py >nul 2>nul
if %errorlevel%==0 goto launch_py

echo.
echo Python not found.
echo Attempting install via winget...
echo.

where winget >nul 2>nul
if not %errorlevel%==0 (
    echo winget is not available on this system.
    echo Install Python manually, then re-run this launcher.
    pause
    exit /b 1
)

winget install -e --id Python.Python.3 --accept-package-agreements --accept-source-agreements

echo.
echo Re-checking Python...
where python >nul 2>nul
if %errorlevel%==0 goto launch

where py >nul 2>nul
if %errorlevel%==0 goto launch_py

echo.
echo Python still not available.
echo You may need to restart Windows or sign out and back in.
pause
exit /b 1

:launch
echo Launching GUI...
start "" pythonw "%~dp0launch_gsq_engine_gui.py"
if %errorlevel% neq 0 (
    echo pythonw failed, trying python...
    python "%~dp0launch_gsq_engine_gui.py"
)
exit /b 0

:launch_py
echo Launching GUI...
start "" pyw "%~dp0launch_gsq_engine_gui.py"
if %errorlevel% neq 0 (
    echo pyw failed, trying py...
    py "%~dp0launch_gsq_engine_gui.py"
)
exit /b 0