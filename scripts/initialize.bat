@echo off
setlocal enabledelayedexpansion

:: Set library name
set LIBRARY_NAME=antools

:: Set working directory to the script's location
:: cd /d "%~dp0"

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
poetry add setuptools
poetry add pre-commit
poetry lock
poetry run pre-commit clean
poetry run pre-commit install
poetry run pre-commit run --all-files


pip freeze > requirements.txt
echo pip freeze to requirements.txt
