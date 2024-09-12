import re
from collections import defaultdict

# 元のタイムスタンプ文字列リスト
timestamps = [
    "2024年09月11日_05時30分20秒",
    "2024年09月11日_07時45分30秒",
    "2024年09月12日_06時15分10秒",
    "2024年09月12日_08時00分45秒",
    "2024年09月13日_07時50分30秒",
    "2024年10月01日_07時00分00秒",
    "2024年10月01日_08時05分10秒",
    "2024年10月02日_09時15分30秒",
]

# 時刻と分の差を計算する関数
def get_time_difference(ts):
    match = re.search(r"(\d{2})時(\d{2})分", ts)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        return abs((hour - 8) * 60 + (minute - 0))
    return float('inf')  # マッチしない場合は非常に大きな値を返す

# 年月ごとに日付ごとに最も8時に近いタイムスタンプを格納する辞書
timestamps_by_month_day = defaultdict(lambda: defaultdict(lambda: None))
all_processed_timestamps = set()

for timestamp in timestamps:
    # 年月日部分を抽出
    date_match = re.match(r"(\d{4}年\d{2}月\d{2}日)", timestamp)
    if date_match:
        year_month_day = date_match.group(1)
        year_month = year_month_day[:7]  # 年月部分
        day = year_month_day[8:]  # 日付部分
        
        # 現在のタイムスタンプが、指定した年月日で最も8時に近いものかを確認
        if timestamps_by_month_day[year_month][day] is None or get_time_difference(timestamp) < get_time_difference(timestamps_by_month_day[year_month][day]):
            if timestamps_by_month_day[year_month][day] is not None:
                all_processed_timestamps.remove(timestamps_by_month_day[year_month][day])
            timestamps_by_month_day[year_month][day] = timestamp
            all_processed_timestamps.add(timestamp)

# 抽出されたタイムスタンプを出力
print("抽出されたタイムスタンプ:")
for year_month, days in timestamps_by_month_day.items():
    for day, ts in days.items():
        if ts:  # None でない場合のみ
            print(f"{year_month} {day}: {ts}")

# 抽出されなかったタイムスタンプを出力
print("\n抽出されなかったタイムスタンプ:")
for ts in timestamps:
    if ts not in all_processed_timestamps:
        print(ts)
