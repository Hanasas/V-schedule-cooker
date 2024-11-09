import cv2
import numpy as np
from PIL import Image

def get_colors_threshold(image, pos):
    # 提取矩形区域
    x1, y1, x2, y2 = pos
    text_box = image.crop((x1, y1, x2, y2))
    
    # 将PIL图像转换为OpenCV图像
    text_box_cv = cv2.cvtColor(np.array(text_box), cv2.COLOR_RGB2BGR)

    # 转换为灰度图像
    gray = cv2.cvtColor(text_box_cv, cv2.COLOR_BGR2GRAY)
    
    # 应用Otsu's方法自动计算阈值并进行分割
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 统计像素数量
    background_pixel_count = np.sum(binary == 255)
    text_pixel_count = np.sum(binary == 0)
    
    # 计算背景颜色和文字颜色的中位数
    if background_pixel_count > text_pixel_count:
        background_color = np.median(text_box_cv[binary == 255], axis=0).astype(int)
        text_color = np.median(text_box_cv[binary == 0], axis=0).astype(int)
    else:
        background_color = np.median(text_box_cv[binary == 0], axis=0).astype(int)
        text_color = np.median(text_box_cv[binary == 255], axis=0).astype(int)
    
    # 将BGR颜色转换为RGB颜色
    background_color_rgb = background_color[::-1]
    text_color_rgb = text_color[::-1]
    
    return tuple(background_color_rgb), tuple(text_color_rgb)
