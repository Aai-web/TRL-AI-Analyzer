@echo off
echo ========================================================
echo   Running TRL Intelligence ML Model Training Pipeline
echo   Techfest IIT Bombay 2nd APCTT Hackathon 2026
echo ========================================================

set PYTHON_CMD=python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py -3.12
)

%PYTHON_CMD% -m backend.app.ml.train
pause
