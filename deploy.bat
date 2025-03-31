@echo off
setlocal enabledelayedexpansion


:: Set library name
set LIBRARY_NAME=antools

:: Set working directory to the script's location
cd /d "%~dp0"

:: Define virtual environment directory
set VENV_DIR=venv

:: Check if virtual environment exists, if not, create it
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Upgrade pip and install necessary libraries
echo Installing required libraries...
pip install build
pip install setuptools wheel twine

:: Build the package
echo Building the package...
python -m build 

:: Install package locally for testing
echo Installing the package locally for testing...
pip uninstall -y antools
pip install .


:: Open installed library in venv (if it exists)
set LIB_PATH="%VENV_DIR%\Lib\site-packages\%LIBRARY_NAME%"
if exist %LIB_PATH% (
    echo Opening installed library folder...
    explorer %LIB_PATH%
) else (
    echo WARNING: Library folder not found inside venv.
)


:: Ask user for confirmation before uploading
set /p CONFIRM="Is everything correct? Do you want to publish? (y/N): "

if /i "%CONFIRM%"=="y" (

    :: Upload to PyPI using Twine
    echo Uploading package to PyPI...
    twine upload dist\*

    echo Deployment completed!

    :: Get antools version dynamically
    for /f %%i in ('python -c "import antools; print(antools.__version__)"') do set VERSION=%%i

    :: remove antools and do pip freeze 
    pip uninstall -y antools
    pip freeze > requirements.txt¨
    echo pip freeze > requirements.txt!

    :: commit and push to Git
    echo Committing and pushing to Git...
    git add .
    git commit -m "Published antools v%VERSION%"
    git push origin main

    echo Git push completed!


) else (
    echo Upload canceled. Please check your package before publishing.
)

endlocal