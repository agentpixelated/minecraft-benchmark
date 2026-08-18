@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-windows.ps1" %*
set CODE=%ERRORLEVEL%
echo.
if not "%CODE%"=="0" echo Benchmark failed with exit code %CODE%.
pause
exit /b %CODE%
