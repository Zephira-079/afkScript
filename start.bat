@echo off
REM Create a virtual environment in the current directory
python -m venv env

REM Change to the Scripts directory and activate the virtual environment
cd env\Scripts
call activate

REM Move back to the root directory of the project
cd ../..

REM Install the required packages from requirements.txt
pip install -r requirements.txt

REM Create a standalone executable with PyInstaller
pyinstaller --onefile afkscript.py

REM Deactivate the virtual environment
deactivate

REM Move back to the original directory
cd ..

echo Setup and build process completed.
pause
