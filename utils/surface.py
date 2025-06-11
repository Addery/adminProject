"""
@Author: zhang_zhiyi
@Date: 2024/11/22_15:24
@FileName:surface.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 提取点云数据表面
"""
import numpy as np
import open3d as o3d
from pandas import DataFrame

from utils.segment import pcd2df


def highlight_all_triangles(hull: o3d.geometry.TriangleMesh, show=False):
    """
    可视化所有三角形
    :param hull:
    :param show: 是否直接显示
    :return:
    """
    # 获取三角形索引和顶点坐标
    triangles = np.asarray(hull.triangles)
    vertices = np.asarray(hull.vertices)

    # 创建一个新三角网格，用于高亮显示
    highlight_mesh = o3d.geometry.TriangleMesh()

    # 存储所有高亮的顶点和三角形
    all_highlighted_vertices = []
    all_highlighted_triangles = []
    colors = []

    for i, triangle in enumerate(triangles):
        # 获取三角形顶点
        triangle_vertices = vertices[triangle]

        # 偏移索引（因为顶点需要连续编号）
        base_index = len(all_highlighted_vertices)

        # 添加当前三角形的顶点
        all_highlighted_vertices.extend(triangle_vertices)

        # 添加当前三角形的索引（注意偏移）
        all_highlighted_triangles.append([base_index, base_index + 1, base_index + 2])

        # 为每个三角形分配随机颜色
        random_color = np.random.rand(3)  # RGB 随机颜色
        colors.append(random_color)

    # 设置高亮网格的顶点、三角形和颜色
    highlight_mesh.vertices = o3d.utility.Vector3dVector(all_highlighted_vertices)
    highlight_mesh.triangles = o3d.utility.Vector3iVector(all_highlighted_triangles)
    highlight_mesh.vertex_colors = o3d.utility.Vector3dVector(
        np.repeat(colors, 3, axis=0)  # 每个顶点与其三角形共享同样的颜色
    )

    # 绘制原始凸包和高亮网格
    # o3d.visualization.draw_geometries([hull, highlight_mesh], window_name="Highlight All Triangles")
    if show:
        o3d.visualization.draw_geometries([highlight_mesh], window_name="Highlight All Triangles")
    return highlight_mesh


def surface_by_reconstruction(data: DataFrame, show=False):
    """
    使用 Open3D 的 Poisson Surface Reconstruction 或 Alpha Shapes 方法，将点云转为表面网格并填充缝隙
    :param data:
    :param show: 是否直接显示
    :return:
    """
    points = data[['X', 'Y', 'Z']].values
    # 读取或生成点云
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)  # 替换为实际点云数据

    # 法向量估计（构建表面的前提）
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=30))

    # Poisson表面重建
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd=point_cloud, depth=9)

    # 裁剪网格（移除多余的表面）
    bbox = point_cloud.get_axis_aligned_bounding_box()
    mesh = mesh.crop(bbox)

    if show:
        # 可视化结果
        o3d.visualization.draw_geometries([mesh], window_name="Closed Surface")
        highlight_all_triangles(mesh, show)
        # o3d.visualization.draw_geometries([point_cloud, mesh], window_name="Closed Surface")
    return point_cloud, mesh


def surface_by_alpha_shape(data: DataFrame, show=False):
    """
    Alpha Shapes 是通过调整参数来生成紧密包裹点云的表面
    :param data:
    :param show: 是否直接显示
    :return:
    """
    points = data[['X', 'Y', 'Z']].values
    # 读取或生成点云
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    # 使用 Alpha Shapes 生成表面
    alpha = 10  # 调整alpha值，影响封闭程度
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(point_cloud, alpha)

    if show:
        # 可视化结果
        # o3d.visualization.draw_geometries([point_cloud, mesh], window_name="Closed Surface")
        o3d.visualization.draw_geometries([mesh], window_name="Closed Surface")
        highlight_all_triangles(mesh, show)
    return point_cloud, mesh


def surface_by_hull(data: DataFrame, show=False):
    """
    如果点云的开放区域是平坦的，可以直接检测边界并填充多边形
    :param data:
    :param show: 是否直接显示
    :return:
    """
    try:
        points = data[['X', 'Y', 'Z']].values
        if len(points) < 4:
            # print("点云数据中点的数量不足，无法构建凸包")
            return None, None, None
        # 读取或生成点云
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

        # 提取边界
        hull, index_list = point_cloud.compute_convex_hull()
        hull.orient_triangles()  # 统一法向方向

        if show:
            # 可视化结果
            o3d.visualization.draw_geometries([point_cloud, hull], window_name="Closed Surface")
            # o3d.visualization.draw_geometries([hull], window_name="Closed Surface")

        return point_cloud, hull, index_list
    except Exception as e:
        print(f"发生错误: {e}")
        return None, None, None


def main():
    # data = read_csv(r"D:\myDesk\1731655263.7117808_3.csv")
    pcd = o3d.io.read_point_cloud(r"E:\07-code\tunnelProject\analyzeProject\backBreak\criterion.pcd")
    data = pcd2df(pcd)
    # visualization_df(data, f"segment")
    surface_by_reconstruction(data, show=True)  # 注重轮廓
    # surface_by_alpha_shape(data, show=True)
    # surface_by_hull(data, show=True)  # 注重规则轮廓


if __name__ == '__main__':
    main()
