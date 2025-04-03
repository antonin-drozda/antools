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
pip install poetry
poetry init
poetry install

:: Remove all files in the dist/ directory
del /Q dist\*

:: Optional: Clear the Poetry cache (remove old cached packages)
poetry cache clear pypi --all

:: Optionally, you can add a message or pause to indicate completion
echo Old Poetry builds removed and Poetry cache cleared.

:: Build the package
echo Building the package...
poetry build

:: Install package locally for testing
echo Installing the package locally for testing...
pip uninstall -y %LIBRARY_NAME%
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
set /p CONFIRM="Do you want to publish to PyPI? (y/N): "

:: Check if the user confirmed with 'y' or 'Y'
if /i "%CONFIRM%"=="y" (

    :: Upload to PyPI using Poetry's built-in publish command
    echo Uploading package to PyPI...

    :: Use Poetry to publish
    poetry publish --build

    :: Open the URL in the default browser
    start https://pypi.org/project/%LIBRARY_NAME%/#history

    :: Inform the user about checking the upload
    echo Check that package was uploaded correctly.

    :: Pause to view output (optional)
    pause

    :: Provide additional help if the user needs to set the token
    echo If not working, call: poetry config pypi-token.pypi YOUR_TOKEN

    :: Inform about deployment completion
    echo Deployment completed!

) else (
    echo Upload canceled. Please check your package before publishing.
)

set /p CONFIRM="Do you want to create commit to Git? (y/N): "

if /i "%CONFIRM%"=="y" (

    :: Get library version dynamically
    cd dist

    :: Get the first .whl or .tar.gz file (assuming only one file is generated)
    for %%f in (*.whl *.tar.gz) do (
        set "package_file=%%f"
        goto :found
    )

    :found
    :: Extract the version number from the filename (e.g., "your_package-0.1.0-py3-none-any.whl")
    for /f "tokens=2 delims=-" %%v in ("%package_file%") do (
        set "version=%%v"
    )

    :: Display the version (or use it further in your script)
    echo Version: %version%
    cd /d "%~dp0"

    :: Remove library and update requirements.txt
    pip uninstall -y %LIBRARY_NAME%
    pip freeze > requirements.txt
    echo Updated requirements.txt!

   :: Commit and push to Git
    echo Creating Git commit ...
    git add .
    git commit -m "published %LIBRARY_NAME% v !version!"
    git push

    :: Open the GitHub repository URL dynamically with the LIBRARY_NAME
    start https://github.com/antonin-drozda/%LIBRARY_NAME%

    :: Inform user to check if the branch was pushed
    echo Check that the branch was pushed
    pause
        

) else (
    echo GIT commit not created
)

endlocal
