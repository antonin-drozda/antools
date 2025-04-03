@echo off
setlocal enabledelayedexpansion

:: Set library name
set LIBRARY_NAME=antools

:: Set working directory to the script's location
cd /d "%~dp0"

:: Define virtual environment directory
set VENV_DIR=venv

:: Ask user for confirmation before uploading
set /p CONFIRM="Do you want to publish to PyPI and push to Git? (y/N): "

if /i "%CONFIRM%"=="y" (
    
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

    :: Get library version dynamically from the first file found in dist/
    cd dist

    :: Find the first .whl or .tar.gz file (assuming only one file will be processed)
    for %%f in (*.whl *.tar.gz) do (
        set "package_file=%%f"
        goto :found
    )

    :found
    :: Extract the version number from the filename (e.g., "your_package-0.1.0-py3-none-any.whl")
    for /f "tokens=2 delims=-" %%v in ("!package_file!") do (
        set "version=%%v"
    )

    :: Display the extracted version
    echo Version: !version!

    :: Return to the original script directory
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
    echo Commit successfully pushed to GitHub.

    :: Open the GitHub repository URL dynamically
    start https://github.com/antonin-drozda/%LIBRARY_NAME%

    :: Inform user to check if the branch was pushed
    echo Check that the branch was pushed.

    :: Pause to view output (optional)
    pause


) else (
    echo Aborted.
)

:: End of script
endlocal
