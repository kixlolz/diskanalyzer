@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================
echo   diskanalyzer - one-click launcher
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found on PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [..] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 ( echo [ERROR] Failed to create venv. & pause & exit /b 1 )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

echo [..] Installing diskanalyzer (editable)...
".venv\Scripts\python.exe" -m pip install -e . --quiet --disable-pip-version-check
if errorlevel 1 ( echo [ERROR] pip install failed. & pause & exit /b 1 )
echo [OK] diskanalyzer installed.

echo.
set /p TARGET="Directory to scan (leave blank for current folder): "
if "%TARGET%"=="" set TARGET=.

echo.
echo ============================================
echo   Scanning: %TARGET%
echo ============================================
echo.
echo [1] TUI (interactive tree)
echo [2] Plain table (top 15)
echo [3] Exit
echo.
set /p CHOICE="Pick 1-3 and press Enter: "

if "%CHOICE%"=="1" (
    ".venv\Scripts\diskanalyzer.exe" "%TARGET%"
    goto end
)
if "%CHOICE%"=="2" (
    ".venv\Scripts\diskanalyzer.exe" "%TARGET%" --plain --top 15
    pause
    goto end
)
goto end

:end
echo.
pause