import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from font_timezone_selector import FontTimezoneSelector
from cookerUI import cooker

ori_image_path = None

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # 配置文件不存在，则创建一个 
        if not FontTimezoneSelector.if_config_exist():
            FontTimezoneSelector(self,self.init_ui())
        else :
            self.init_ui()

    def init_ui(self):
        # 界面的内容是选择图片
        self.title("select image")
        self.geometry("1080x720")
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        # 创建按钮，用于打开文件对话框选择图片
        self.select_button = tk.Button(self.button_frame, text="选择图片", command=self.open_image)
        self.select_button.pack(side='left',padx=10,pady=20)

        # 创建按钮，用于清空界面
        self.clear_button = tk.Button(self.button_frame, text="确定", command=self.go_next)
        self.clear_button.pack(side='left',padx=10,pady=20)

        # 用于显示选中的图片
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=20)

        

    def open_image(self):
        global ori_image_path
        # 打开文件对话框，让用户选择图片文件
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            ori_image_path = file_path
            # 使用PIL加载图片
            image = Image.open(file_path)

            # 调整预览图大小
            max_width, max_height = 960, 640  # 设置最大宽度和高度
            image.thumbnail((max_width, max_height))

            # 将PIL图像转换为Tkinter兼容的图像
            photo = ImageTk.PhotoImage(image)
            # 清空当前显示的图片
            self.image_label.config(image='')
            # 更新标签以显示图片
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 防止垃圾回收

    def clear_ui(self):
        # 清空界面上的所有组件
        for widget in self.winfo_children():
            widget.pack_forget()

    def go_next(self):
        if ori_image_path is None:
            return
        # 清空界面
        self.clear_ui()
        # 进入下一个界面
        self.title("V schedule cooker")

        self.cooker_frame = cooker(self, ori_image_path)
        self.cooker_frame.pack(fill=tk.BOTH, expand=True)

        

if __name__ == "__main__":
    app = GUI()
    app.mainloop()