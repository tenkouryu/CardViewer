@echo off
chcp 65001 >nul
cd /d "%~dp0"
python mtg_card_viewer.py
pause
