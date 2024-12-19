"""
@Author: zhang_zhiyi
@Date: 2024/10/18_15:10
@FileName:data.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
from flask import jsonify, request, Blueprint
# from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.equipHttpStatus import EquipHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils

data_acq_db = Blueprint('data_acq_db', __name__)


@data_acq_db.route('/addDataAcq', methods=['POST'])
def data_acq_add():
    """
    添加数据采集器信息
    :return:
    """
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
            'code': EquipHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个数据采集器',
            'data': ''
        }
    }
    try:
        data = request.json
        acq_code = data.get('DataAcqEquipCode')
        acq_name = data.get('DataAcqEquipName')
        acq_ip = data.get('DataAcqEquipIP')
        interval = data.get('DataAcqEquipInterval')
        distance = data.get('Distance')
        status = data.get('DataAcaEquipStatus', 0)
        equ_code = data.get('ConEquipCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([acq_code, acq_name, acq_ip, interval, distance, equ_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证TunCode是否存在
        sql = "SELECT * From eq_control WHERE ConEquipCode = {}".format(f"'{equ_code}'")
        res = DBUtils.project_is_exist(cursor, sql, EquipHttpStatus.NO_FIND_CODE.value, "该中控设备不存在")
        if res:
            return jsonify(res), 200

        # 校验待添加的设备是否已经存在
        select_sql = "SELECT ConEquipCode From eq_data WHERE DataAcqEquipCode = {}".format(f"'{acq_code}'")
        res = DBUtils.is_exist(cursor, select_sql, equ_code, EquipHttpStatus.NO_FIND_CODE.value, "该数据采集器已经存在")
        if res:
            return jsonify(res), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO eq_data (DataAcqEquipCode, DataAcqEquipName, DataAcqEquipIP, DataAcqEquipInterval, Distance, DataAcaEquipStatus, ConEquipCode) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql, (acq_code, acq_name, acq_ip, interval, distance, status, equ_code))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '添加失败', 'data': {str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@data_acq_db.route('/deleteDataAcq', methods=['POST'])
def data_acq_delete():
    """
    删除数据采集器信息
    :return:
    """
    result_dict = {
        0: {
            'code': ProjectHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的数据采集器不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': EquipHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多数据采集器信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        equ_code = data.get('ConEquipCode')
        acq_code = data.get('DataAcqEquipCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([equ_code, acq_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
              DELETE FROM eq_data WHERE ConEquipCode = %s and DataAcqEquipCode = %s
              """
        rows = cursor.execute(sql, (equ_code, acq_code))
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


@data_acq_db.route('/updateDataAcq', methods=['POST'])
def data_acq_update():
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '数据采集器信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': EquipHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多数据采集器信息被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_equ_code = data.get("OldConEquipCode")
        old_acq_code = data.get("OldDataAcqEquipCode")
        acq_code = data.get("DataAcqEquipCode")
        acq_name = data.get("DataAcqEquipName")
        acq_ip = data.get("DataAcqEquipIP")
        interval = data.get("DataAcqEquipInterval")
        distance = data.get("Distance")
        equ_code = data.get("ConEquipCode")
        status = data.get('DataAcaEquipStatus')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([old_equ_code, old_acq_code, acq_code, status, acq_name, acq_ip, interval, distance, equ_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待修改的数据采集器信息是否已经存在
        select_old_sql = "SELECT ConEquipCode From eq_data WHERE DataAcqEquipCode={} AND ConEquipCode={}".format(f"'{old_acq_code}'", f"'{old_equ_code}'")
        old_is_exist = DBUtils.is_exist(cursor, select_old_sql, old_equ_code, EquipHttpStatus.EXIST_CODE.value,
                                        "数据采集器信息存在")
        if not old_is_exist:
            return jsonify(
                {'code': ProjectHttpStatus.NO_FIND_CODE.value, 'msg': '数据采集器信息不存在', 'data': {}}), 200

        # 校验修改后的数据采集器信息是否被占用
        select_sql = "SELECT ConEquipCode From eq_data WHERE DataAcqEquipCode={}".format(f"'{acq_code}'")
        is_exist = DBUtils.is_exist(cursor, select_sql, equ_code, EquipHttpStatus.EXIST_CODE.value,
                                    "数据采集器编号已经被使用")
        if is_exist and old_acq_code != acq_code:
            return jsonify(is_exist), 200

        # 验证StruCode是否存在
        code_sql = "SELECT * From eq_control WHERE ConEquipCode = {}".format(f"'{equ_code}'")
        res = DBUtils.project_is_exist(cursor, code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该中控设备不存在")
        if res:
            return jsonify(res), 200

        sql = """
                   UPDATE 
                       eq_data 
                   SET 
                       DataAcqEquipCode=%s, DataAcqEquipName=%s, DataAcqEquipIP=%s, DataAcqEquipInterval=%s, Distance=%s, ConEquipCode=%s, DataAcaEquipStatus=%s
                   Where 
                       ConEquipCode=%s AND DataAcqEquipCode=%s;
                   """
        rows = cursor.execute(sql, (
            acq_code, acq_name, acq_ip, interval, distance, equ_code, status, old_equ_code, old_acq_code))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '修改失败', 'data': {str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@data_acq_db.route('/selectDataAcq', methods=['POST'])
def data_acq_select():
    """
       获取数据采集器信息，分页展示
       :return:
       """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'eq_data', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@data_acq_db.route('/searchInfoByColumn', methods=['POST'])
def data_acq_info_search_by_column():
    """
    根据数据采集器表中的某个字段搜索对应的数据采集器信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'eq_data', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200
