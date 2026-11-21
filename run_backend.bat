@echo off
echo ========================================================
echo   Starting TRL Intelligence FastAPI Backend Server
echo   Techfest IIT Bombay 2nd APCTT Hackathon 2026
echo ========================================================

set PYTHON_CMD=python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py -3.12
)

echo Using Python launcher: %PYTHON_CMD%
echo API Docs will be available at: http://localhost:8000/docs
echo Health Check: http://localhost:8000/api/health
echo.

%PYTHON_CMD% -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
