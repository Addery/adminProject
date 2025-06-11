"""
@Author: zhang_zhiyi
@Date: 2024/11/20_10:22
@FileName:preprocess.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云预处理
"""
import configparser
import os
import re
import sympy as sp
from sympy import lambdify, symbols
from decimal import getcontext, Decimal
import numpy as np
from pandas import DataFrame
from typing import Tuple
from matplotlib import pyplot as plt
import open3d as o3d
from open3d.cpu.pybind.geometry import PointCloud

from utils.dfutils import df2pcd
from utils.show import read_batch_csv


# DEFAULT_ORG_PATH = "../config/orgconfig.ini"
# DEFAULT_INIT_PATH = "../config/init_parameter.ini"

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
# 获取上一级目录的绝对路径
parent_dir = os.path.dirname(os.path.dirname(script_path))

# 构造配置文件的绝对路径
DEFAULT_ORG_PATH = os.path.join(parent_dir, "config", "orgconfig.ini")
DEFAULT_INIT_PATH = os.path.join(parent_dir, "config", "init_parameter.ini")


def ransac(pcd: PointCloud) -> Tuple[list, PointCloud, PointCloud, str]:
    """
    RANSAC平面分割算法
    :param pcd: pcd数据
    :return: 内部点索引列表, 内部点云, 外部点云, 平面方程
    """
    # RANSAC算法参数
    distance_threshold = 1  # 内点到平面模型的最大距离
    ransac_n = 3  # 用于拟合平面的采样点数
    num_iterations = 1000  # 最大迭代次数

    # 执行算法，返回模型系数plane_model和内点索引inliers
    plane_model, inliers = pcd.segment_plane(distance_threshold, ransac_n, num_iterations)

    # 构造平面方程
    [a, b, c, d] = plane_model
    eq = f"{a:.6f} * x + {b:.6f} * y + {c:.6f} * z + {d:.6f} = 0"
    # print(f"Plane equation: {equipment}")

    # 平面内点点云
    inlier_cloud = pcd.select_by_index(inliers)
    inlier_cloud.colors = o3d.utility.Vector3dVector(np.ones((len(inlier_cloud.points), 3)) * 0.3)
    # print(f"平面内的点云：{inlier_cloud}")

    # 平面外点点云
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    outlier_cloud.colors = o3d.utility.Vector3dVector(np.ones((len(outlier_cloud.points), 3)) * 0.7)
    # print(f"平面外的点云：{outlier_cloud}")

    # 设置点云颜色
    inlier_cloud.paint_uniform_color([1, 0, 0])  # 将内点云设置为红色
    outlier_cloud.paint_uniform_color([0, 0, 1])  # 将外点云设置为蓝色

    # inliers: 返回平面内点索引, inlier_cloud: 平面内点点云, outlier_cloud: 平面外点点云, equipment: 平面方程
    return inliers, inlier_cloud, outlier_cloud, eq


def update(df: DataFrame, inners: list) -> DataFrame:
    """
    标记内点和外点
    :param df: 原始3D点云数据数据
    :param inners: 内部点索引列表
    :return: 添加label标签后的3D点云数据
    """
    # 标记内点和外点
    df['label'] = 'outlier'
    df.loc[inners, 'label'] = 'inlier'
    return df


def filter_label(df: DataFrame, label: str, target: str) -> DataFrame:
    """
    根据标签过滤3D点云数据
    :param df: 3D点云原始数据
    :param label: 过滤的标签
    :param target: 保留的目标值
    :return: 过滤后的3D点云数据
    """
    res = df[df[label] == target]
    df.reset_index(drop=True, inplace=True)
    return res


class SurfaceEquation(object):
    """
    方程类：主要用于检测平面或者曲面是否方程表达式
    """

    def __init__(self, symbols: list, equation_str: str):
        """
        SurfaceEquation构造器
        :param symbols: 需要定义的符号变量列表
        :param equation_str: 字符串形式的方程表达式
        """
        self.symbols = symbols  # 符号变量列表
        self.equation = equation_str  # 方程表达式

        # 方程表达式至少要有两个变量
        if len(symbols) != 3:
            raise ValueError("The 'symbols' list must have 3 elements.")

        # 定义符号变量
        self.x, self.y, self.z = sp.symbols(self.symbols)
        # 解析方程字符串为 sympy 表达式，并改为等式形式
        self.equation = sp.Eq(sp.sympify(equation_str.split('=')[0]), sp.sympify(equation_str.split('=')[1]))
        # 求解方程，得到以z为目标的表达式
        self.z_eq = sp.solve(self.equation, self.z)[0]
        # 编译表达式
        self.curve_func = lambdify((self.x, self.y), self.z_eq, 'numpy')

    def curve_equation(self, x_val, y_val):
        """
        根据x_val, y_val和平面方程计算z_val
        :param x_val: 计算值
        :param y_val: 计算值
        :return: 计算结果
        """
        z = self.z_eq.evalf(subs={self.x: x_val, self.y: y_val})
        return z

    @staticmethod
    def get_coefficient_mean(coefficients_1: list, coefficients_2: list):
        """
        求两个方程系数的均值
            coefficients = {
                'x**2': 0,
                'x*y': 0,
                'y**2': 0,
                'x': 0,
                'y': 0,
                'constant': 0
            }
        :param coefficients_1:
        :param coefficients_2:
        :return:
        """
        # res_list = []
        # for p1, p2 in zip(coefficients_1, coefficients_2):
        #     temp = float(p1) + float(p2)
        #     res_list.append(0) if temp == 0 else res_list.append(round(temp / 2, 3))
        # return res_list

        # keys = ['x**2', 'x*y', 'y**2', 'x', 'y', 'constant']
        # res_dict = {}
        # for k in keys:
        #     res_dict[k] = np.mean([(coefficients_1.get(k) + coefficients_2.get(k))])
        # return res_dict

        getcontext().prec = 3
        res_list = []
        for p1, p2 in zip(coefficients_1, coefficients_2):
            d1, d2 = Decimal(float(p1)), Decimal(float(p2))
            temp = d1 + d2
            res_list.append(0) if temp == 0 else res_list.append(temp / 2)
        return res_list

    @staticmethod
    def get_coefficient(equation_str: str):
        """
        提取二次曲面方程系数
        :param equation_str: 二次曲面等式方程
        :return:
        """
        # 使用正则表达式提取各项的系数
        pattern = r'([-+]?\d*\.?\d+)?\s*\*?\s*([xy]\*\*\d+|[xy])'
        matches = re.findall(pattern, equation_str)

        # 初始化系数字典
        coefficients = {
            'x**2': 0,
            'x*y': 0,
            'y**2': 0,
            'x': 0,
            'y': 0,
            'constant': 0
        }

        # 遍历匹配结果
        for coeff, term in matches:
            coeff = float(coeff) if coeff else 1.0  # 处理省略的系数
            if term == 'x**2':
                coefficients['x**2'] += coeff
            elif term == 'x*y':
                coefficients['x*y'] += coeff
            elif term == 'y**2':
                coefficients['y**2'] += coeff
            elif term == 'x':
                coefficients['x'] += coeff
            elif term == 'y':
                coefficients['y'] += coeff

        # 处理常数项
        constant_pattern = r'([-+]?\d*\.?\d+)(?=\s*$)'
        constant_match = re.search(constant_pattern, equation_str)
        if constant_match:
            coefficients['constant'] = float(constant_match.group(0))

        return coefficients

    @staticmethod
    def reconstruct_equation(coefficients_mean: dict):
        """
        重建方程
            coefficients = {
                'x**2': 0,
                'x*y': 0,
                '': 0,
                'x': 0,
                'y': 0,
                'constant': 0
            }
        :param coefficients_mean: 方程的新系数
        :return:
        """
        # 定义符号
        x, y = sp.symbols('x y')
        new_equation = (coefficients_mean.get('x**2') * x ** 2 +
                        coefficients_mean.get('x*y') * x * y +
                        coefficients_mean.get('y**2') * y ** 2 +
                        coefficients_mean.get('x') * x +
                        coefficients_mean.get('y') * y +
                        coefficients_mean.get('constant'))
        equation_str = "z=" + str(new_equation)
        return equation_str

    def check_curve_equation(self, df, tolerance: float, name: str) -> Tuple[DataFrame, str]:
        """
        根据是否满足方程表达式对df数据进行分类
        :param df: 原始3D点云数据
        :param tolerance: 容许的误差范围
        :param name: 方程表达式表示的曲面名称
        :return: 添加分类标签的3D点云数据, 新添加的标签
        """
        # 计算z值
        x_val = df['X'].values
        y_val = df['Y'].values
        z_val = df['Z'].values
        # expected_z = np.array([float(self.curve_equation(x, y)) for x, y in zip(x_val, y_val)])

        # 矢量化计算expected_z
        # expected_z = self.curve_equation(x_val, y_val)
        # 确保expected_z是一个NumPy数组
        # expected_z = np.asarray(expected_z)

        expected_z = self.curve_func(df['X'].values, df['Y'].values)
        # 将计算所得z值与实际z值进行比对, satisfies布尔数组numpy.ndarray
        satisfies = np.abs(z_val - expected_z) < tolerance
        # 使用矢量化操作创建标签列, labels字符串数组numpy.ndarray
        labels = np.where(satisfies, 'True', 'False')
        # 在数据中添加标签
        label_name = f'{name}'
        df[label_name] = labels
        return df, label_name

    @staticmethod
    def fit_surface_equation(df: DataFrame, name: str, folder_name: str = None):
        """
        拟合曲面方程
        :param df: DataFrame格式，拟合曲面方程的点云数据
        :param name: 数据处理过程的保存名称
        :param folder_name: 数据处理过程的保存文件夹
        :return: 二次曲面方程，等式形式
        """
        try:
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

            pcd = df2pcd(df)
            cloud_points = np.asarray(pcd.points)
            result = SurfaceEquation.quadric_surface_fitting(cloud_points)
            # 构造曲面方程形式
            function = "z=%.6s*x**2%.6s*x*y%.6s*y**2%.6s*x%.6s*y%.6s" % (
                SurfaceEquation.fun(result[0]), SurfaceEquation.fun(result[1]), SurfaceEquation.fun(result[2]),
                SurfaceEquation.fun(result[3]), SurfaceEquation.fun(result[4]), SurfaceEquation.fun(result[5]))
            # 输出方程
            # print(f"Quadric surface equation: {function}")
            # 可视化原始数据
            # o3d.visualization.draw_geometries([pcd], window_name="可视化输入点云",
            #                                   width=1024, height=768,
            #                                   left=50, top=50, mesh_show_back_face=False)

            # 画曲面图和离散点
            # fig = plt.figure()  # 建立一个空间
            # ax = fig.add_subplot(111, projection='3d')  # 3D坐标
            # n = 256
            # u = np.linspace(-20, 20, n)  # 创建一个等差数列
            # x, y = np.meshgrid(u, u)  # 转化成矩阵
            # 给出方程
            # z = result[0] * x * x + result[1] * x * y + result[2] * y * y + result[3] * x + result[4] * y + result[5]
            # 使用 jet colormap画出拟合曲面
            # jet = colormaps.get_cmap('jet')
            # ax.plot_surface(x, y, z, rstride=3, cstride=3, cmap=jet)
            """
            # 画出点
            X = cloud_points[:, 0]
            Y = cloud_points[:, 1]
            Z = cloud_points[:, 2]
            ax.scatter(X, Y, Z, c='black')
            """
            # 过程数据保存路径
            # save_folder_path = f"E:\\07-code\\remote_github\\tunnelProjectTest\config\\res\\{folder_name}"
            # 如果目录不存在，则创建目录
            # if not os.path.exists(save_folder_path):
            #     os.makedirs(save_folder_path)
            #
            # save_path = os.path.join(save_folder_path, f"{name}.png")

            # plt.title("最小二乘法拟合的二次曲面")
            # plt.tight_layout()
            # plt.savefig(save_path)
            # plt.show()
            return function, [result[0], result[1], result[2], result[3], result[4], result[5]]
        except Exception as e:
            print(f"{str(e)}: A error in fit_surface_equation")
            return None

    @staticmethod
    def quadric_surface_fitting(points: np.ndarray) -> np.ndarray:
        """
        二次曲面方程:z(x,y)=ax^2+bxy+cy^2+dx+ey+f
        :param points: 待拟合的点坐标
        :return: 二次曲面方程的系数
        """
        X = points[:, 0]
        Y = points[:, 1]
        Z = points[:, 2]
        N = points.shape[0]
        A = np.array([[sum(X ** 4), sum(X ** 3 * Y), sum(X ** 2 * Y ** 2), sum(X ** 3), sum(X ** 2 * Y), sum(X ** 2)],
                      [sum(X ** 3 * Y), sum(X ** 2 * Y ** 2), sum(X * Y ** 3), sum(X ** 2 * Y), sum(X * Y ** 2),
                       sum(X * Y)],
                      [sum(X ** 2 * Y ** 2), sum(X * Y ** 3), sum(Y ** 4), sum(X * Y ** 2), sum(Y ** 3), sum(Y ** 2)],
                      [sum(X ** 3), sum(X ** 2 * Y), sum(X * Y ** 2), sum(X ** 2), sum(X * Y), sum(X)],
                      [sum(X ** 2 * Y), sum(X * Y ** 2), sum(Y ** 3), sum(X * Y), sum(Y ** 2), sum(Y)],
                      [sum(X ** 2), sum(X * Y), sum(Y ** 2), sum(X), sum(Y), N]])
        B = np.array([sum(Z * X ** 2), sum(Z * X * Y), sum(Z * Y ** 2), sum(Z * X), sum(Z * Y), sum(Z)])
        # 高斯消元法解线性方程
        """
        numpy.linalg.LinAlgError: Singular matrix 奇异矩阵，无法求解
        """
        res = np.linalg.solve(A, B.T)
        return res

    @staticmethod
    def segment(df: DataFrame) -> Tuple[DataFrame, PointCloud, PointCloud, str]:
        """
        3D点云平面分割
        :param df: 3D点云数据
        :return: 分割后带有label的3D点云数据, 内部点云, 外部点云, 平面方程
        """
        pcd = df2pcd(df)
        # RANSAC平面分割算法
        inners, inlier, outlier, eq = ransac(pcd)
        # 标记内点和外点
        res = update(df, inners)
        # 返回分割结果
        return res, inlier, outlier, eq

    @staticmethod
    def filter_equation(df: DataFrame, symbols: list, equation: str, tolerance: float, target: str,
                        name: str) -> DataFrame:
        """
        根据表达式过滤3D点云数据
        :param df: 原始3D点云数据
        :param symbols: 需要定义的符号变量列表
        :param equation: 字符串形式的方程表达式
        :param tolerance: 容许的误差范围
        :param target: 希望保留数据的标签值
        :param name: 方程表达式表示的曲面名称
        :return: 过滤后的3D点云数据
        """
        # 实例化SurfaceEquation对象
        se = SurfaceEquation(symbols, equation)
        # 根据equation方式表达式对df数据进行分类标记 TODO: 速度较慢，需要优化
        res, label = se.check_curve_equation(df, tolerance, name)
        # 根据新标记的标签进行过滤
        res = filter_label(res, label, target)
        return res

    @staticmethod
    def fun(x) -> str:
        """
        处理符号问题，主要用于表达式输出显示。
        :param x:
        :return:
        """
        round(x, 2)
        if x >= 0:
            return '+' + str(x)
        else:
            return str(x)


def remove_nan(df: DataFrame) -> DataFrame:
    """
    去除3D点云数据中的NaN值
    :param df: 3D点云数据
    :return: 去除后的DataFrame数据
    """
    tag = ((df['X'] != 0) & (df['Y'] != 0) & (df['Z'] != 0)) & (df['Reflectivity'] != 0)
    df = df[tag]
    df.reset_index(drop=True, inplace=True)
    return df


def filter_distance(df: DataFrame, distance) -> DataFrame:
    """
    过滤3D点云数据深度在 distance米 以外的数据
    :param df: 3D点云数据
    :param distance: 深度值
    :return: 过滤后的DataFrame数据
    """
    df = df[df['X'] < distance]
    df.reset_index(drop=True, inplace=True)
    return df


def calculate_gap(df: DataFrame, threshold: float = 0.0005) -> float:
    """
    计算 隧道的实际高度 和 点云数据最高点 两者的差距，用于calibrate_data()校准坐标数据以0为起点
    :param df: 3D点云对象
    :param threshold: 选取计算z轴最高处的范围
    """
    config = configparser.ConfigParser()
    config.read(DEFAULT_ORG_PATH)
    real_high = int(config.get('orgparameter', 'orghight'))
    # 获取点云数据的全部z坐标数据
    z_vals = df.loc[:, 'Z']
    # 从大到小排序
    sorted_arr = np.sort(z_vals, kind='mergesort')[::-1]
    # 计算threshold的位置
    percentile = int(len(sorted_arr) * threshold)
    if percentile == 0:
        percentile = 1
    # 截取前threshold的数据
    target_arr = sorted_arr[:percentile]
    # 求平均值
    max_z = target_arr.mean()
    # 计算差值并返回
    return real_high - max_z


def calibrate_data(df: DataFrame, gap: float) -> DataFrame:
    """
    校准点云z坐标数据
    :param df: 3D点云数据
    :param gap: 差值
    :return: 过滤后的DataFrame数据
    """
    # 分离z坐标
    z = df.loc[:, 'Z']
    # 坐标校准
    df.loc[:, 'Z'] = z + gap
    return df


def filter_high(df: DataFrame, height) -> DataFrame:
    """
    过滤3D点云数据高度在 high米 以下的数据
    :param df: 3D点云数据
    :param height: 高度值
    :return: 过滤后的DataFrame数据
    """
    df = df[df['Z'] > height]
    df.reset_index(drop=True, inplace=True)
    return df


def preprocess(data: DataFrame, high=2.5, distance=50, folder_name: str = None, init_path=DEFAULT_INIT_PATH):
    """
    预处理DataFrame数据
    TODO: 平面过滤、曲面过滤策略优化
    :param data: 原始DataFrame数据
    :param high: 要过滤的隧道高度
    :param distance: 要过滤的深度
    :param folder_name: 若要保存过程数据，这是保存的文件夹
    :param init_path: 初始化参数配置文件路径
    :return: 处理后的DataFrame数据
    """
    try:
        # visualization_df(data, "original_data", folder_name)
        # 去除数据中的NaN值
        data = remove_nan(data)
        # visualization_df(data, "remove_nan", folder_name)
        # 过滤深度在50m以外的数据
        data = filter_distance(data, distance)
        # visualization_df(data, "filter_by_distance", folder_name)
        # 校准Z轴坐标
        data = calibrate_data(data, gap=calculate_gap(data))
        # 过滤高度在2米以下的数据
        data = filter_high(data, high)
        # visualization_df(data, "filter_by_height", folder_name)

        # 点云分割
        # config, inner, outer, equation = SurfaceEquation.segment(data)
        # visualization_pcd([inner, service], "res_segment")
        # 根据分割结果所新添的标签过滤点云数据
        # config = filter_label(config, 'label', 'outlier')
        # visualization_df(config, "filter_ground_by_label", folder_name)
        # 根据拟合隧道底面平面方程过滤点云数据
        # config = SurfaceEquation.filter_equation(data, ['x', 'y', 'z'], equation, 1.5, 'False', 'ground')
        # visualization_df(config, "filter_ground_by_function", folder_name)

        # 拟合隧道曲面方程，并使用方程过滤点云数据
        quadric_equation, _ = SurfaceEquation.fit_surface_equation(data, "quadric_surface_function", folder_name)
        print(quadric_equation)
        data = SurfaceEquation.filter_equation(data, ['x', 'y', 'z'], quadric_equation, 1, 'True', 'quadric_surface')
        # visualization_df(data, "filter_quadric_surface_by_function", folder_name)
        return data
    except Exception as e:
        print(f"{str(e)}: a error in preprocess")


def preprocess_batch(data_list):
    """
    批量预处理DataFrame数据
    :param data_list: 原始DataFrame数据列表
    :return: 处理后的DataFrame数据列表
    """
    res_list = []
    for data in data_list:
        res_list.append(preprocess(data))
    return res_list


def main():
    directory1 = r'E:\07-code\tunnelProject\analyzeProject\test\1'
    data1 = read_batch_csv(directory1)
    preprocess(data1)


if __name__ == "__main__":
    main()
