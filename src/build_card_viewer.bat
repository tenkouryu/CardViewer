@echo off
REM MTG Card Viewer - Build Windows Executable
REM This script builds the MTG Card Viewer into a standalone Windows executable

cd /d "%~dp0"

echo.
echo ============================================
echo MTG Card Viewer - Building Executable
echo ============================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Error: PyInstaller is not installed.
    echo Please run: python -m pip install -r requirements-build.txt
    pause
    exit /b 1
)

echo Building MTG Card Viewer...
echo.

REM Build the executable
python -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name MTGCardViewerApp ^
    --distpath "..\release" ^
    --workpath "..\build\card_viewer" ^
    --specpath "..\build" ^
    --add-data "..\mtg_card_viewer.html;." ^
    mtg_card_viewer.py

if errorlevel 1 (
    echo.
    echo Build failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build successful!
echo ============================================
echo.
echo Executable location:
echo   ..\release\MTGCardViewerApp.exe
echo.
echo To run the app:
echo   1. Navigate to the release folder
echo   2. Double-click MTGCardViewerApp.exe
echo.
pause
