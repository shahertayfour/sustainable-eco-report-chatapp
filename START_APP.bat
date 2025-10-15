@echo off
chcp 65001 > nul
echo.
echo ========================================
echo Sustainable Eco Report Chat App
echo ========================================
echo.
echo Starting Backend MCP Server...
echo.
start cmd /k "cd backend && py -3.12 run_server.py"
timeout /t 3 /nobreak > nul

echo Starting Frontend Flask App...
echo.
start cmd /k "cd frontend && py -3.12 flask_app_simple.py"
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo App is starting...
echo ========================================
echo.
echo Backend: http://localhost:4141/sse
echo Frontend: http://localhost:5000
echo.
echo Opening browser...
timeout /t 2 /nobreak > nul
start http://localhost:5000
echo.
echo Press any key to exit this window...
pause > nul
