import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
import matplotlib.font_manager as fm

# 从原图的image对象中取出文本框
def get_text_box(image, pos):
    # 从原图的image对象中取出文本框
    #
    # 参数:
    # image (PIL.Image): 原图像对象
    # pos (tuple): 文本框的位置 (left, upper, right, lower)
    #
    # 返回:
    # PIL.Image: 文本框图像对象
    x1, y1, x2, y2 = pos
    text_box = image.crop((x1, y1, x2, y2))
    return text_box

# 使用K-means聚类获得背景颜色和文字颜色
def get_colors_kmeans(text_box, n_clusters=2):
    # 使用K-means聚类获得背景颜色和文字颜色
    #
    # 参数:
    # text_box (PIL.Image): 文本框图像对象
    # n_clusters (int): 聚类的簇数，默认为2
    #
    # 返回:
    # tuple: 背景颜色 (R, G, B)
    # tuple: 文字颜色 (R, G, B)
    pixels = np.array(text_box).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_clusters).fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    
    # 获取数量最多的簇和数量最少的簇
    cluster_A = colors[np.argmax(counts)]
    cluster_B = colors[np.argmin(counts)]
    
    # 获取簇A和簇B中的所有像素
    pixels_A = pixels[labels == np.argmax(counts)]
    pixels_B = pixels[labels == np.argmin(counts)]
    
    # 选择簇A中最浅的颜色作为背景颜色
    background_color = pixels_A[np.sum(pixels_A, axis=1).argmin()]
    
    # 选择簇B中最深的颜色作为文字颜色
    text_color = pixels_B[np.sum(pixels_B, axis=1).argmax()]
    
    return tuple(background_color), tuple(text_color)

# 动态计算合适的字号
def calculate_font_size(text, text_box_height, font_path):
    # 动态计算合适的字号
    #
    # 参数:
    # text (str): 要绘制的文本
    # text_box_height (int): 文本框的高度
    # font_path (str): 字体文件的路径
    #
    # 返回:
    # int: 计算出的合适字号
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while draw.textbbox((0, 0), text, font=font)[3] < text_box_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
    return font_size

# 在文本框内写上新的字
def draw_text_in_box(image, pos, text, background_color, text_color, font_path):
    # 在文本框内写上新的字
    #
    # 参数:
    # image (PIL.Image): 原图像对象
    # pos (tuple): 文本框的位置 (left, upper, right, lower)
    # text (str): 要绘制的文本
    # background_color (tuple): 背景颜色 (R, G, B)
    # text_color (tuple): 文字颜色 (R, G, B)
    # font_path (str): 字体文件的路径
    text_box = get_text_box(image, pos)
    text_box_height = text_box.size[1]
    font_size = calculate_font_size(text, text_box_height, font_path)
    font = ImageFont.truetype(font_path, font_size)
    
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = pos
    
    # 用背景颜色填充文本框
    draw.rectangle([x1, y1, x2, y2], fill=background_color)
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = x1
    text_y = y1 + (y2 - y1 - text_height) // 2
    
    # 用字体颜色写字
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    # 返回新字的位置范围
    new_pos = (text_x, text_y, text_x + text_width, text_y + text_height)
    return new_pos

# 从config.txt中获得字体，并且从系统中读取字体
def get_font_from_config(config_path="config.txt", default_font_path="arial.ttf"):
    # 从config.txt中获得字体，并且从系统中读取字体
    #
    # 参数:
    # config_path (str): 配置文件的路径，默认为"config.txt"
    # default_font_path (str): 默认字体文件的路径，默认为"arial.ttf"
    #
    # 返回:
    # str: 字体文件的路径
    font_name = None
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            for line in config_file:
                if line.startswith("Font:"):
                    font_name = line.split(":")[1].strip()
                    break
    if font_name:
        # 在系统中查找字体文件
        font_path = find_font_path(font_name)
        if font_path:
            return font_path
    return default_font_path

def find_font_path(font_name):
    # 在系统中查找字体文件
    #
    # 参数:
    # font_name (str): 字体名称
    #
    # 返回:
    # str: 字体文件的路径，如果未找到则返回None
    print(f"Searching for font: {font_name}")

    # 获取系统中的所有字体
    font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    for font_path in font_list:
        try:
            font = fm.FontProperties(fname=font_path)
            if font_name.lower() in font.get_name().lower():
                print(f"Found font: {font_path}")
                return font_path
        except Exception as e:
            print(f"Error reading {font_path}: {e}")
    return None

def cover_text(image, pos, text, font_path="arial.ttf"):
    # 从原图中提取文本框
    text_box = get_text_box(image, pos)

    # 使用K-means聚类获得背景颜色和文字颜色
    background_color, text_color = get_colors_kmeans(text_box)
    print(f"Background color: {background_color}")
    print(f"Text color: {text_color}")

    # 从config.txt中获得字体，并且从系统中读取字体
    font_path = get_font_from_config()

    # 在文本框内写上新的字，并返回新字的位置范围
    new_pos = draw_text_in_box(image, pos, text, background_color, text_color, font_path)

    return image, new_pos
    

# 示例使用
if __name__ == "__main__":
    # 打开一个图像文件
    image = Image.open("02.png")

    # 定义文本框的位置 (left, upper, right, lower)
    pos = (283, 110, 424, 138)

    # 从原图中提取文本框
    text_box = get_text_box(image, pos)
    text_box.show()

    # 使用K-means聚类获得背景颜色和文字颜色
    background_color, text_color = get_colors_kmeans(text_box)
    print(f"Background color: {background_color}")
    print(f"Text color: {text_color}")

    # 从config.txt中获得字体，并且从系统中读取字体
    font_path = get_font_from_config()

    # 在文本框内写上新的字
    draw_text_in_box(image, pos, "新文字", background_color, text_color, font_path)

    # 显示新图像   
    image.show()