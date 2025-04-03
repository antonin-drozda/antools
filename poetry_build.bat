@echo off
setlocal enabledelayedexpansion

:: Set library name
set LIBRARY_NAME=antools

:: Set working directory to the script's location
cd /d "%~dp0"

:: Define virtual environment directory
set VENV_DIR=venv

:: Remove old builds
if exist dist\* (
echo Cleaning up old build files...
del /Q dist\*
)
poetry cache clear pypi --all
echo Old Poetry builds removed and Poetry cache cleared.

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

pause

:: Remove old builds
if exist dist\* (
echo Cleaning up old build files...
del /Q dist\*
)
poetry cache clear pypi --all
echo Old Poetry builds removed and Poetry cache cleared.


:: Ask user for confirmation before uploading
set /p CONFIRM="Do you want to publish to Pypi and push to Git? (y/N): "

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
    git commit -m "published antools v!VERSION!"
    git push

    :: Open the GitHub repository URL dynamically
    start https://github.com/antonin-drozda/%LIBRARY_NAME%

    :: Inform user to check if the branch was pushed
    echo Check that the branch was pushed.

    :: Pause to view output (optional)
    pause

    echo Please push manually ... currently working via GitHubDesktop

) else (
echo GIT commit not created
)

endlocal