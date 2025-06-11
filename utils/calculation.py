"""
@Author: zhang_zhiyi
@Date: 2024/11/22_15:05
@FileName:calculation.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 净空计算
"""
from pandas import DataFrame
import open3d as o3d

from utils.mesh import highlight_all_triangles
from utils.show import read_csv, visualization_df
from utils.surface import surface_by_hull


def radius(data: DataFrame):
    """
    计算断面半径
    :param data:
    :return:
    """
    visualization_df(data, f"segment")


def calculate_hull_metrics(hull: o3d.geometry.TriangleMesh):
    try:
        if not hull.is_watertight():
            # print("网格不是水密的！")
            hull = hull.simplify_quadric_decimation(target_number_of_triangles=1000)
            # highlight_all_triangles(hull)
            # hull.remove_non_manifold_edges()
            # hull = hull.fill_holes()
            # hull.compute_vertex_normals()

        # print("网格是水密的！")
        # 计算表面积
        surface_area = hull.get_surface_area()
        # 计算体积
        volume = hull.get_volume()
        return surface_area, volume
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 0, 0


def calculation(data: DataFrame, show=False):
    """
    净空计算
    :param data:
    :param show: 是否可视化
    :return:
    """
    # visualization_df(data)
    s, v = 0, 0
    try:
        pcd, hull, _ = surface_by_hull(data)
        if hull is not None:
            if show:
                o3d.visualization.draw_geometries([hull], window_name="Closed Surface")
                _ = highlight_all_triangles(hull, show=show)
            s, v = calculate_hull_metrics(hull)
        return s, v, hull
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 0, 0, None


def main():
    data = read_csv("../test/1/1731656822.6120367_0.csv")
    # data = read_csv("../utils/data.csv")
    visualization_df(data, f"source")
    s, v, mesh = calculation(data, show=True)
    print(f"表面积: {s}, 体积: {v}")
    pass


if __name__ == "__main__":
    main()
