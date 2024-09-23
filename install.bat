@echo off
set "installer_path=C:\temp\python-installer.exe"
set "log_file=C:\temp\python_install.log"

:: Python�̃C���X�g�[��
if not exist "%installer_path%" (
    echo Python���C���X�g�[������Ă��܂���B�C���X�g�[�����J�n���܂��B
    set "download_url=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    powershell -Command "Invoke-WebRequest -Uri '%download_url%' -OutFile '%installer_path%'"
    echo �_�E�����[�h����: %installer_path%
)

echo Python�̃C���X�g�[�����J�n���܂�...
cmd /c "%installer_path%" /quiet InstallAllUsers=1 PrependPath=1 >> "%log_file%" 2>&1
set "install_error=%ERRORLEVEL%"
if %install_error% neq 0 (
    echo Python���������C���X�g�[������܂���ł����B�G���[�R�[�h: %install_error%
    exit /b
)

echo Python���������C���X�g�[������܂����B

:: ���C�u�������X�g�̃t�@�C������C���X�g�[��
echo ���C�u�����̃C���X�g�[�����J�n���܂�...
pip install -r requirements.txt
echo ���C�u�����̃C���X�g�[�����������܂����B

pause
