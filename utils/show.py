"""
@Author: zhang_zhiyi
@Date: 2024/11/19_16:19
@FileName:show.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云数据显示脚本
"""
import os

import numpy as np
from pandas import DataFrame
import pandas as pd
import open3d as o3d

from utils.dfutils import df2pcd


def visualization_df(df: DataFrame, name: str = "test", folder_name: str = None) -> None:
    """
    可视化3D点云数据
    :param df: 3D点云数据
    :param name: 可视化图形名称
    :param folder_name: 用于创建保存过程数据的文件夹
    :return: None
    """
    points = df[['X', 'Y', 'Z']].values
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if {'R', 'G', 'B'}.issubset(df.columns):
        pcd.colors = o3d.utility.Vector3dVector(df[['R', 'G', 'B']].values)
    o3d.visualization.draw_geometries([pcd], window_name=name, width=1024, height=768)
    # 将结果写入文件
    # if folder_name is not None:
    #     write_pcd2ply(pcd, name, folder_name)


def visualization_df_by_dict(df_dict, name="test"):
    """
    传入保存 dataframe 格式的字典，合并数据，然后显示
    :param df_dict:
    :param name:
    :return:
    """
    res_df = None
    for k, v in df_dict.items():
        if res_df is None:
            res_df = v
            continue
        res_df = pd.concat([res_df, v], axis=0, ignore_index=True)
    visualization_df(res_df, name=name)


def show_single(data: DataFrame, name=None, color=None):
    """
    显示单个点云数据
    :param data: 点云数据
    :param name: 窗口名称
    :param color: 点云颜色
    :return:
    """
    try:
        if data is None:
            print("Point cloud data is None.")
            return
        # 创建点云对象
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)
        if color:
            if {'R', 'G', 'B'}.issubset(data.columns):
                pcd.colors = data[['R', 'G', 'B']].values
            else:
                default_color = np.zeros((len(data), 3))  # 初始化为全0
                default_color[:] = color
                pcd.colors = o3d.utility.Vector3dVector(default_color)
        # 可视化点云
        o3d.visualization.draw_geometries([pcd], window_name=name)
    except Exception as e:
        print(f"发生错误: {e}")


def show_batch(df_list: list, random_colors: list = None):
    """
    对比点云图
    :param df_list: 点云数据
    :param random_colors: 点云颜色
    :return:
    """
    pcds = []
    if not random_colors:
        random_colors = [[1, 0, 0]] * len(df_list)
    try:
        for data, color in zip(df_list, random_colors):
            if data is None:
                continue
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)
            if {'R', 'G', 'B'}.issubset(data.columns):
                pcd.colors = o3d.utility.Vector3dVector(data[['R', 'G', 'B']].values)
            else:
                default_color = np.zeros((len(data), 3))  # 初始化为全0
                default_color[:] = color
                pcd.colors = o3d.utility.Vector3dVector(default_color)
            pcds.append(pcd)
        # 可视化点云
        o3d.visualization.draw_geometries(pcds, window_name='compare')
    except Exception as e:
        print(f"发生错误: {e}")


def read_csv(path: str):
    """
    读取path保存的csv文件，并转化为DataFrame格式
    :param path:
    :return:
    """
    try:
        if not os.path.exists(path):
            print(f"CSV file {path} not found.")
            return
        if not os.path.isfile(path) or not path.lower().endswith('.csv'):
            print(f"Invalid file format for {path}. Only support CSV.")
            return
        # data = pd.read_csv(path, usecols=['X', 'Y', 'Z', 'R', 'G', 'B'])
        return pd.read_csv(path)
    except Exception as e:
        print(f"发生错误: {e}")


def read_batch_csv(path: str):
    """
    读取文件夹中所有保存点云数据的csv文件，并转化为DataFrame格式
    :param path:
    :return:
    """
    result = None
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.csv'):  # 读取CSV文件
                csv_path = os.path.join(path, entry.name)
                # data = pd.read_csv(csv_path, usecols=['X', 'Y', 'Z'])
                data = pd.read_csv(csv_path)
                if result is None:
                    result = data
                else:
                    result = pd.concat([result, data], axis=0)  # 按行合并
            elif entry.is_dir():
                read_batch_csv(entry.path)
    return result


def compare_show(df_list: list):
    """
    对比点云数据
    :param df_list:
    :return:
    """
    try:
        if not df_list:
            print("The point cloud list is empty.")
            return
        # num_clouds = len(df_list)
        # random_colors = np.random.rand(num_clouds, 3).tolist()
        random_colors = [[1, 0, 0], [0, 0, 1]]
        show_batch(df_list, random_colors)
    except Exception as e:
        print(f"发生错误: {e}")


def main_show():
    """
    show脚本测试入口
    :return:
    """
    directory = r'E:\07-code\tunnelProject\analyzeProject\source\2024-11-16\5\16_08\2'
    # directory = r'E:\07-code\tunnelProject\after\data\test_anomaly'
    tag = 2
    if tag == 1:
        data = read_batch_csv(directory)
        show_single(data, directory)
    elif tag == 2:
        for path in os.listdir(directory):
            data = read_csv(os.path.join(directory, path))
            show_single(data, path)


def main_compare():
    """
    对比点云脚本测试入口
    :return:
    """
    directory1 = r'E:\07-code\tunnelProject\analyzeProject\test\1'
    directory2 = r'E:\07-code\tunnelProject\analyzeProject\test\2'
    data1 = read_batch_csv(directory1)
    data2 = read_batch_csv(directory2)
    compare_show([data1, data2])


def clear_folder(folder_path):
    # 获取文件夹内的所有文件和文件夹
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # 如果是文件，删除文件
            if os.path.isfile(file_path):
                os.remove(file_path)
            # 如果是文件夹，递归删除文件夹内容
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # 删除空文件夹
        except Exception as e:
            print(f"Error removing {file_path}: {e}")


def read_pcd(path):
    pcd = o3d.io.read_point_cloud(path)
    o3d.visualization.draw_geometries([pcd])


if __name__ == '__main__':
    # main_show()
    # directory = r'E:\07-code\tunnelProject\analyzeProject\source\test'
    # data = read_batch_csv(directory)
    # data = read_csv(r"E:\07-code\tunnelProject\analyzeProject\rmq_data\2024_11_15 09-32-06-930581_1.csv")
    # show_single(data, name="test")
    # three_data = []
    # for row in data.itertuples():
    #     three_data.extend([row.X, row.Y, row.Z])
    # with open('three.txt', 'w') as file:
    #     file.write(str(three_data))

    # visualization_df(data)
    # pcd = df2pcd(data)
    # pcd = o3d.io.read_point_cloud(r"E:\pointcloundtools\01Semantic Segmentation Editor\sse-images\0003\0003.pcd")
    # o3d.visualization.draw_geometries([pcd])
    # o3d.io.write_point_cloud("../data/pcd/0075.pcd", pcd)
    # clear_folder(directory)
    read_pcd(r'E:\07-code\tunnelProject\analyzeProject\0001.pcd')
