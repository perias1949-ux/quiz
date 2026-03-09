@echo off
echo ==============================================
echo Building Quiz Video Generator Desktop App...
echo ==============================================

echo 1. Activating Virtual Environment...
call venv\Scripts\activate.bat

echo 2. Installing requirements (including pywebview & pyinstaller)...
pip install -r requirements.txt

echo 3. Compiling the application into an .exe...
REM We include the templates and static folders explicitly so PyInstaller bundles the frontend
pyinstaller --name "QuizVideoGenerator" --noconfirm --onedir --windowed --add-data "templates;templates" --add-data "app;app" --add-data "database;database" --add-data "modules;modules" desktop_app.py

echo ==============================================
echo Build Complete!
echo You can find your app inside the "dist\QuizVideoGenerator" folder.
echo Just double-click "QuizVideoGenerator.exe" to run it like a normal PC app!
echo ==============================================
pause
