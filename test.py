from zoneinfo import available_timezones

# 利用可能なタイムゾーンのリストを表示
timezones = available_timezones()
print(timezones)

# Asia/Tokyoの確認
if 'Asia/Tokyo' in timezones:
    print("Asia/Tokyo タイムゾーンは利用可能です。")
else:
    print("Asia/Tokyo タイムゾーンは利用できません。")
