import tkinter as tk
from PIL import Image, ImageTk
import cv2
import easyocr
import numpy as np
from tkinter import filedialog, messagebox

import workout as wk
import cover_text as ct
import time_convert as tc

class cooker(tk.Frame):
    def __init__(self, master = None, path = None):
        super().__init__()
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.max_width = master.winfo_width() - 100
        self.max_height = master.winfo_height() - 100

        self.font = ct.get_font_from_config()

        ori_rects = wk.handle_image(path)
        self.rects = wk.handle_time(ori_rects)
        time_group = wk.get_time_rect()
        cluster_times = wk.get_cluster_times(wk.time_queue.get_list(), time_group)
        
        # for cluster_id, time in cluster_times.items():
        #     print(f"Cluster {cluster_id} time: {time}")

        self.image = cv2.imread(path)

        # 遍历 time_group 并为时间矩形添加覆盖颜色
        for i,rect in time_group:
            x1, y1, x2, y2 = map(int, rect)
            time_box = self.image[y1:y2, x1:x2]
            cover_color = wk.get_cover_color(time_box)
            cv2.rectangle(self.image, (x1 - 8, y1 - 8), (x2 + 8, y2 + 8), cover_color, thickness=cv2.FILLED)
        
        # 为每个时间矩形写上转化时区后的时间
        for cluster_id, time in cluster_times.items():
            rect = cluster_id
            target_timezone = tc.read_target_timezone('config.txt')
            time_str = time
            converted_time = tc.convert_to_target_timezone(time_str, target_timezone)
            
            x1, y1, x2, y2 = map(int, rect)
            # 计算时间的尺寸
            text_size = cv2.getTextSize(converted_time + ' ' + target_timezone, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            # 计算文本的起始位置，使其在矩形区域的正中间
            text_x = int(x1 + (x2 - x1 - text_size[0]) // 2)
            text_y = int(y1 + (y2 - y1 + text_size[1]) // 2)
            # 在图像上绘制文本
            cv2.putText(self.image, converted_time + ' ' + target_timezone, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=2)



        self.image_index = 0

        # 图片显示区域
        self.image_label = tk.Label(self)
        self.image_label.pack()

        # 图片序号标签
        self.image_index_label = tk.Label(self, text=f"序号: {self.image_index + 1}")
        self.image_index_label.pack()

        # 文本框
        self.text_box = tk.Text(self, height=5, width=50)
        self.text_box.pack()

        # 按钮容器
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)

        # 按钮
        self.prev_button = tk.Button(self.button_frame, text="上一个", command=self.show_prev_image)
        self.prev_button.pack(side="left", padx=10)
        self.ok_button = tk.Button(self.button_frame, text="确定", command=self.confirm)
        self.ok_button.pack(side="left", padx=10)
        self.next_button = tk.Button(self.button_frame, text="下一个", command=self.show_next_image)
        self.next_button.pack(side="left", padx=10)
        self.save_button = tk.Button(self.button_frame, text="保存并退出", command=self.save_and_exit)
        self.save_button.pack(side="left", padx=10)

        self.update_image()

    def update_image(self):
        # 复制原始图像
        now_image = self.image.copy()

        # 绘制当前索引对应的矩形框
        rect = self.rects[self.image_index]
        x1, y1, x2, y2 = rect.get_rect_two_points()
        cv2.rectangle(now_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # 将图像转换为PIL图像
        image = Image.fromarray(cv2.cvtColor(now_image, cv2.COLOR_BGR2RGB))

        # 限制图片大小
        resized_image = image.resize(self.calculate_resized_dimensions(image.size))
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # 防止图像被垃圾回收

        self.image_index_label.config(text=f"序号: {self.image_index + 1}")
        self.text_box.delete("1.0", tk.END)
    
    def calculate_resized_dimensions(self, original_size):
        width, height = original_size
        max_width = min(width, self.max_width)
        max_height = min(height, self.max_height)
        # 计算调整后的宽度和高度
        if width > max_width or height > max_height:
            if max_width / width < max_height / height:
                resized_width = max_width
                resized_height = int(height * (max_width / width))
            else:
                resized_height = max_height
                resized_width = int(width * (max_height / height))
            return (resized_width, resized_height)
        else:
            return (width, height)
    
    def show_prev_image(self):
        self.image_index = (self.image_index - 1) % len(self.rects)
        self.update_image()

    def show_next_image(self):
        self.image_index = (self.image_index + 1) % len(self.rects)
        self.update_image()

    def confirm(self):
        # 在这里编写点击确定按钮后的逻辑
        print(f'{self.text_box.get("1.0", tk.END)}')
        translated_text = self.text_box.get("1.0", tk.END).strip()
        image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        image, new_pos = ct.cover_text(image,self.rects[self.image_index].get_rect_two_points() ,translated_text, self.font)
        self.image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        x1, y1, x2, y2 = new_pos
        self.rects[self.image_index].set_rect_two_points(x1, y1, x2, y2)
        
        self.update_image()
        pass
    
    def save_and_exit(self):
        # 弹出保存对话框
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            # 保存图像
            pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            pil_image.save(file_path)
            messagebox.showinfo("保存成功", "图像已成功保存！")
            self.master.quit()
    

    

if __name__ == "__main__":
    app = cooker()
    app.mainloop()
