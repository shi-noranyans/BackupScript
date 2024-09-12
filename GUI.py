import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import backup

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("バックアップ")

        self.config_file = '.config.ini'
        self.config = configparser.ConfigParser()
        self.load_config()

        # GUIの作成
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        # フォルダ選択
        l1 = ttk.Label(frame, text="[システムバックアップ]フォルダを選択してください")
        l1.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.path_entry = tk.Entry(frame, width=50)
        self.path_entry.insert(0, self.path)
        self.path_entry.grid(row=1, column=0, padx=5, pady=5)

        b1 = ttk.Button(frame, text="選択", command=self.select_folder)
        b1.grid(row=1, column=1, padx=5)

        s1 = ttk.Separator(frame, orient="horizontal")
        s1.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # パスワードファイル選択
        l2 = ttk.Label(frame, text="[パスワードファイル]を選択してください")
        l2.grid(row=3, column=0, columnspan=2, pady=5)

        self.pass_entry = tk.Entry(frame, width=50)
        self.pass_entry.insert(0, self.password)
        self.pass_entry.grid(row=4, column=0, padx=5, pady=5)

        b2 = ttk.Button(frame, text="選択", command=self.select_file)
        b2.grid(row=4, column=1, padx=5)

        s2 = ttk.Separator(frame, orient="horizontal")
        s2.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # オリジナルファイル選択
        l3 = ttk.Label(frame, text="[オリジナルファイル]を選択してください")
        l3.grid(row=6, column=0, columnspan=2, pady=5)

        self.org_entry = tk.Entry(frame, width=50)
        self.org_entry.insert(0, self.original)
        self.org_entry.grid(row=7, column=0, padx=5, pady=5)

        b3 = ttk.Button(frame, text="選択", command=self.select_file_original)
        b3.grid(row=7, column=1, padx=5)

        s3 = ttk.Separator(frame, orient="horizontal")
        s3.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        # バックアップ開始ボタン
        b4 = ttk.Button(frame, text="バックアップ開始", command=self.start_backup)
        b4.grid(row=9, column=0, columnspan=2, pady=20)


    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def select_file(self):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.insert(0, file_selected)

    def select_file_original(self):
        file_selected = filedialog.askdirectory()
        if file_selected:
            self.org_entry.delete(0, tk.END)
            self.org_entry.insert(0, file_selected)

    def start_backup(self):
        # 設定の保存
        self.password = self.pass_entry.get()
        self.original = self.org_entry.get()
        self.path = self.path_entry.get()

        self.config['Credentials'] = {
            'password': self.password,
            'original': self.original,
            'path': self.path
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

        try:
            # バックアップの実行
            backup.execBackup(self.config_file)
            messagebox.showinfo("成功", "バックアップが完了しました。")
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self.password = self.config.get('Credentials', 'password', fallback='')
            self.original = self.config.get('Credentials', 'original', fallback='')
            self.path = self.config.get('Credentials', 'path', fallback='')
        else:
            self.password = ''
            self.original = ''
            self.path = ''

def main():
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
