# 这个代码实现了对包含时间的矩形按距离聚类分组，并输出若干个矩形，每个矩形覆盖一个组
# 调用cover_rects(rectangles)
# 每一组的矩形中心最大的距离
MAX_D = 200

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import euclidean

# 矩形列表，每个矩形由四个点表示
rectangles = [
    ([671, 103], [745, 103], [745, 119], [671, 119]),([769, 103], [803, 103], [803, 121], [769, 121]),([669, 123], [741, 123], [741, 141], [669, 141]),([769, 125], [801, 125], [801, 141], [769, 141]),([671, 147], [743, 147], [743, 163], [671, 163]),([769, 147], [801, 147], [801, 165], [769, 165]),([671, 239], [747, 239], [747, 255], [671, 255]),([769, 239], [803, 239], [803, 257], [769, 257]),([671, 261], [745, 261], [745, 277], [671, 277]),([769, 261], [801, 261], [801, 277], [769, 277]),([671, 283], [747, 283], [747, 299], [671, 299]),([769, 283], [801, 283], [801, 299], [769, 299]),([671, 511], [745, 511], [745, 527], [671, 527]),([769, 511], [803, 511], [803, 529], [769, 529]),([671, 533], [741, 533], [741, 549], [671, 549]),([769, 533], [801, 533], [801, 549], [769, 549]),([671, 555], [743, 555], [743, 571], [671, 571]),([769, 555], [801, 555], [801, 571], [769, 571]),([671, 647], [745, 647], [745, 663], [671, 663]),([769, 647], [803, 647], [803, 665], [769, 665]),([671, 669], [745, 669], [745, 685], [671, 685]),([769, 669], [801, 669], [801, 685], [769, 685]),([669, 689], [741, 689], [741, 707], [669, 707]),([769, 691], [801, 691], [801, 707], [769, 707]),([671, 783], [745, 783], [745, 801], [671, 801]),([769, 783], [803, 783], [803, 801], [769, 801]),([671, 805], [745, 805], [745, 821], [671, 821]),([769, 805], [801, 805], [801, 821], [769, 821]),([671, 825], [745, 825], [745, 843], [671, 843]),([769, 827], [801, 827], [801, 843], [769, 843]),
]

def rect_form(rectangle_points):
    x1, y1 = min(point[0] for point in rectangle_points), min(point[1] for point in rectangle_points)
    x2, y2 = max(point[0] for point in rectangle_points), max(point[1] for point in rectangle_points)
    
    rect = [x1,y1,x2,y2]
    return rect

# 计算矩形中心点的函数
def rectangle_center(rect):
    x1, y1, x2, y2 = rect_form(rect)
    return [(x1 + x2) / 2, (y1 + y2) / 2]

# 计算每个类的覆盖矩形的列表
def cover_rects(rectangles):
    # 计算所有矩形中心点的列表
    centers = [rectangle_center(rect) for rect in rectangles]

    # 将中心点转换为numpy数组，便于计算
    centers_array = np.array(centers)

    # 计算中心点之间的距离矩阵
    distance_matrix = np.zeros((len(centers), len(centers)))
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            distance_matrix[i, j] = euclidean(centers[i], centers[j])
            distance_matrix[j, i] = distance_matrix[i, j]

    # 使用层次聚类进行聚类
    Z = linkage(distance_matrix, method='single')

    # 根据最大距离阈值进行聚类划分，这里选择一个合适的阈值
    max_d = MAX_D  # 例如，距离阈值为200
    clusters = fcluster(Z, max_d, criterion='distance')

    # 打印聚类结果
    for i, cluster in enumerate(clusters):
        print(f"Rectangle {i + 1} is in cluster {cluster}")

    # 可以将聚类结果与原矩形列表关联起来
    clustered_rectangles = {cluster: [rectangles[i] for i, c in enumerate(clusters) if c == cluster] for cluster in set(clusters)}
    # print(clustered_rectangles)

    group_rects = []
    for i in clustered_rectangles:
        items = clustered_rectangles[i]
        x1 = float('inf')
        y1 = float('inf')
        x2 = 0
        y2 = 0
        for item in items:
            for x,y in item:
                x1 = min(x1,x)
                y1 = min(y1,y)
                x2 = max(x2,x)
                y2 = max(y2,y)
        group_rects.append([x1,y1,x2,y2])

    group_rects_formed = []
    for item in group_rects:
        x1,y1,x2,y2 = item
        rec_formed = ([x1,y1],[x2,y1],[x2,y2],[x1,y2])
        group_rects_formed.append(rec_formed)
    print(group_rects_formed)
    return group_rects_formed