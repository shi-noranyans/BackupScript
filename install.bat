@echo off
setlocal

:: バッチファイルが置かれているディレクトリに移動
cd /d "%~dp0"

echo Step 1: Changed directory to batch file location.
pause

:: Pythonの最新版のURLを取得する
echo Fetching the latest Python version...
for /f "tokens=*" %%i in ('powershell -Command "(Invoke-WebRequest -Uri 'https://www.python.org/downloads/windows/').Content -match 'https://www.python.org/ftp/python/[\d\.]+/python-[\d\.]+-amd64.exe' | Out-Null; $matches[0]"') do set "installer_url=%%i"

if not defined installer_url (
    echo Failed to retrieve the latest Python version.
    pause
    exit /b 1
)

echo Step 2: Latest Python installer URL is %installer_url%.
pause

:: インストーラファイル名を抽出
for /f "tokens=*" %%i in ('powershell -Command "$url='%installer_url%'; $url.Substring($url.LastIndexOf('/')+1)"') do set "installer=%%i"

echo Step 3: Installer file name is %installer%.
pause

:: Pythonインストーラをダウンロード
if not exist "%installer%" (
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri '%installer_url%' -OutFile '%installer%'"
    if %errorlevel% neq 0 (
        echo Failed to download Python installer.
        pause
        exit /b 1
    )
    echo Python installer downloaded successfully.
    pause
)

:: インストール先ディレクトリを設定
set "install_dir=%USERPROFILE%\AppData\Local\Programs\Python\PythonLatest"
set "python_scripts_dir=%install_dir%\Scripts"

echo Step 4: Installing Python to %install_dir%.
pause

