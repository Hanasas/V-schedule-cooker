# 这份代码整合所有功能，用于在中GUI调用

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import easyocr
import numpy as np

import timeJudge
import sorted_queue
import group

class Position:
    def __init__(self,l) -> None:
        if len(l) < 4:
            raise IndexError("init position from a short list")
        self.left_up = l[0]
        self.right_up = l[1]
        self.right_down = l[2]
        self.left_down  = l[3]

    def get_np_points(self):  
        # 返回四边形的四个角点，形成一个多段线的点集  
        return np.array([[self.left_up, self.right_up, self.right_down, self.left_down]], dtype=np.int32)
    
    def get_rect_two_points(self):
        x1 = min(self.left_down[0], self.left_up[0], self.right_down[0], self.right_up[0])
        x2 = max(self.left_down[0], self.left_up[0], self.right_down[0], self.right_up[0])
        y1 = min(self.left_down[1], self.left_up[1], self.right_down[1], self.right_up[1])
        y2 = max(self.left_down[1], self.left_up[1], self.right_down[1], self.right_up[1])
        return (x1,y1,x2,y2)
    
    def set_rect_two_points(self,x1,y1,x2,y2):
        self.left_up = (x1,y1)
        self.right_up = (x2,y1)
        self.right_down = (x2,y2)
        self.left_down = (x1,y2)
    
    def __str__(self):
        return f"({self.left_up}, {self.right_up}, {self.right_down}, {self.left_down})"
    
    def __lt__(self,other):
        a = self.left_up
        b = other.left_up
        if a[1] != b[1]:
            return a[1] < b[1]
        return a[0] < b[0]

"""
    表示一个具有位置、文本和类型的项目。
    类型根据文本内容确定，特别是是否表示时间。
"""
class Item:
    def __init__(self,position,text,confidence) -> None:
        self.position = Position(position)
        self.text = text
        # self.confidence = confidence
        self.type = timeJudge.is_time_string(text)
    
    def print_detail(self) -> None:
        print(self.position,end=',')
        print(self.text,end=',')
        # print(self.confidence,end=',')
        print(self.type)

    def get_rect_two_points(self) :
        return self.position.get_rect_two_points()
    
    def set_rect_two_points(self,x1,y1,x2,y2):
        self.position.set_rect_two_points(x1,y1,x2,y2)

# -----------------------------------------------------------------

time_queue = sorted_queue.SortedQueue()

"""
    处理图像以识别和提取文本信息。

    使用EasyOCR库读取图像并识别其中的文本，然后在识别出的文本周围绘制边界框，并在图像上标注文本类型。
    最后，将处理后的图像保存到指定路径。

    参数:
    image_name (str): 输入图像的文件名。

    返回:
    list[Item]: 包含识别结果的项列表。
"""
def handle_image(image_name) -> list[Item]:
    reader = easyocr.Reader(['en'], gpu=True, model_storage_directory='./EasyOCRModel')
    text_json_list = []
    precision_json_list = []
    img = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
    results = [Item(*item) for item in reader.readtext(img)]
    print("识别完成")
    # for result in results:
    #     result.printDetail()
    for item in results:
        cv2.polylines(img,item.position.get_np_points(),isClosed=True,color=(0,0,255),thickness=2)
        cv2.putText(img,str(item.type),item.position.left_down,cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    output_image_path = "result_" + image_name
    cv2.imwrite(output_image_path, img)
    print("绘制边界框并保存图片完成")
    return results

"""
    处理时间相关的项目，并更新全局时间队列。
    
    此函数遍历给定的项目列表，根据项目类型决定如何处理每个项目。它还会重置时间队列并根据需要更新它。
    
    参数:
    items (list[Item]): 待处理的项目列表。
    
    返回:
    list[Item]: 处理后的项目列表，主要包含类型为1的项目。
"""
def handle_time(items:list[Item]) -> list[Item]:
    global time_queue
    before_queue = items
    results = []
    if time_queue.is_empty == False:
        time_queue.clear()
    cnt = 0
    for index,item in enumerate(before_queue):
        cnt += 1
        if item.type == 1: # text
            results.append(item)
        elif item.type == 2 or item.type == 3: # date weekday
            pass
        else:
            time_queue.enqueue(item.position) # time zone
    return results

def get_time_rect():
    global time_queue
    
