"""
@Author: zhang_zhiyi
@Date: 2024/11/22_14:05
@FileName:divide.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 断面分割
"""
import numpy as np
from pandas import DataFrame
import open3d as o3d

from utils.mesh import highlight_all_triangles
from utils.preprocess import preprocess, filter_distance
from utils.show import read_batch_csv, read_csv
from utils.surface import surface_by_hull


def divide(data: DataFrame, size: float):
    """
    根据x轴分割数据
    :param data:
    :param size: 断面大小
    :return:
    """
    try:
        # 从小到大排序 TODO: 是否为提高后续操作的执行效率有待验证
        sorted_x = data.sort_values(by='X', ascending=True).reset_index(drop=True)
        # 计算分割点
        min_x = sorted_x['X'].min()
        max_x = sorted_x['X'].max()
        # 根据size计算范围
        split_ranges = np.arange(min_x, max_x, size)
        # 分割数据
        segments = []
        for i in range(len(split_ranges) - 1):
            start = split_ranges[i]
            end = split_ranges[i + 1]
            segment = sorted_x[((sorted_x.loc[:, 'X'] >= start) & (sorted_x.loc[:, 'X'] <= end))]
            if not segment.empty:
                segments.append(segment)
        return segments
    except Exception as e:
        print(f"divide error: {str(e)}")
        return None


def calculate_focus():
    """
    计算两个线段的焦点
    :return:
    """
    pass


def split_triangle_by_x(triangle, end, start, index):
    """
    TODO: 分割一个三角形，使得其 X 坐标位于 x_min 到 x_min + step_size 区间内
    :param triangle:
    :param end:
    :param start:
    :param index: 新的顶点索引
    :return:
    """
    # 获取三角形的三个顶点
    v0, v1, v2 = triangle
    vertices = np.array([v0, v1, v2])
    # 获取每个顶点的 x 坐标
    x_coords = vertices[:, 0]

    # 如果三角形的所有顶点的 X 坐标都在[end, start]区间内，则不做处理
    if np.all((x_coords >= start) & (x_coords <= end)):
        return vertices, np.asarray([index, index+1, index+2])

    # 如果三角形的所有顶点的 X 坐标都在[end, start]区间之外，则不做处理
    if np.all((x_coords <= start)):
        return None
    if np.all((x_coords >= end)):
        return None

    # 如果三个顶点不在区间内，且在区间两侧都有分布，需分别计算与 x = start 和 x = end 的焦点
    if np.all((x_coords <= start) | (x_coords >= end)):
        return vertices, np.asarray([index, index + 1, index + 2])

    # 有顶点在区间内，但三个点不全在区间内
    # 求出三个顶点形成的三条线段的方程
    # 计算三条线段与 x = end / x = start 的焦点
    # 求出新的三角形集合

    # 有两个焦点
    # 有四个焦点

    return vertices, np.asarray([index, index+1, index+2])


def divide_mesh(data: o3d.geometry.TriangleMesh, size: float):
    """
    根据x轴分割mesh数据
    1. 提取数据
    2. 获取分割节点
    3. 分割mesh
        3.1 判断分割出的三角形是否在一个断面区间内
        3.2 若不在则对三角形怎么分割，直至三角形都在独立的区间内
        3.3 创建断面mesh
    :param data:
    :param size: 断面大小
    :return:
    """
    # 获取顶点的 X 坐标和所有的三角形索引
    vertices = np.asarray(data.vertices)
    triangles = np.asarray(data.triangles)

    # 获取 X 坐标的最大值和最小值
    min_x = np.min(vertices[:, 0])
    max_x = np.max(vertices[:, 0])
    # 获取分割节点
    x_ranges = np.arange(min_x, max_x, size)

    segments = []
    for i in range(len(x_ranges) - 1):
        start = x_ranges[i]
        end = x_ranges[i + 1]
        index_count = 0

        # 获取落在当前区间内的三角形索引、获取三角形对应的顶点坐标
        selected_triangles = []
        selected_vertices = []
        for t in triangles:
            # 获取三角形的三个顶点坐标
            triangle = vertices[t]
            # 判断是否要分割三角形（即某些顶点落在 X 区间的两侧）
            res = split_triangle_by_x(triangle, end, start, index_count)
            if res:
                new_v, new_t = res
                selected_triangles.append(new_t)
                selected_vertices.extend(new_v)
                index_count += 3

        # temp = np.asarray(selected_vertices)
        # temp1 = np.asarray(selected_triangles)
        # 创建子网格
        sub_mesh = o3d.geometry.TriangleMesh()
        sub_mesh.vertices = o3d.utility.Vector3dVector(selected_vertices)
        sub_mesh.triangles = o3d.utility.Vector3iVector(selected_triangles)

        if sub_mesh:
            segments.append(sub_mesh)
    return segments


def main():
    """
    mesh 和 data 中x的最大最小值一致，即xyz信息数据一致
    :return:
    """
    directory = r'E:\07-code\tunnelProject\analyzeProject\test\1'
    data = read_batch_csv(directory)
    # visualization_df(data, f"source")

    # 数据预处理
    data = filter_distance(data, 50)

    # 断面分割
    # seg_data = divide(data, 5)  # 断面大小为10m
    _, hull, _ = surface_by_hull(data)
    hull = highlight_all_triangles(hull)
    seg_data = divide_mesh(hull, 5)

    # 处理分割结果
    if seg_data:
        for i, e in enumerate(seg_data):
            # o3d.visualization.draw_geometries([e], window_name="Highlight Triangle")
            highlight_all_triangles(e, show=True)
            # visualization_df(e, f"segment_{i}")
            # e.to_csv(f"segment/segment_{i}.csv", index=False)


if __name__ == '__main__':
    main()
