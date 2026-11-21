@echo off
echo ========================================================
echo   Running TRL Intelligence Unit & Integration Tests
echo   Techfest IIT Bombay 2nd APCTT Hackathon 2026
echo ========================================================

set PYTHON_CMD=python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py -3.12
)

%PYTHON_CMD% -m unittest discover -s backend/tests -v
pause
