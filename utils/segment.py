"""
@Author: zhang_zhiyi
@Date: 2024/11/20_15:15
@FileName:segment.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云区域分割
"""
import datetime
import time

from utils.preprocess import preprocess
from utils.show import read_csv, show_batch, show_single, read_batch_csv

from typing import List
from pandas import DataFrame
import open3d as o3d
import os
import numpy as np
import pandas as pd
from open3d.cpu.pybind.geometry import PointCloud


def pcd2df(pcd: PointCloud) -> DataFrame:
    """
    将PointCloud数据转化为DataFrame格式
    :param pcd: PointCloud
    :return: DataFrame
    """
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors) if pcd.colors else None
    normals = np.asarray(pcd.normals) if pcd.normals else None
    # print(type(points))  # <class 'numpy.ndarray'>

    data = {
        'X': points[:, 0],
        'Y': points[:, 1],
        'Z': points[:, 2]
    }

    if colors is not None:
        data['R'] = colors[:, 0]
        data['G'] = colors[:, 1]
        data['B'] = colors[:, 2]

    if normals is not None:
        data['NX'] = normals[:, 0]
        data['NY'] = normals[:, 1]
        data['NZ'] = normals[:, 2]

    return pd.DataFrame(data)


class Region(object):
    """
    投影面类：xy轴形成的投影面
    """
    MIN_X, MAX_X = 0, 60  # 投影面x轴的范围，单位米
    MIN_Y, MAX_Y = -10, 10  # 投影面y轴的范围，单位米
    GRID_SIZE = 0.5  # 投影面每个网格的大小，单位米

    def __init__(self):
        self.pcds = {}  # 子区域点云字典，索引：数据

    def set_pcd(self, index, pcd) -> None:
        """
        向子区域点云列表添加数据
        :param index: 区域索引
        :param pcd: DataFrame格式点云数据
        :return: None
        """
        self.pcds[index] = pcd

    def get_pcds(self):
        """
        获取子区域点云列表
        :return:
        """
        return self.pcds


class Segment(object):
    """
    点云区域划分类：根据点云投影到固定的xy投影面的区域划分点云
    """

    def __init__(self, data_list: list):
        self.data_list = data_list  # DataFrame点云数据列表
        self.res_list = []  # 划分区域后的子点云数据列表

    def segment(self) -> List[Region]:
        """
        划分区域
        :return: 划分结果: 子点云数据列表 List[Region]
        """
        # 遍历self.data_list
        for data in self.data_list:
            # 过滤高度在2.5米以下的数据
            # config = filter_high(config, height=2.5)
            if data is not None:
                # 划分区域
                geometries = Segment.subdivide(data)
                self.res_list.append(geometries)

        # 返回划分结果
        return self.res_list

    @staticmethod
    def subdivide(data: DataFrame) -> Region:
        """
        划分子区域
        :param data: 原始数据
        :return: 划分结果，PointCloud列表
        """
        # 提取x, y, z坐标信息
        points = data[['X', 'Y', 'Z']].values
        # 创建 Open3D 点云对象
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        # 投影到二维平面 (x, y)，忽略 z 坐标
        points_2d = points[:, :2]

        # 定义网格大小和区域数量
        num_x = int(np.ceil((Region.MAX_X - Region.MIN_X) / Region.GRID_SIZE))
        num_y = int(np.ceil((Region.MAX_Y - Region.MIN_Y) / Region.GRID_SIZE))

        # 划分点云数据到多个小区域
        regions = [[] for _ in range(num_x * num_y)]
        for idx, point in enumerate(points_2d):
            x_idx = int(point[0] // Region.GRID_SIZE)
            y_idx = int((point[1] - Region.MIN_Y) // Region.GRID_SIZE)
            region_idx = x_idx + y_idx * num_x
            if 0 <= region_idx < len(regions):
                regions[region_idx].append(idx)

        # 创建颜色映射
        colors = np.random.rand(num_x * num_y, 3)  # 随机生成颜色

        # 创建 Open3D 点云对象列表
        geometries = Region()
        for region_idx, point_indices in enumerate(regions):
            if point_indices:  # 如果该区域有数据
                region_points = points[point_indices]
                pcd_region = o3d.geometry.PointCloud()
                pcd_region.points = o3d.utility.Vector3dVector(region_points)
                color = colors[region_idx]
                pcd_region.paint_uniform_color(color)
                # vis = o3d.visualization.Visualizer()
                # vis.create_window(window_name="Region Coloring", width=1024, height=768)
                # vis.add_geometry(pcd_region)
                #
                # # 渲染并关闭窗口
                # vis.run()
                # vis.destroy_window()
                # pcd.colors = o3d.utility.Vector3dVector(color)

                df_region = pcd2df(pcd_region)
                # show_single(df_region, 'test')
                # 向区域点云对象的列表中添加数据，DataFrame格式
                geometries.set_pcd(region_idx, df_region)
            else:  # 该区域没有数据，直接用None填充
                geometries.set_pcd(region_idx, None)
        # print(type(geometries), geometries)
        # print(type(geometries.get_pcds()), geometries.get_pcds())
        # 创建 Open3D 可视化窗口并添加几何体
        # vis = o3d.visualization.Visualizer()
        # vis.create_window(window_name="Region Coloring", width=1024, height=768)
        # for k, geometry in geometries.get_pcds().items():
        #     print(type(k), k)
        #     print(type(geometry), geometry)
        #
        #     if geometry is not None:
        #         vis.add_geometry(geometry)
        #
        # # 渲染并关闭窗口
        # vis.run()
        # vis.destroy_window()

        # 返回划分区域的子点云列表对象
        return geometries


def segment_batch(data_list, show=False):
    """
    批处理点云区域划分
    :param data_list: 原始数据列表
    :param show: 是否显示分割后的点云
    :return: 批处理结果：子点云数据列表 List[Region]
    """
    segment = Segment(data_list)
    geometries_list = segment.segment()
    if show:
        # 显示分割后的点云
        for geometries in geometries_list:
            region_dict = geometries.get_pcds()
            show_batch(list(region_dict.values()))
    return geometries_list


def main():
    directory1 = r'E:\07-code\tunnelProject\analyzeProject\test\1'
    directory2 = r'E:\07-code\tunnelProject\analyzeProject\test\2'
    data1 = preprocess(read_batch_csv(directory1))
    data2 = preprocess(read_batch_csv(directory2))
    data_list = [data1, data2]

    segment = Segment(data_list)
    geometries_list = segment.segment()
    for geometries in geometries_list:
        region_dict = geometries.get_pcds()
        show_batch(list(region_dict.values()))


if __name__ == '__main__':
    main()
