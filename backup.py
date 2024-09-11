import glob
import re
import os
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo
import pyzipper
import configparser

g_Saisin = "最新"
g_Kako = "過去"
g_Hozon = "保存"
g_SystemBackup = "システムバックアップ"
g_KugiriMoji = "/"
g_password = ''
g_original = ''
g_path = ''

# ログファイルへの書き出し用関数
def write_log(message):
    # 現在の年月日を取得
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    # ログファイルのパスを指定
    log_file_dir = 'Logs'
    log_file_name = f'{date_str}.log'
    log_file_path = os.path.join(log_file_dir, log_file_name)
    
    # ログディレクトリが存在しない場合は作成
    if not os.path.exists(log_file_dir):
        os.makedirs(log_file_dir)
    
    # 現在の年月日とメッセージをフォーマット
    log_message = f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"
    
    # ログファイルに書き込む
    with open(log_file_path, 'a') as file:
        file.write(log_message)

def execBackup(config_path):
    write_log("Backup開始")
    load_config(config_path)
    searchFolderPath = g_path + g_KugiriMoji + g_Kako
    # フォルダ内のファイルのリストを取得
    files = glob.glob(searchFolderPath + g_KugiriMoji + "*")
    fileNames = []
    if len(files) <= 0:
        raise ValueError("パスが正しくありません。")
        
    # ファイル名（パス）のリスト
    for file in files:
        fileName = file.split(g_KugiriMoji)[-1]
        # ファイルのリストからファイル名のリストを作成
        fileNames.append(fileName)

    # ３ヶ月前の年月を取得
    today = datetime.now(ZoneInfo("Asia/Tokyo")).date()    
    threeMonthAgoYear = today.year
    threeMonthAgoMonth = today.month - 3
    if threeMonthAgoMonth <= 0:
        threeMonthAgoMonth += 12
        threeMonthAgoYear -= 1

    toZipFileObj = {}
    toDeleteFileObj = []
    # ファイル名のリスト
    i = 0
    while i < len(fileNames):
        file = fileNames[i]
        # ファイル名から年月日時分秒の切り出し
        p = re.findall(r'\d+', file)

        if len(p) >= 6:
            # ３ヶ月以上前のファイルリストの辞書を作成
            if int(p[0]) <= threeMonthAgoYear and int(p[1]) < threeMonthAgoMonth:
                key = f'{p[0]:04}年{p[1]:02}月'
                exist8file = False
                if (p[3] == '08'):
                    exist8file = True
                    if key in toZipFileObj:
                        toZipFileObj[key].append(file)
                    else:
                        toZipFileObj[key] = [file]
                if exist8file == False:
                    for i in range(7, 4, -1):
                        for dfile in fileNames:
                            if (int(p[3]) == i):
                                exist8file = True
                                if key in toZipFileObj:
                                    toZipFileObj[key].append(dfile)
                                else:
                                    toZipFileObj[key] = [dfile]
                                break
                if exist8file == False:
                    for i in range(9, 24, +1):
                        for dfile in fileNames:
                            if (int(p[3]) == i):
                                exist8file = True
                                if key in toZipFileObj:
                                    toZipFileObj[key].append(dfile)
                                else:
                                    toZipFileObj[key] = [dfile]
                                break
                for dfile in fileNames:
                    if re.match(f'{p[0]:04}年{p[1]:02}月{p[2]:02}日_*', dfile) != None:
                        toDeleteFileObj.append(dfile)
                        fileNames.remove(dfile)
        i += 1

    for key, value in toZipFileObj.items():
        newPath = f'{g_path}{g_KugiriMoji}{g_Hozon}{g_KugiriMoji}{key}'
        print(newPath)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        for file in value:
            shutil.move(f'{g_path}{g_KugiriMoji}{g_Kako}{g_KugiriMoji}{file}', f'{newPath}{g_KugiriMoji}{file}')
        with pyzipper.AESZipFile(f'{newPath}.zip', 'w', compression=pyzipper.ZIP_LZMA) as zf:
            zf.setpassword(g_password)
            zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES256で暗号化         
            zf.write(newPath)
        write_log(f'{newPath}.zip を作成しました。')

    for folder in toDeleteFileObj:
        shutil.rmtree(folder)
        write_log(f'{folder} を削除しました。')

def load_config(config_path):
    global g_password
    global g_original
    global g_path
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        with open(config.get('Credentials', 'password', fallback=''), 'r') as f:
            g_password = f.read()
        g_original = config.get('Credentials', 'original', fallback='')
        g_path = config.get('Credentials', 'path', fallback='')
    else:
        g_password = ''
        g_original = ''
        g_path = ''

#execBackup('.config.ini')
