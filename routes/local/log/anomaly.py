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

from flask import jsonify, request, Blueprint
# from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.logHttpStatus import LogHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils

anomaly_db = Blueprint('anomaly_db', __name__)


@anomaly_db.route('/addAnomaly', methods=['POST'])
def anomaly_add():
    try:
        data = request.json
        res = DBUtils.log_insert_db(data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '失败', 'data': {str(e)}}), 200


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
        desc_code = data.get('DescCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([desc_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
              DELETE FROM anomaly_log_desc WHERE DescCode = %s
              """
        rows = cursor.execute(sql, desc_code)
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '删除失败', 'data': {str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@anomaly_db.route('/selectAnomalyLog', methods=['POST'])
def log_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'anomaly_log', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@anomaly_db.route('/selectAnomalyLogDesc', methods=['POST'])
def desc_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'anomaly_log_desc', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@anomaly_db.route('/searchLogByColumn', methods=['POST'])
def log_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'anomaly_log', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@anomaly_db.route('/searchDescByColumn', methods=['POST'])
def desc_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'anomaly_log_desc', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200
