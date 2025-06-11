"""
@Author: zhang_zhiyi
@Date: 2024/10/21_15:23
@FileName:anomaly.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import time
from collections import Counter

from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor

# from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.logHttpStatus import LogHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils
from utils.util_statistics import StUtils

anomaly_db = Blueprint('anomaly_db', __name__)


@anomaly_db.route('/addAnomaly', methods=['POST'])
def anomaly_add():
    try:
        data = request.json
        res = DBUtils.anomaly_log_insert(data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/deleteAnomaly', methods=['POST'])
def anomaly_delete():
    result_dict = {
        0: {
            'code': LogHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的日志不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': LogHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多日志信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        identification = data.get('Identification')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([identification]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        sql = """
              DELETE FROM anomaly_log WHERE Identification = %s
              """
        rows = cursor.execute(sql, identification)
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@anomaly_db.route('/selectAnomalyLog', methods=['POST'])
def log_select():
    try:
        data = request.json
        res = DBUtils.paging_display_condition_on_sql(data, 'anomaly_log', 1, 10, join=True)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/selectAnomalyLogDesc', methods=['POST'])
def desc_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'anomaly_log_desc', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/selectAnomalyLogImg', methods=['POST'])
def img_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'anomaly_log_img', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/searchLogByColumn', methods=['POST'])
def log_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item('anomaly_log', data.get('Item'), data.get('Value'), join=True, data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/searchDescByColumn', methods=['POST'])
def desc_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item('anomaly_log_desc', data.get('Item'), data.get('Value'), data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/searchImgByColumn', methods=['POST'])
def img_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item('anomaly_log_img', data.get('Item'), data.get('Value'), data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/sectionFilter', methods=['POST'])
def section_filter():
    try:
        data = request.json
        column = data.get('Column', None)
        if column is None:
            return jsonify(
                {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
        res = StUtils.section_filter('anomaly_log', column, data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@anomaly_db.route('/modifyLogStatus', methods=['POST'])
def modify_log_status():
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '更新内容和原先保持一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '更新成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '更新了多个预警记录',
            'data': ''
        }
    }
    try:
        data = request.json
        identification = data.get('Identification')
        operation = data.get('Operation')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '失败', 'data': {'exception': str(e)}}), 200

    if not all([operation, identification]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的参数', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 验证 预警记录identification 是否存在
        identification_sql = "SELECT * From anomaly_log WHERE Identification = {}".format(f"'{identification}'")
        res = DBUtils.project_is_exist(cursor, identification_sql, LogHttpStatus.NO_FIND_CODE.value, "该预警记录不存在")
        if res:
            return jsonify(res), 200

        update_sql = "UPDATE anomaly_log SET Sign = %s WHERE Identification = %s"
        rows = cursor.execute(update_sql, (int(operation), identification))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@anomaly_db.route('/statisticsStatus', methods=['POST'])
def log_status():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}

    if not all([item, value]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的参数', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()

        sql = f"SELECT Sign FROM anomaly_log WHERE {item} = %s"
        cursor.execute(sql, value)
        res = cursor.fetchall()
        counter = Counter(item['Sign'] for item in res)
        counter = dict(counter)
        print('counter: ', counter)
        print('counter class', type(counter))
        print(counter.get(1, 0))
        print(counter.get(2, 0))
        if not counter:
            return {
                'code': BaseHttpStatus.OK.value,
                'msg': '统计成功',
                'data':
                    {
                        '1': 0,
                        '2': 0
                    }
            }
        return {
            'code': BaseHttpStatus.OK.value,
            'msg': '统计成功',
            'data': {
                '1': counter.get(1, 0),
                '2': counter.get(2, 0)
            }
        }
    except Exception as e:
        if con:
            con.rollback()
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


