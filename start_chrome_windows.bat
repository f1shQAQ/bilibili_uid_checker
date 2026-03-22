@echo off
echo ============================================
echo   Chrome Debug Mode Launcher [Windows]
echo ============================================
echo.

set "CHROME_PATH="
set "TEMP_PROFILE=%TEMP%\chrome_temp_profile"

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" if not defined CHROME_PATH set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if not defined CHROME_PATH (
    echo [X] Chrome not found!
    echo     Please edit this script and set CHROME_PATH manually.
    pause
    exit /b 1
)

echo [*] Chrome: %CHROME_PATH%

if exist "%TEMP_PROFILE%" rd /s /q "%TEMP_PROFILE%" 2>nul

echo [*] Starting Chrome with debug port 9222 ...
echo.

start "" "%CHROME_PATH%" --remote-debugging-port=9222 --no-first-run --no-default-browser-check --user-data-dir="%TEMP_PROFILE%"

echo [OK] Chrome started!
echo.
echo [i] Now run in another terminal: python bilibili_uid_checker.py
echo.
pause
