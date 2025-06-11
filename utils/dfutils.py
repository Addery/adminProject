"""
@Author: zhang_zhiyi
@Date: 2024/12/18_14:40
@FileName:dfutils.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import pandas as pd
from open3d.cpu.pybind.geometry import PointCloud
from pandas import DataFrame
import open3d as o3d


def df2pcd(data: DataFrame) -> PointCloud:
    """
    转换3D点云数据格式：DataFrame--->PointCloud
    :param data: 原始DataFrame格式的3D点云数据
    :return: PointCloud3D点云格式
    """
    # 创建 Open3D 点云对象
    pcd = o3d.geometry.PointCloud()
    if {'X', 'Y', 'Z'}.issubset(data.columns):
        points = data[['X', 'Y', 'Z']].values
        pcd.points = o3d.utility.Vector3dVector(points)
    if {'R', 'G', 'B'}.issubset(data.columns):
        colors = data[['R', 'G', 'B']].values
        pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd


if __name__ == '__main__':
    file_path = r"E:\07-code\tunnelProject\analyzeProject\data\2024-11-18\1731634326.7545216_0.csv"
    df = pd.read_csv(file_path)
    df2pcd(df)



