@echo off
setlocal

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found. Please ensure it is in the same directory as this script.
    exit /b 1
)

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies from requirements.txt. Please check the file and try again.
    exit /b 1
)

REM Check if Ollama is installed (optional if already in requirements.txt)
python -c "import ollama" >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is not installed. Installing Ollama...
    pip install ollama
    if %errorlevel% neq 0 (
        echo Failed to install Ollama. Please check your Python and pip installations.
        exit /b 1
    )
)

REM Run server.py
echo Running server.py...
start python server.py
if %errorlevel% neq 0 (
    echo Failed to run server.py.
    exit /b 1
)

REM Run client.py
echo Running client.py...
start python client.py
if %errorlevel% neq 0 (
    echo Failed to run client.py.
    exit /b 1
)

echo Both scripts are running.
endlocal
