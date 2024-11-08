import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import matplotlib.font_manager as fm
import os

config_file = 'config.txt'

class FontTimezoneSelector(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.callback = callback
        self.title("选择字体和时区")
        self.geometry("400x300")

        
        # 获取系统中的所有字体
        font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        # 获取系统中的所有字体
        self.fonts = sorted([fm.FontProperties(fname=font).get_name() for font in font_list])

        # 字体选框
        self.font_label = tk.Label(self, text="选择字体:")
        self.font_label.pack(pady=10)
        self.font_var = tk.StringVar()
        self.font_combobox = ttk.Combobox(self, textvariable=self.font_var)
        self.font_combobox['values'] = self.fonts
        self.font_combobox.pack(pady=10)

        # 常见时区及其对应的 UTC 时间
        self.timezones = {
            "CST": "UTC+08:00",
            "EST": "UTC-05:00",
            "PST": "UTC-08:00",
            "MST": "UTC-07:00",
            "JST": "UTC+09:00",
            "GMT": "UTC+00:00",
            "CET": "UTC+01:00",
            "EET": "UTC+02:00",
            "IST": "UTC+05:30",
            "AEST": "UTC+10:00"
        }

        # 时区选框
        self.timezone_label = tk.Label(self, text="选择时区:")
        self.timezone_label.pack(pady=10)
        self.timezone_var = tk.StringVar()
        self.timezone_combobox = ttk.Combobox(self, textvariable=self.timezone_var)
        self.timezone_combobox['values'] = [f"{tz} ({offset})" for tz, offset in self.timezones.items()]
        self.timezone_combobox.pack(pady=10)

        # 添加确认按钮
        self.confirm_button = tk.Button(self, text="确认", command=self.save_and_close)
        self.confirm_button.pack(pady=20)

        # 设置模式窗口
        self.grab_set()
        self.transient(master)
        self.wait_window(self)

    def save_and_close(self):
        font = self.font_var.get()
        timezone = self.timezone_var.get()
        with open("config.txt", "w") as config_file:
            config_file.write(f"Font: {font}\n")
            config_file.write(f"Timezone: {timezone}\n")
        self.destroy()
        if self.callback:
            self.callback()

    def if_config_exist():
        """判断配置文件是否存在"""
        return os.path.exists(config_file)