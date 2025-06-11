"""
@Author: zhang_zhiyi
@Date: 2024/11/26_9:49
@FileName:sampling.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 采样相关工具类
"""
import numpy as np
import open3d as o3d
from pandas import DataFrame

from utils.show import read_batch_csv, read_csv, visualization_df
from utils.surface import surface_by_hull


def upsample_by_mesh(mesh: o3d.geometry.TriangleMesh, number_of_points: int = 10000):
    """
    通过mesh进行上采样
    :param mesh:
    :param number_of_points:
    :return:
    """
    dense_pcd = mesh.sample_points_uniformly(number_of_points=number_of_points)
    return dense_pcd


def upsample_by_interpolation(data: DataFrame):
    # 读取点云
    points = data[['X', 'Y', 'Z']].values
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # 设置上采样倍数
    upsample_factor = 2
    new_points = []

    # 简单插值算法：在两个邻点之间生成中点
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            midpoint = (points[i] + points[j]) / 2
            new_points.append(midpoint)

    # 将原始点和新生成点合并
    all_points = np.vstack((points, new_points))

    # 创建新的点云
    dense_pcd = o3d.geometry.PointCloud()
    dense_pcd.points = o3d.utility.Vector3dVector(all_points)

    # 可视化结果
    o3d.visualization.draw_geometries([dense_pcd])


def main():
    directory = r'E:\07-code\tunnelProject\analyzeProject\test\1\1731656822.6120367_0.csv'
    # data = read_batch_csv(directory)
    data = read_csv(directory)
    visualization_df(data, f"segment")
    _, mesh, _ = surface_by_hull(data)
    upsampled_pcd = upsample_by_mesh(mesh)
    o3d.visualization.draw_geometries([upsampled_pcd])


if __name__ == "__main__":
    main()
