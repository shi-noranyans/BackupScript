@echo off
setlocal

:: ????Python?????????????????????
set "installer=python-3.12.1-amd64.exe"
set "installer_url=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
set "install_dir=%USERPROFILE%\AppData\Local\Programs\Python\Python312"
set "python_scripts_dir=%install_dir%\Scripts"

:: Python ??????????????
if not exist "%installer%" (
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri '%installer_url%' -OutFile '%installer%'"
    if %errorlevel% neq 0 (
        echo Failed to download Python installer.
        pause
        exit /b 1
    )
    echo Python installer downloaded successfully.
)

:: Python ???????
echo Installing Python...
start /wait "" "%installer%" /passive InstallAllUsers=1 PrependPath=1 TargetDir="%install_dir%" /log "python_install.log"
if not exist "%install_dir%\python.exe" (
    echo Python installation failed.
    type "python_install.log"
    pause
    exit /b 1
)
echo Python installation complete.

:: PATH ???????
echo Updating PATH...
set "new_path=%python_scripts_dir%;%install_dir%;%PATH%"
setx PATH "%new_path%" /M

:: pip ????????
echo Upgrading pip...
"%install_dir%\python.exe" -m pip install --upgrade pip

:: ???????????????
if exist "requirements.txt" (
    echo Installing Python libraries...
    "%install_dir%\python.exe" -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install Python libraries.
        pause
        exit /b 1
    )
    echo Python libraries installed successfully.
) else (
    echo requirements.txt not found.
)

:: ???????
echo Setup complete. Press any key to exit.
pause

endlocal
