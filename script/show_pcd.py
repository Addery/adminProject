"""
@Author: zhang_zhiyi
@Date: 2024/11/13_14:32
@FileName:show_pcd.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import pandas as pd
import open3d as o3d

file_path = r"E:\07-code\tunnelProject\data\2024-11-18\1731657173.381599_9.csv"

try:
    # 读取CSV文件
    data = pd.read_csv(file_path, usecols=['X', 'Y', 'Z'])
    # data = pd.read_csv(file_path, usecols=['X', 'Y', 'Z', 'R', 'G', 'B'])

    # 创建点云对象
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)
    # pcd.colors = o3d.utility.Vector3dVector(data[['R', 'G', 'B']].values / 255.0)

    # 可视化点云
    o3d.visualization.draw_geometries([pcd])

except FileNotFoundError:
    print("文件未找到，请检查路径是否正确。")
except KeyError as e:
    print(f"CSV 文件中缺少必要的列: {e}")
except Exception as e:
    print(f"发生错误: {e}")
