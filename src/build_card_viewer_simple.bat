@echo off
REM Simple build script - one-click build
cd /d "%~dp0"
python -m PyInstaller --noconfirm --onefile --windowed --name MTGCardViewerApp --distpath "..\release" --workpath "..\build\card_viewer" --specpath "..\build" --add-data "..\mtg_card_viewer.html;." mtg_card_viewer.py
if %errorlevel%==0 (echo. & echo Build complete! & pause) else (echo Build failed! & pause)
