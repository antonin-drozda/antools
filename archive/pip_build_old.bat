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
set /p CONFIRM="Do you want to publish to Pypi? (y/N): "

if /i "%CONFIRM%"=="y" (

    :: Upload to PyPI using Twine
    echo Uploading package to PyPI...
    echo Can be found in BitWarden for PyPI. Paste with shift+ctrl+v!
    twine upload dist\*

    echo Deployment completed!

) else (
    echo Upload canceled. Please check your package before publishing.
)

set /p CONFIRM="Do you want to create commit to Git? (y/N): "

if /i "%CONFIRM%"=="y" (

    :: Get antools version dynamically
    for /f %%i in ('python -c "import antools; print(antools.__version__)"') do (
        set VERSION=%%i
    )
    echo Detected antools version: !VERSION!

    :: Remove antools and update requirements.txt
    pip uninstall -y antools
    pip freeze > requirements.txt
    echo Updated requirements.txt!

    :: Commit and push to Git
    echo Creating Git commit ...
    git add .
    git commit -m "Published antools v!VERSION!"
    git push

) else (
echo GIT commit not created
)


endlocal