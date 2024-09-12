import backup

try:
    backup.execBackup('.config.ini')
    print("成功", "バックアップが完了しました。")
except Exception as e:
    print("エラー", f"エラーが発生しました: {str(e)}")

