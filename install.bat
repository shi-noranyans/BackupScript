@echo off
setlocal

:: バッチファイルの場所にディレクトリを変更
cd /d "%~dp0"

:: PowerShellを使用して最新のPythonインストーラーURLを取得
powershell -Command "$content = Invoke-WebRequest -Uri 'https://www.python.org/downloads/windows/'; $regex = [regex] 'https://www.python.org/ftp/python/[\d\.]+/python-[\d\.]+-amd64.exe'; $matches = $regex.Match($content.Content); if ($matches.Success) { $matches.Value } else { 'No match found' }" > url.txt
set /p installer_url=<url.txt

:: URLが正常に取得されたか確認
if "%installer_url%"=="No match found" (
    echo 最新のPythonバージョンを取得できませんでした。
    pause
    exit /b 1
)

:: URLからファイル名を抽出
for %%i in ("%installer_url%") do set filename=%%~nxi

:: Pythonインストーラーを一時フォルダにダウンロード
set temp_dir=%TEMP%
set installer_path=%temp_dir%\%filename%
echo Pythonインストーラーをダウンロード中...
powershell -Command "Invoke-WebRequest -Uri '%installer_url%' -OutFile '%installer_path%' -ErrorAction Stop"
if %ERRORLEVEL% neq 0 (
    echo Pythonインストーラーのダウンロードに失敗しました。
    pause
    exit /b 1
)

:: Pythonをインストール
echo Pythonをインストール中...
start /wait "" "%installer_path%" /quiet InstallAllUsers=1 PrependPath=1

:: Pythonインストールを確認
echo Pythonインストールを確認中...
python --version
if %ERRORLEVEL% neq 0 (
    echo Pythonのインストールに失敗しました。
    echo インストールログを確認してください。
    pause
    exit /b 1
)

:: 必要なライブラリをインストール
echo 必要なライブラリをインストール中...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo 必要なライブラリのインストールに失敗しました。
    pause
    exit /b 1
)

:: クリーンアップ
del "%installer_path%"

echo インストールが正常に完了しました。
pause
