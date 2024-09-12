import glob
import re
import os
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo
import pyzipper
import configparser
from collections import defaultdict

g_Saisin = "最新"
g_Kako = "過去"
g_Hozon = "保存"
g_KugiriMoji = "/"
g_allowSizeDifferece = 100000
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
    
    print(message)

# 時刻と分の差を計算する関数
def get_time_difference(ts):
    if ts is None:
        return float('inf')
    match = re.search(r"(\d{2})時(\d{2})分", ts)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        return abs((hour - 8) * 60 + (minute - 0))
    return float('inf')  # マッチしない場合は非常に大きな値を返す

def get_folder_size(folder_path):
    total_size = 0
    # フォルダ内を再帰的に探索し、ファイルのサイズを取得
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # ファイルサイズを確認
            file_size = os.path.getsize(file_path)
            print(f"File: {file_path}, Size: {file_size} bytes")
            total_size += file_size
    return total_size

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

    threeMonthAgoFiles = []
    # ファイル名のリスト
    i = 0
    while i < len(fileNames):
        file = fileNames[i]
        # ファイル名から年月日時分秒の切り出し
        p = re.findall(r'\d+', file)
        if len(p) >= 6:
            # ３ヶ月以上前のファイルリストの辞書を作成
            if int(p[0]) <= threeMonthAgoYear and int(p[1]) < threeMonthAgoMonth:
                threeMonthAgoFiles.append(file)
        i += 1

    timestamps_by_month_day = defaultdict(lambda: defaultdict(lambda: None))
    all_processed_timestamps = set()

    originalFileSize = get_folder_size(g_original)
    write_log(g_original + " : " + str(originalFileSize) + " bytes")
    for file in threeMonthAgoFiles:
        # 年月日部分を抽出
        date_match = re.match(r"(\d{4}年\d{2}月\d{2}日)", file)
        if date_match:
            year_month_day = date_match.group(1)
            year_month = year_month_day[:8]  # 年月部分
            day = year_month_day[8:10]  # 日付部分
            # 現在のタイムスタンプが、指定した年月日で最も8時に近いものかを確認
            if timestamps_by_month_day[year_month][day] is None or get_time_difference(file) < get_time_difference(timestamps_by_month_day[year_month][day]):
                if timestamps_by_month_day[year_month][day] is not None:
                    all_processed_timestamps.remove(timestamps_by_month_day[year_month][day])
                write_log(file)
                fileSize = get_folder_size(file)
                write_log(str(fileSize))
                if (not (originalFileSize - fileSize > g_allowSizeDifferece)):
                    timestamps_by_month_day[year_month][day] = file
                    all_processed_timestamps.add(file)

    # 年月ごとに最も8時に近いタイムスタンプをリストにまとめる
    toZipFilesDict = defaultdict(list)

    for year_month, days in timestamps_by_month_day.items():
        for day, ts in days.items():
                toZipFilesDict[year_month].append(ts)

    toDeleteFileList = []
    for ts in threeMonthAgoFiles:
        if ts not in all_processed_timestamps:
            toDeleteFileList.append(ts)
    
    empty_values = [None, '', [], {}]
    for key, value in toZipFilesDict.items():
        if value in empty_values:
            write_log(key + "は空です。")
            continue
        newPath = f'{g_path}{g_KugiriMoji}{g_Hozon}{g_KugiriMoji}{key}'
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        for file in value:
            if os.path.exists(f'{g_path}{g_KugiriMoji}{g_Kako}{g_KugiriMoji}{file}'):
                shutil.move(f'{g_path}{g_KugiriMoji}{g_Kako}{g_KugiriMoji}{file}', f'{newPath}{g_KugiriMoji}{file}')
        with pyzipper.AESZipFile(f'{newPath}.zip', 'w', compression=pyzipper.ZIP_DEFLATED) as zf:
            zf.setpassword(g_password.encode('utf-8'))
            zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES256で暗号化         
            for foldername, subfolders, filenames in os.walk(newPath):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, newPath)
                    # ファイルをZIPファイルに追加
                    zf.write(file_path, arcname)
                    write_log("ZipTo : " + file_path)
        shutil.rmtree(newPath)
        write_log(f'{newPath}.zip を作成しました。')

    for folder in toDeleteFileList:
        shutil.rmtree(f'{g_path}{g_KugiriMoji}{g_Kako}{g_KugiriMoji}{folder}')
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
