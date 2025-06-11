"""
@Author: zhang_zhiyi
@Date: 2025/4/15_15:10
@FileName:history.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 历史记录
"""
import base64
import os
import pickle
import random
from datetime import datetime

from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.logHttpStatus import LogHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils
from utils.util_statistics import StUtils

history_db = Blueprint('history_db', __name__)

ANOMALY_ROOT_DIR = r'D:\tunnelProject\adminProject\data'


@history_db.route('/selectHistory', methods=['POST'])
def log_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'pcd_log', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/searchLogByColumn', methods=['POST'])
def log_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item('pcd_log', data.get('Item'), data.get('Value'), data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/viewPCD', methods=['POST'])
def view_pcd():
    try:
        data = request.json
        # TODO: 显示点云数据
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/sectionFilter', methods=['POST'])
def section_filter():
    try:
        data = request.json
        column = data.get('Column', None)
        if column is None:
            return jsonify(
                {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
        res = StUtils.section_filter('pcd_log', column, data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/uploadInitFile', methods=['POST'])
def upload_init_file():
    result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '添加失败',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '添加成功',
            'data': ''
        },
        2: {
            'code': LogHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个日志',
            'data': ''
        }
    }
    try:
        data = request.json
        region = data.get('Region')
        intact_data = data.get('IntactData')
        project_code = data.get('ProCode')
        tunnel_code = data.get('TunCode')
        control_code = data.get('ConEquipCode')
        log_uuid = data.get('LogUUID')
        # avia_code = data.get('TunCode', None)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '上传失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([region, intact_data, project_code, tunnel_code, control_code, log_uuid]):
        return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

    con = None
    cursor = None
    try:
        dub = DBUtils()
        con = dub.connection()
        cursor = con.cursor()
        con.autocommit(False)
        """ 写入文件 """
        # 构建保存路径
        region_save_dir = f"{ANOMALY_ROOT_DIR}/data/project_{project_code}/tunnel_{tunnel_code}/control_{control_code}/uuid_{log_uuid}/init/region"
        intact_save_dir = f"{ANOMALY_ROOT_DIR}/data/project_{project_code}/tunnel_{tunnel_code}/control_{control_code}/uuid_{log_uuid}/init/intact"
        os.makedirs(region_save_dir, exist_ok=True)
        os.makedirs(intact_save_dir, exist_ok=True)

        # 解包 intact_data
        decode = base64.b64decode(intact_data)
        intact_data_df = pickle.loads(decode)
        intact_data_df.to_csv(f'{intact_save_dir}/{log_uuid}.csv', index=False, encoding='utf-8')

        # 解包区域数据并写入
        # region_list = []
        for k, v in region.items():
            # region_save_path = f"{region_save_dir}/{k}.txt"
            region_save_path = f"{region_save_dir}/{k}.csv"
            index_data = base64.b64decode(v)
            index_data_df = pickle.loads(index_data)
            index_data_df.to_csv(region_save_path, index=False, encoding='utf-8')
            # for row in index_data_df.itertuples(index=False):
            # region_list.extend([row.X, row.Y, row.Z, row.Reflectivity])
            # region_list.extend([row.X, row.Y, row.Z, float(random.randint(0, 255))])

            # with open(region_save_path, 'w', encoding='utf-8') as f:
            #     f.write(str(region_list))

        """ 记录数据库 """
        log_insert_sql = """
            INSERT INTO pcd_init (ConEquipCode, InitPCDPath, InitRegionPath) VALUES (%s, %s, %s)
        """
        intact_save_dir_db = f'{intact_save_dir}/{log_uuid}.csv'.replace(ANOMALY_ROOT_DIR,
                                                                         'https://sat.jovysoft.net:8066')
        region_save_dir_db = region_save_dir.replace(ANOMALY_ROOT_DIR, 'https://sat.jovysoft.net:8066')
        rows = cursor.execute(log_insert_sql, (control_code, intact_save_dir_db, region_save_dir_db))
        res = DBUtils.kv(rows, result_dict)
        if res.get('code') != 101:
            return res

        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '插入成功', 'data': {}}), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '插入失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@history_db.route('/uploadAnomalyFile', methods=['POST'])
def upload_anomaly_file():
    try:
        data = request.json
        pre_data = data.get('PreData')
        region = data.get('Region')
        describe = data.get('Describe')
        project_code = data.get('ProCode')
        tunnel_code = data.get('TunCode')
        control_code = data.get('ConEquipCode')
        log_uuid = data.get('LogUUID')
        # avia_code = data.get('TunCode', None)
        # 校验必填字段
        if not all([pre_data, region, describe, project_code, tunnel_code, control_code, log_uuid]):
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

        pre_data_save_dir = f"{ANOMALY_ROOT_DIR}/data/project_{project_code}/tunnel_{tunnel_code}/control_{control_code}/uuid_{log_uuid}/anomaly/pre"
        region_save_dir = f"{ANOMALY_ROOT_DIR}/data/project_{project_code}/tunnel_{tunnel_code}/control_{control_code}/uuid_{log_uuid}/anomaly/region"
        describe_save_dir = f"{ANOMALY_ROOT_DIR}/data/project_{project_code}/tunnel_{tunnel_code}/control_{control_code}/uuid_{log_uuid}/anomaly/describe"
        os.makedirs(region_save_dir, exist_ok=True)
        os.makedirs(describe_save_dir, exist_ok=True)
        os.makedirs(pre_data_save_dir, exist_ok=True)

        # 写入预处理后的数据
        pre_data_decode = base64.b64decode(pre_data)
        pre_data_df = pickle.loads(pre_data_decode)
        pre_data_df.to_csv(f'{pre_data_save_dir}/{log_uuid}.csv', index=False, encoding='utf-8')

        for r, d in zip(region.items(), describe.items()):
            region_index, anomaly_data = r
            _, anomaly_describe = d
            decode = base64.b64decode(anomaly_data)
            anomaly_data_df = pickle.loads(decode)

            region_save_path = f"{region_save_dir}/{region_index}.csv"
            describe_save_path = f"{describe_save_dir}/{region_index}.txt"

            anomaly_data_df.to_csv(region_save_path, index=False, encoding='utf-8')
            with open(describe_save_path, 'w', encoding='utf-8') as f:
                f.write(str(anomaly_describe))

        return jsonify(
            {
                'code': BaseHttpStatus.OK.value,
                'msg': '写入成功',
                'data': {
                    'AnomalyRegionPath': region_save_dir,
                    'AnomalyDescribePath': describe_save_dir,
                    'AnomalyPrePath': f'{pre_data_save_dir}/{log_uuid}.csv'
                }
            }
        ), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '写入失败', 'data': {'exception': str(e)}}), 200


# @history_db.route('/uploadPreFile', methods=['POST'])
# def upload_pre_file():
#     try:
#         data = request.json
#         pre_data = data.get('PreData')
#     except Exception as e:
#         return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '写入失败', 'data': {'exception': str(e)}}), 200
#
#     # 校验必填字段
#     if not all([pre_data]):
#         return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}


@history_db.route('/addHistory', methods=['POST'])
def add_history():
    result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '添加失败',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '添加成功',
            'data': ''
        },
        2: {
            'code': LogHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个日志',
            'data': ''
        }
    }
    try:
        data = request.json
        pcd_log_uid = data.get('PCDLogUID')
        pro_code = data.get('ProCode')
        tun_code = data.get('TunCode')
        work_sur_code = data.get('WorkSurCode')
        stru_code = data.get('StruCode')
        mileage = data.get('Mileage')
        con_acq_code = data.get('ConEquipCode')
        data_acq_code = data.get('DataAcqEquipCode')
        anomaly_time = data.get('AnomalyTime')
        company_code = data.get('CompanyCode')

        anomaly_region_path = data.get('AnomalyRegionPath')
        anomaly_describe_path = data.get('AnomalyDescribePath')
        anomaly_pre_path = data.get('AnomalyPrePath')
        update_init_count = data.get('UpdateInitCount', 20)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200

    if not all([pcd_log_uid, pro_code, tun_code, work_sur_code, stru_code, mileage, con_acq_code, data_acq_code,
                anomaly_time, company_code, anomaly_region_path, anomaly_describe_path, anomaly_pre_path, str(update_init_count)]):
        return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

    con = None
    cursor = None
    try:
        dub = DBUtils()
        con = dub.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        con.autocommit(False)

        # 验证各个Code
        checks = [
            ('tunnel', 'TunCode', tun_code, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道不存在"),
            ('project', 'ProCode', pro_code, ProjectHttpStatus.NO_FIND_CODE.value, "该项目不存在"),
            ('structure', 'StruCode', stru_code, ProjectHttpStatus.NO_FIND_CODE.value, "该结构物不存在"),
            ('work_surface', 'WorkSurCode', work_sur_code, ProjectHttpStatus.NO_FIND_CODE.value, "该工作面不存在"),
            ('eq_control', 'ConEquipCode', con_acq_code, ProjectHttpStatus.NO_FIND_CODE.value, "该中控设备不存在"),
            ('eq_data', 'DataAcqEquipCode', data_acq_code, ProjectHttpStatus.NO_FIND_CODE.value, "该数据采集器不存在"),
            ('company', 'Code', company_code, ProjectHttpStatus.NO_FIND_CODE.value, "所属机构不存在")
        ]
        for table, column, code, error_code, error_msg in checks:
            res = DBUtils.check_existence(cursor, table, column, code, error_code, error_msg)
            if res:
                return res

        sql = """
            INSERT INTO
                pcd_log
            (PCDLogUID, ProCode, TunCode, WorkSurCode, StruCode, Mileage, ConEquipCode, DataAcqEquipCode, AnomalyTime, Year, Month, Day, Hour, Minute, Second, CompanyCode, InitPCDPath, InitRegionPath, AnomalyRegionPath, AnomalyDescribePath, AnomalyPrePath, UpdateInitCount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 日期
        now = datetime.strptime(anomaly_time, '%Y-%m-%d %H:%M:%S')
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second

        """ 通过设备编号在 pcd_init 表中查询对应的 InitPCDPath 和 InitRegionPath """
        select_init_sql = """
            SELECT InitPCDPath, InitRegionPath FROM pcd_log WHERE ConEquipCode = %s
        """
        cursor.execute(select_init_sql, con_acq_code)
        select_res = cursor.fetchone()

        init_pcd_path = select_res.get('InitPCDPath', None)
        init_region_path = select_res.get('InitRegionPath', None)
        if not init_region_path or not init_region_path:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '未找到对应的初始点云或区域路径', 'data': {}}), 200

        rows = cursor.execute(sql, (
            pcd_log_uid, pro_code, tun_code, work_sur_code, stru_code, mileage, con_acq_code, data_acq_code,
            anomaly_time, year, month, day, hour, minute, second, company_code, init_pcd_path, init_region_path,
            anomaly_region_path, anomaly_describe_path, anomaly_pre_path, update_init_count))

        res = DBUtils.kv(rows, result_dict)
        if res.get('code') != 101:
            return res

        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '插入成功', 'data': {}}), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '插入失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)
