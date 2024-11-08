import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("选择图片")
        self.geometry("400x300")
        
        # 创建按钮，用于打开文件对话框选择图片
        self.select_button = tk.Button(self, text="选择图片", command=self.open_image)
        self.select_button.pack(pady=20)
        
        # 用于显示选中的图片
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=20)

    def open_image(self):
        # 打开文件对话框，让用户选择图片文件
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            # 使用PIL加载图片
            image = Image.open(file_path)
            # 调整图片大小以适应标签
            image = image.resize((200, 200))
            # 将PIL图像转换为Tkinter兼容的图像
            photo = ImageTk.PhotoImage(image)
            # 更新标签以显示图片
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 防止垃圾回收

if __name__ == "__main__":
    app = GUI()
    app.mainloop()