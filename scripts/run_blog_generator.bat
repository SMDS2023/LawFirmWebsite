@echo off
REM Blog Topic Generator - Daily Run
REM Schedule this with Windows Task Scheduler to run daily at 6:00 AM
REM
REM Task Scheduler Setup:
REM 1. Open Task Scheduler (taskschd.msc)
REM 2. Create Basic Task > Name: "Blog Topic Generator"
REM 3. Trigger: Daily at 6:00 AM
REM 4. Action: Start a program
REM 5. Program: C:\Users\jeff\OneDrive\Documents\LotterLaw\Website\scripts\run_blog_generator.bat
REM 6. Start in: C:\Users\jeff\OneDrive\Documents\LotterLaw\Website

setlocal enabledelayedexpansion

set SCRIPT_DIR=C:\Users\jeff\OneDrive\Documents\LotterLaw\Website
set LOG_DIR=%SCRIPT_DIR%\output\blog_suggestions\logs
set LOG_FILE=%LOG_DIR%\run_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

REM Create log directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

cd /d "%SCRIPT_DIR%"

echo ================================================ >> "%LOG_FILE%" 2>&1
echo Blog Topic Generator - %date% %time% >> "%LOG_FILE%" 2>&1
echo ================================================ >> "%LOG_FILE%" 2>&1

python scripts\blog_topic_generator.py --days 30 >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo. >> "%LOG_FILE%" 2>&1
    echo SUCCESS: Topics generated successfully >> "%LOG_FILE%" 2>&1
) else (
    echo. >> "%LOG_FILE%" 2>&1
    echo ERROR: Script failed with error code %ERRORLEVEL% >> "%LOG_FILE%" 2>&1
)

echo ================================================ >> "%LOG_FILE%" 2>&1
echo Completed: %date% %time% >> "%LOG_FILE%" 2>&1
echo ================================================ >> "%LOG_FILE%" 2>&1

endlocal
