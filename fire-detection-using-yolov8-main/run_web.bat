@echo off
cd /d "%~dp0"
echo Starting Fire Detection Web Application...
echo.
echo Open your browser and go to: http://localhost:5000
echo.
echo Default Login:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause

