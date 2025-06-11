"""
@Author: zhang_zhiyi
@Date: 2024/10/24_15:32
@FileName:pcd_db_op.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云数据操作路由 本地文件保存点云数据，数据库保存日志信息
    <p>
    数据库中需要的字段：
    项目信息（项目编号、隧道编号、工作面编号、结构物编号、里程、中控设备编号、采集设备编号、公司编号）
    采集时间
    文件存储相关（初始化完整点云数据路径、初始化点云区域数据路径、异常点云数据路径）
    TODO：初始化方程
    初始化点云更新计数器（初始化完整点云数据、初始化点云区域数据）（在初始化操作之后，每扫描10次更新一次）
"""
import ast
import os
import random
import time
from datetime import datetime, timedelta

import pandas as pd
# from datetime import datetime
from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor
import open3d as o3d

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.pcdHttpStatus import PCDHttpStatus
from utils.util_database import DBUtils
from utils.util_file import FileUtils
from utils.util_pcd import get_path, get_history, get_path_by_time, get_pcd_list, compare_log_information, \
    get_xyz_rgb_list, data_is_overdue
from spaceCalculation.space_calculation import run

pcd_db_op = Blueprint('pcd_db_op', __name__)

SAVE_DIR = 'D:/tunnelProject/adminProject/data'


@pcd_db_op.route('/logByCodeOrDate', methods=['POST'])
def log_by_code_or_date():
    """
    检索日志信息
    可以通过ProCode、TunCode、WorkSurCode、StruCode、ConEquipCode、DataAcqEquipCode、Year、Month、Day、Hour、Minute、Second
    中任意组合作为条件去数据库表中进行检索获得负责要求的log_desc数据
    :return:
    """
    try:
        data = request.json
        return jsonify(DBUtils.get_log_by_columns(data)), 200
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/historyCodeAndDate', methods=['POST'])
def history_by_code_and_date():
    """
    检索历史记录
    :return:
    """
    try:
        data = request.json
        filters = {
            "DataAcqEquipCode": data.get('DataAcqEquipCode', None),
            "Year": data.get('Year', 0),
            "Month": data.get('Month', 0),
            "Day": data.get('Day', 0),
            "Hour": data.get('Hour', 0),
            "Minute": data.get('Minute', 0),
            "Second": data.get('Second', 0)
        }
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200
    con = None
    cursor = None
    try:
        # 校验必填字段
        if not all([filters.get('DataAcqEquipCode'), str(filters.get('Year')), str(filters.get('Month')),
                    str(filters.get('Day')), str(filters.get('Hour')), str(filters.get('Minute')),
                    str(filters.get('Second'))]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        con.autocommit(False)

        # TODO: 判断是否是三天内的数据
        if not data_is_overdue(filters):
            return jsonify({'code': PCDHttpStatus.DATA_OVERDUE.value, 'msg': '只展示三天内的数据', 'data': {}}), 200

        # 获取目录路径
        data_path = get_path_by_time(filters)
        # path, data_path = get_path(filters, 'data', 'history', 'history')
        if data_path is None:  # 该时间点不存在雷达采集数据事件
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': '不存在历史数据', 'data': {}}), 200
        init_region_path = os.path.join('data', str(filters.get('DataAcqEquipCode')), 'data', 'init', 'regions')
        if not os.path.exists(init_region_path):
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': '不存在初始化数据', 'data': {}}), 200

        # 判断该时间点是否有异常数据
        sql = "SELECT Identification, AnomalyTime FROM anomaly_log WHERE 1=1"
        params = []
        for field, value in filters.items():
            if value and field != "DataAcqEquipCode":
                sql += f" AND {field} = %s"
                params.append(value)
        cursor.execute(sql, params)
        items = cursor.fetchall()
        if not items:  # 该时间点雷达采集数据了，但是不存在异常数据
            # 获取初始化的点云数据
            init_pcd = get_history(init_path=init_region_path)
            return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '该时间点不存在异常数据', 'data': init_pcd}), 200

        # 获取历史数据
        res = get_history(init_path=init_region_path, path=data_path)
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '检索成功', 'data': res}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@pcd_db_op.route('/compare', methods=['POST'])
def compare():
    """
    两个时间点的数据比对
    :return:
    """
    try:
        data = request.json
        root = data.get('root')
        comparison = data.get('comparison')
        filters = {
            'root': {
                "ProCode": root.get('ProCode', None),
                "TunCode": root.get('TunCode', None),
                "WorkSurCode": root.get('WorkSurCode', None),
                "StruCode": root.get('StruCode', None),
                "ConEquipCode": root.get('ConEquipCode', None),
                "DataAcqEquipCode": root.get('DataAcqEquipCode', None),
                "Year": root.get('Year', 0),
                "Month": root.get('Month', 0),
                "Day": root.get('Day', 0),
                "Hour": root.get('Hour', 0),
                "Minute": root.get('Minute', 0),
                "Second": root.get('Second', 0)
            },
            'comparison': {
                "ProCode": comparison.get('ProCode', None),
                "TunCode": comparison.get('TunCode', None),
                "WorkSurCode": comparison.get('WorkSurCode', None),
                "StruCode": comparison.get('StruCode', None),
                "ConEquipCode": comparison.get('ConEquipCode', None),
                "DataAcqEquipCode": comparison.get('DataAcqEquipCode', None),
                "Year": comparison.get('Year', 0),
                "Month": comparison.get('Month', 0),
                "Day": comparison.get('Day', 0),
                "Hour": comparison.get('Hour', 0),
                "Minute": comparison.get('Minute', 0),
                "Second": comparison.get('Second', 0)
            }
        }
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200

    try:
        start1 = time.time()
        root, comparison = filters.get('root'), filters.get('comparison')
        # 校验必填字段
        if not all([root.get('ProCode'), root.get('TunCode'), root.get('WorkSurCode'), root.get('StruCode'),
                    root.get('ConEquipCode'), root.get('DataAcqEquipCode'), str(root.get('Year')),
                    str(root.get('Month')), str(root.get('Day')), str(root.get('Hour')), str(root.get('Minute')),
                    str(root.get('Second')), comparison.get('ProCode'), comparison.get('TunCode'),
                    comparison.get('WorkSurCode'), comparison.get('StruCode'), comparison.get('ConEquipCode'),
                    comparison.get('DataAcqEquipCode'), str(comparison.get('Year')), str(comparison.get('Month')),
                    comparison.get('Day'), str(comparison.get('Hour')), str(comparison.get('Minute')),
                    str(comparison.get('Second'))]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
        # TODO: 判断是否是三天内的数据
        if not data_is_overdue(root) or not data_is_overdue(comparison):
            return jsonify({'code': PCDHttpStatus.DATA_OVERDUE.value, 'msg': '只展示三天内的数据', 'data': {}}), 200

        # TODO: 对比数据（日志信息、点云数据）
        # 1.拿到两个时间点和初始化的点云数据所在文件目录
        root_path, comparison_path = get_path_by_time(root), get_path_by_time(comparison)
        init_path = os.path.join('data', str(root.get('DataAcqEquipCode')), 'data', 'init', 'regions')
        if not os.path.exists(init_path) or root_path is None or comparison_path is None:
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': '不存在初始化数据', 'data': {}}), 200

        start2 = time.time()
        # 2.拿到两个时间点和初始化的点云数据文件路径字典
        root_dict, comparison_dict, init_dict = get_pcd_list(root_path), get_pcd_list(comparison_path), get_pcd_list(
            init_path)
        print("获取点云数据文件路径耗时：", time.time() - start2)

        start3 = time.time()
        # 3.拿到两个时间点的日志信息
        root_log = DBUtils.get_log_by_columns(root)
        comparison_log = DBUtils.get_log_by_columns(comparison)
        if root_log.get('code') != 101 or comparison_log.get('code') != 101:
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': '不存在数据', 'data': {}}), 200
        root_desc, comparison_desc = root_log.get('data').get('desc'), comparison_log.get('data').get('desc')
        root_bas_dict, comparison_bas_dict = {}, {}
        for e in root_desc:
            root_bas_dict[e.get('Region')] = e.get('Bas')
        for e in comparison_desc:
            comparison_bas_dict[e.get('Region')] = e.get('Bas')
        print("获取日志信息耗时：", time.time() - start3)

        start4 = time.time()
        # 4.对比日志信息，将bas相差较大的区域和偏差信息记录下来
        compare_bas_res, compare_bas_log = compare_log_information(root_bas_dict, comparison_bas_dict, comparison_dict)
        print("对比日志信息耗时：", time.time() - start4)

        start5 = time.time()
        # 5.融合点云数据形成最终对比结果
        if not compare_bas_res:
            for k, v in root_dict.items():
                init_dict[k] = v
        else:
            # 需要先融合root和init，再将融合结果与comparison融合
            for k, v in root_dict.items():
                init_dict[k] = v
            for k, v in compare_bas_res.items():
                init_dict[k] = v
        print("融合点云耗时：", time.time() - start5)

        start6 = time.time()
        coordinate_list, color_list = get_xyz_rgb_list(init_dict, compare_bas_res)
        print("组合返回结果耗时：", time.time() - start6)

        # res_df = pd.concat(df_list, ignore_index=True)
        # pcd = o3d.geometry.PointCloud()
        # pcd.points = o3d.utility.Vector3dVector(res_df[['X', 'Y', 'Z']].values)
        # pcd.colors = o3d.utility.Vector3dVector(res_df[['R', 'G', 'B']].values / 255.0)
        # o3d.visualization.draw_geometries([pcd])

        print("整体耗时：", time.time() - start1)
        # 7.返回结果
        return jsonify({'xyz': str(coordinate_list), 'rgb': str(color_list), 'msg': compare_bas_log,
                        'code': BaseHttpStatus.OK.value}), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '对比失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/selectPCDByColumn', methods=['POST'])
def select_pcd_by_column():
    """
    获取历史数据
    TODO：
        1. 通过k-v键值对检索到指定的历史数据（完整数据）
        2. 以字符串的形式返回点云数据
    """
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        if len(item) == 1 and item[0] == 'PCDLogUID':  # 若 item 为 PCDLogUID，则筛选出唯一记录的 InitPCDPath 值并读取路径中的数据进行组装
            res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
            if res.get('code') != 101:
                return jsonify(res), 200

            items = res.get('data').get('items')
            if len(items) != 1:
                return jsonify(
                    {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {}}), 200

            init_pcd_path = items[0].get('InitPCDPath')
            # TODO:读取文件中的数据
            get_pcd_res = FileUtils.read_pcd_csv2str(init_pcd_path)
            return jsonify(get_pcd_res), 200
        else:
            res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/selectRegionPCDByColumn', methods=['POST'])
def select_region_pcd_by_column():
    """
    获取初始化区域数据
    TODO:
        1. 通过k-v键值对检索到指定的历史数据（完整数据），提取历史记录相关信息
        2. 通过项目/隧道/设备等编号在云服务器上找到指定的初始化区域数据
        3. 以字典形式返回点云数据
    """
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        if len(item) != 1 or item[0] != 'PCDLogUID':
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': {}}), 200

        res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
        items = res.get('data').get('items')
        if len(items) != 1:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': {}}), 200
        # TODO: 组合数据
        init_region_dir = items[0].get('InitRegionPath')
        region_res = FileUtils.read_region_dir_csv(init_region_dir)
        return jsonify(region_res), 200
        # return jsonify({
        #     'code': BaseHttpStatus.OK.value,
        #     'msg': '查找成功',
        #     'data':
        #         {
        #             '1': '[1, 1, 1, 255, 255, 0]',
        #             '2': '[1, 1, 1, 255, 255, 0]',
        #         }
        # }), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/selectAnomalyPCDByColumn', methods=['POST'])
def select_anomaly_pcd_by_column():
    """
    获取沉降分析数据
    TODO:
        1. 通过k-v键值对检索到指定的历史数据（完整数据），提取历史记录相关信息
        2. 通过项目/隧道/设备等编号在云服务器上找到指定的初始化区域数据
        3. 读取异常区域数据
        4. 组合初始化区域数据和异常区域数据
        5. 以字典形式返回点云数据
    """
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        if len(item) != 1 or item[0] != 'PCDLogUID':
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': ''}), 200

        res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
        items = res.get('data').get('items')
        if len(items) != 1:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': ''}), 200

        # 组合数据
        init_region_path = items[0].get('InitRegionPath', None)
        anomaly_region_path = items[0].get('AnomalyRegionPath', None)
        anomaly_describe_path = items[0].get('AnomalyDescribePath', None)
        if not init_region_path:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': ''}), 200

        init_region_path = str(init_region_path).replace('https://sat.jovysoft.net:8066',
                                                         'D:/tunnelProject/adminProject/data')
        anomaly_region_path = str(anomaly_region_path).replace('https://sat.jovysoft.net:8066',
                                                               'D:/tunnelProject/adminProject/data')
        anomaly_describe_path = str(anomaly_describe_path).replace('https://sat.jovysoft.net:8066',
                                                                   'D:/tunnelProject/adminProject/data')
        init_region_dict = {}
        with os.scandir(init_region_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.csv'):
                    init_region_path = entry.path
                    region_index = entry.name.split('.')[0]
                    region_df = pd.read_csv(init_region_path)
                    region_list = []
                    temp_dict = {
                        'data': '',
                        'describe': []
                    }
                    for row in region_df.itertuples(index=False):
                        # region_list.extend([float(row.X), float(row.Y), float(row.Z), float(row.Reflectivity)])
                        region_list.extend([float(row.X), float(row.Y), float(row.Z), 102])
                    temp_dict['data'] = region_list
                    temp_dict['describe'] = None
                    init_region_dict[region_index] = temp_dict

        if anomaly_region_path and anomaly_describe_path:
            anomaly_region_len = len(os.listdir(anomaly_region_path))
            anomaly_describe_len = len(os.listdir(anomaly_describe_path))
            if anomaly_region_len != anomaly_describe_len:
                return jsonify(
                    {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': '异常数据与异常描述不符'}), 200

            anomaly_dict = {}
            # 构造预警详情信息
            with os.scandir(anomaly_describe_path) as entries:
                reflectivity = 102
                for entry in entries:
                    temp_dict = {
                        'data': None,
                        'describe': None
                    }
                    if entry.is_file() and entry.name.endswith('.txt'):
                        anomaly_describe_path = entry.path
                        region_index = entry.name.split('.')[0]
                        with open(anomaly_describe_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # 获取对应的dataframe数据路径
                        anomaly_region_son_path = f'{anomaly_region_path}/{region_index}.csv'
                        anomaly_region_data = pd.read_csv(anomaly_region_son_path)

                        # 读取异常描述数据
                        list_describe = ast.literal_eval(content)
                        temp_dict['describe'] = list_describe

                        # 根据 describe 信息设置 reflectivity
                        if list_describe[-1] == 1:
                            reflectivity = 255
                        elif list_describe[-1] == 2:
                            reflectivity = 199
                        elif list_describe[-1] == 3:
                            reflectivity = 160
                        anomaly_region_data.loc[:, 'Reflectivity'] = reflectivity
                        anomaly_dict[region_index] = temp_dict

                # 构造预警数据信息
                with os.scandir(anomaly_region_path) as entries:
                    for entry in entries:
                        if entry.is_file() and entry.name.endswith('.csv'):
                            anomaly_region_path = entry.path
                            region_index = entry.name.split('.')[0]
                            if region_index in anomaly_dict.keys():
                                region_df = pd.read_csv(anomaly_region_path)
                                region_list = []
                                for row in region_df.itertuples(index=False):
                                    region_list.extend([float(row.X), float(row.Y), float(row.Z), float(row.Reflectivity)])
                                anomaly_dict[region_index]['data'] = region_list
        else:  # 用于测试接口
            region_index_list = list(init_region_dict.keys())
            first_list = random.sample(region_index_list, 100)
            second_list = random.sample(region_index_list, 100)
            third_list = random.sample(region_index_list, 100)
            for k, v in init_region_dict.items():
                region = v['data']  # list
                if k in first_list:
                    v['describe'] = [[10.0, 5.0, 6.0], 0.6, 1]
                    for i in range(3, len(region), 4):
                        region[i] = 255
                elif k in second_list:
                    v['describe'] = [[50.0, 7.0, 6.0], 1.0, 2]
                    for i in range(3, len(region), 4):
                        region[i] = 199
                elif k in third_list:
                    v['describe'] = [[60.0, -5.0, 6.0], 1.5, 3]
                    for i in range(3, len(region), 4):
                        region[i] = 160
                else:
                    v['describe'] = None
                    for i in range(3, len(region), 4):
                        region[i] = 102
                v['data'] = region
            # for f in first_list:
            #     init_region_dict[f]['describe'] = [[10.0, 5.0, 6.0], 0.6, 1]
            # for s in second_list:
            #     init_region_dict[s]['describe'] = [[50.0, 7.0, 6.0], 1.0, 2]
            # for t in third_list:
            #     init_region_dict[t]['describe'] = [[60.0, -5.0, 6.0], 1.5, 3]

        return jsonify({
            'code': BaseHttpStatus.OK.value,
            'msg': '查找成功',
            'data': init_region_dict
        }), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '分析失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/selectBackBreakPCDByColumn', methods=['POST'])
def select_back_break_pcd_column():
    """
    获取超欠挖分析数据
    TODO:
        1. 通过k-v键值对检索到指定的历史数据（完整数据），提取历史记录相关信息
        2. 通过项目/隧道/设备等编号在云服务器上找到指定的初始化区域数据
        3. 用工程方程模拟标准隧道数据
        4. 组合初始化区域数据和异常数据
        5. 利用组合数据和标准隧道数据进行超欠挖计算
        6. 以字典形式返回点云数据
    """
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        if len(item) != 1 or item[0] != 'PCDLogUID':
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {}}), 200

        res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
        items = res.get('data').get('items')
        if len(items) != 1:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {}}), 200

        # TODO：用方程模拟数据

        init_region_path = items[0].get('InitRegionPath')
        anomaly_region_path = items[0].get('AnomalyRegionPath')
        # TODO：组合数据
        # 超欠挖计算
        return jsonify({
            'code': BaseHttpStatus.OK.value,
            'msg': '计算成功',
            'data':
                {
                    '1': '[1, 1, 1, 255, 255, 0]',
                    '2': '[1, 1, 1, 255, 255, 0]',
                }
        }), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {'exception': str(e)}}), 200


@pcd_db_op.route('/selectClearanceCalculationByColumn', methods=['POST'])
def select_clearance_calculation_by_column():
    """
    获取净空计算数据
    TODO：
        1. 通过k-v键值对检索到指定的历史数据（完整数据），提取历史记录相关信息
        2. 通过项目/隧道/设备等编号在云服务器上找到指定的初始化区域数据
        3. 读取异常区域数据，与初始化区域数据组合成完整预处理数据
        4. 将完整预处理数据根据指定间距分割成大小相同的断面
        5. 对每个断面进行断面分析
        6. 以字典形式返回断面分析结果

    """
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        size = data.get('Size', 5)  # 分割断面大小，默认为10米
        if len(item) != 1 or item[0] != 'PCDLogUID':
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {}}), 200

        res = DBUtils.search_by_some_item('pcd_log', item, value, join=False, data=data)
        items = res.get('data').get('items')
        if len(items) != 1:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {}}), 200

        """ 净空计算 """
        # 判断是否有净空计算结果，如果有则直接获取数据并返回
        calculation_uuid = items[0].get('CalculationUUID', None)
        if calculation_uuid:
            res = DBUtils.get_calculation_result(calculation_uuid)
            if res.get('code') != 101:
                return jsonify(
                    {'code': BaseHttpStatus.ERROR.value, 'msg': '计算失败', 'data': {}}), 200
            return jsonify(res), 200

        # 需要计算
        try:
            pre_path = items[0].get('AnomalyPrePath', None)
            pro_code = items[0].get('ProCode', None)
            tun_code = items[0].get('TunCode', None)
            control_code = items[0].get('ConEquipCode', None)
            log_uuid = items[0].get('PCDLogUID', None)
        except Exception as e:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {'获取记录信息时发生错误': str(e)}}), 200

        if not all([pro_code, tun_code, control_code, log_uuid]):
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': '缺少必要的字段'}), 200

        if not pre_path:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': ''}), 200

        # 断面净空计算
        pcd_path = pre_path.replace('https://sat.jovysoft.net:8066', 'D:/tunnelProject/adminProject/data')
        pcd_df = pd.read_csv(pcd_path)
        # 构建服务器本地存储路径
        save_path = f"{SAVE_DIR}/data/project_{pro_code}/tunnel_{tun_code}/control_{control_code}/uuid_{log_uuid}/calculation/region"
        os.makedirs(save_path, exist_ok=True)
        res = run(pcd_df, save_path, size)
        if res is None:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '计算失败', 'data': {}}), 200

        # 在 space_calculation 表中记录
        space_calculation_res = DBUtils.update_space_calculation_log(log_uuid, save_path, size, res['intact_surface_area'], res['intact_volume'])
        if space_calculation_res.get('code') != 101:
            return jsonify(space_calculation_res), 200
        return jsonify({
            'code': BaseHttpStatus.OK.value,
            'msg': '计算成功',
            'data':
                res
        }), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '计算失败', 'data': {'exception': str(e)}}), 200
