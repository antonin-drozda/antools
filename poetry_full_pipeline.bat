@echo off
setlocal enabledelayedexpansion

:: ========================================
:: Setup and Virtual Environment Creation
:: ========================================

:: Set the library name to be used in the process
set LIBRARY_NAME=antools

:: Set the working directory to the script's location
cd /d "%~dp0"

:: Define the directory for the virtual environment
set VENV_DIR=venv

:: Check if the virtual environment already exists; if not, create it
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"

:: ===========================================
:: Upgrade Pip and Install Dependencies
:: ===========================================

:: Upgrade pip to ensure it is the latest version
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install Poetry and other required dependencies
echo Installing required libraries...
pip install poetry
poetry init
poetry install

:: ===========================================
:: Clean Old Builds and Clear Cache
:: ===========================================

:: Remove all files in the dist/ directory (old builds)
del /Q dist\*

:: Optional: Clear the Poetry cache (remove old cached packages)
poetry cache clear pypi --all

:: Inform the user that old builds were removed and the cache cleared
echo Old Poetry builds removed and Poetry cache cleared.

:: ===========================================
:: Build and Install the Package Locally
:: ===========================================

:: Build the package using Poetry
echo Building the package...
poetry build

:: Install the package locally for testing
echo Installing the package locally for testing...
pip uninstall -y antools
pip install .

:: Open installed library in the virtual environment (if it exists)
set LIB_PATH="%VENV_DIR%\Lib\site-packages\%LIBRARY_NAME%"
if exist "!LIB_PATH!" (
    echo Opening installed library folder...
    explorer "!LIB_PATH!"
) else (
    echo WARNING: Library folder not found inside venv.
)

:: ===========================================
:: Publish to PyPI (User Confirmation)
:: ===========================================

:: Ask the user for confirmation before uploading to PyPI
set /p CONFIRM="Do you want to publish to PyPI? (y/N): "

:: If the user confirmed with 'y' or 'Y', upload to PyPI
if /i "!CONFIRM!"=="y" (

    :: Upload the package to PyPI using Poetry's built-in publish command
    echo Uploading package to PyPI...

    :: Use Poetry to publish the package
    poetry publish --build

    :: Open the URL in the default browser to check the upload
    start https://pypi.org/project/antools/#history

    :: Inform the user to check that the upload was successful
    echo Check that the package was uploaded correctly.

    :: Pause the script to allow the user to view the output (optional)
    pause

    :: Provide additional instructions for the user if the upload fails (set token)
    echo If not working, call: poetry config pypi-token.pypi <YOUR_TOKEN>

    :: Inform the user that deployment is complete
    echo Deployment completed!

) else (
    :: If the user cancels, inform them about the cancellation
    echo Upload canceled. Please check your package before publishing.
)

:: ===========================================
:: Git Commit (User Confirmation)
:: ===========================================

:: Ask the user if they want to create a commit to Git
set /p CONFIRM="Do you want to create a commit to Git? (y/N): "

if /i "!CONFIRM!"=="y" (

    :: Navigate to the dist directory to find the generated package file
    cd dist

    :: Get the first .whl or .tar.gz file (assuming only one file is generated)
    for %%f in (*.whl *.tar.gz) do (
        set "package_file=%%f"
        goto :found
    )

    :found
    :: Extract the version number from the filename (e.g., "antools-0.1.0-py3-none-any.whl")
    for /f "tokens=2 delims=-" %%v in ("!package_file!") do (
        set "version=%%v"
    )

    :: Display the extracted version number
    echo Version: !version!
    
    :: Return to the script's original directory
    cd /d "%~dp0"

    :: Uninstall the previous version of the package and update the requirements.txt
    pip uninstall -y antools
    pip freeze > requirements.txt
    echo Updated requirements.txt!

    :: Commit and push to Git
    echo Creating Git commit ...
    git add .
    git commit -m "published antools v !version!"
    git push
    echo Please push manually... currently working via GitHub Desktop

) else (
    :: If the user cancels Git commit, inform them
    echo GIT commit not created
)

:: End of script
endlocal
