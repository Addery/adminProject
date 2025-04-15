"""
@Author: zhang_zhiyi
@Date: 2024/10/24_15:32
@FileName:pcd_db_op.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云数据操作路由 本地文件保存点云数据，数据库保存日志信息
"""
import os
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
from utils.util_pcd import get_path, get_history, get_path_by_time, get_pcd_list, compare_log_information, \
    get_xyz_rgb_list, data_is_overdue

pcd_db_op = Blueprint('pcd_db_op', __name__)


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
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200


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
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200
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
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {'exception': str(e)}}), 200

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
        return jsonify({'xyz': str(coordinate_list), 'rgb': str(color_list), 'msg': compare_bas_log, 'code': BaseHttpStatus.OK.value}), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '对比失败', 'data': {'exception': str(e)}}), 200
