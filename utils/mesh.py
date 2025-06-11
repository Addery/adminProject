"""
@Author: zhang_zhiyi
@Date: 2024/11/22_15:47
@FileName:mesh.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: TriangleMesh 相关
"""
import numpy as np
import open3d as o3d
from pandas import DataFrame

from utils.show import read_csv
from utils.surface import surface_by_hull, surface_by_alpha_shape, surface_by_reconstruction


def view_hull_triangles(hull: o3d.geometry.TriangleMesh):
    """
    查看mesh三角形面信息（顶点索引、顶点坐标）
    :param hull:
    :return:
    """
    # 获取三角形的顶点索引
    triangles = np.asarray(hull.triangles)  # 每个三角形由三个顶点的索引组成
    # 获取顶点坐标
    vertices = np.asarray(hull.vertices)  # 所有顶点的坐标

    print(f"总共有 {len(triangles)} 个三角形面")
    for i, triangle in enumerate(triangles):
        print(f"三角形 {i + 1}: 顶点索引 {triangle}, 顶点坐标:")
        for idx in triangle:
            print(f"  顶点 {idx}: {vertices[idx]}")

    return triangles, vertices


def highlight_triangle(hull: o3d.geometry.TriangleMesh, triangle_idx: int):
    """
    可视化单个三角形
    :param hull:
    :param triangle_idx:
    :return:
    """
    # 获取三角形索引
    triangles = np.asarray(hull.triangles)
    vertices = np.asarray(hull.vertices)

    # 获取特定三角形的顶点
    triangle = triangles[triangle_idx]
    triangle_vertices = vertices[triangle]

    # 创建一个新点云，表示高亮的三角形
    highlight = o3d.geometry.TriangleMesh()
    highlight.vertices = o3d.utility.Vector3dVector(triangle_vertices)
    highlight.triangles = o3d.utility.Vector3iVector([[0, 1, 2]])
    highlight.paint_uniform_color([1, 0, 0])  # 高亮颜色：红色

    # 绘制原始凸包和高亮三角形
    o3d.visualization.draw_geometries([hull, highlight], window_name="Highlight Triangle")


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


def calculate_hull(data: DataFrame):
    points = data[['X', 'Y', 'Z']].values
    # 读取或生成点云
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    colors = np.full((data.shape[0], 3), [0, 0.3, 0.2])
    pcd.colors = o3d.utility.Vector3dVector(colors)
    print(pcd)  # 输出点云点的个数

    hull, idx = pcd.compute_convex_hull()
    hull_cloud = pcd.select_by_index(idx)
    o3d.io.write_point_cloud("hull_cloud.pcd", hull_cloud)  # 获取凸包顶点
    hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
    hull_ls.paint_uniform_color((1, 0, 0))
    o3d.visualization.draw_geometries([pcd, hull_ls])
    return pcd, hull_ls


def main():
    data = read_csv("../test/1/1731656822.6120367_0.csv")
    _, hull, _ = surface_by_hull(data)
    o3d.visualization.draw_geometries([hull], window_name="Highlight All Triangles")
    # _, hull = surface_by_alpha_shape(data)
    # _, hull = surface_by_reconstruction(data)
    # triangles, vertices = view_hull_triangles(hull)
    # highlight_triangle(hull, 0)
    highlight_all_triangles(hull, show=True)
    pass


if __name__ == '__main__':
    main()
