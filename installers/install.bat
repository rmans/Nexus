@echo off
REM Nexus installation script for Windows

setlocal enabledelayedexpansion

REM Colors (Windows doesn't support ANSI colors in batch, so we'll use text)
set "INFO=[INFO]"
set "SUCCESS=[SUCCESS]"
set "WARNING=[WARNING]"
set "ERROR=[ERROR]"

echo 🚀 Nexus Installer for Windows
echo ==============================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Python is required but not installed.
    echo %INFO% Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo %SUCCESS% Python found

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% pip is required but not installed.
    echo %INFO% Please install pip and try again.
    pause
    exit /b 1
)

echo %SUCCESS% pip found

REM Install Nexus
echo %INFO% Installing Nexus with hybrid configuration system...

REM Try PyPI installation first
pip install nexus-context --user
if errorlevel 1 (
    echo %WARNING% PyPI installation failed, trying local installation...
    
    REM Get script directory
    set "SCRIPT_DIR=%~dp0"
    
    REM Install from source
    if exist "%SCRIPT_DIR%setup.py" (
        pip install "%SCRIPT_DIR%" --user
        if errorlevel 1 (
            echo %ERROR% Local installation failed
            pause
            exit /b 1
        )
        echo %SUCCESS% Nexus installed from source
    ) else (
        echo %ERROR% Could not find setup.py for local installation
        pause
        exit /b 1
    )
) else (
    echo %SUCCESS% Nexus installed from PyPI
)

REM Set up PATH
echo %INFO% Setting up PATH...

REM Add %USERPROFILE%\AppData\Roaming\Python\Python3x\Scripts to PATH
for /f "tokens=2 delims=." %%i in ('python -c "import sys; print(sys.version_info.major, sys.version_info.minor)"') do set PYTHON_VERSION=%%i

set "PYTHON_SCRIPTS=%USERPROFILE%\AppData\Roaming\Python\Python%PYTHON_VERSION%\Scripts"
set "PYTHON_SCRIPTS_ALT=%USERPROFILE%\AppData\Roaming\Python\Python%PYTHON_VERSION%x\Scripts"

REM Check if the directory exists
if exist "%PYTHON_SCRIPTS%" (
    set "SCRIPTS_DIR=%PYTHON_SCRIPTS%"
) else if exist "%PYTHON_SCRIPTS_ALT%" (
    set "SCRIPTS_DIR=%PYTHON_SCRIPTS_ALT%"
) else (
    echo %WARNING% Could not find Python Scripts directory
    echo %INFO% You may need to add the Scripts directory to your PATH manually
    goto :verify
)

REM Add to PATH if not already there
echo %PATH% | find /i "%SCRIPTS_DIR%" >nul
if errorlevel 1 (
    setx PATH "%PATH%;%SCRIPTS_DIR%" >nul
    echo %SUCCESS% Added Python Scripts to PATH
    echo %WARNING% Please restart your command prompt for PATH changes to take effect
) else (
    echo %SUCCESS% Python Scripts already in PATH
)

:verify
REM Verify installation
echo %INFO% Verifying installation...

REM Check if nexus command is available
where nexus >nul 2>&1
if errorlevel 1 (
    echo %WARNING% Nexus command not found in PATH
    echo %INFO% You may need to restart your command prompt
    echo %INFO% Or run: %SCRIPTS_DIR%\nexus.exe
) else (
    echo %SUCCESS% Nexus command found
    
    REM Test basic functionality
    nexus --version >nul 2>&1
    if errorlevel 1 (
        echo %WARNING% Nexus installed but may have issues
    ) else (
        echo %SUCCESS% Nexus is working correctly
    )
)

echo.
echo %SUCCESS% Installation complete!
echo.
echo Next steps:
echo 1. Restart your command prompt
echo 2. Run 'nexus init-project' to create a new project
echo 3. Run 'nexus status' to check the installation
echo 4. Run 'nexus --help' for more information
echo.
echo %INFO% For documentation, visit: https://github.com/rmans/Nexus

pause
