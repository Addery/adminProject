"""
@Author: zhang_zhiyi
@Date: 2024/10/18_11:04
@FileName:console.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库中控设备表相关路由
"""

from flask import jsonify, request, Blueprint
# from pymysql.cursors import DictCursor

from outer.routes.local.status_code.baseHttpStatus import BaseHttpStatus
from outer.routes.local.status_code.equipHttpStatus import EquipHttpStatus
from outer.routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from outer.utils.util_database import DBUtils

console_db = Blueprint('console_db', __name__)


@console_db.route('/addConsole', methods=['POST'])
def console_add():
    """
    添加设备信息
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
            'msg': '添加了多个中控设备',
            'data': ''
        }
    }
    try:
        data = request.json
        equ_code = data.get('ConEquipCode')
        equ_name = data.get('ConEquipName')
        equ_ip = data.get('ConEquipIP')
        pro_code = data.get('ProCode')
        tun_code = data.get('TunCode')
        work_sur_code = data.get('WorkSurCode')
        stru_code = data.get('StruCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([equ_code, equ_name, equ_ip, pro_code, tun_code, work_sur_code, stru_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证TunCode是否存在
        sql = "SELECT * From tunnel WHERE TunCode = {}".format(f"'{tun_code}'")
        res = DBUtils.project_is_exist(cursor, sql, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道不存在")
        if res:
            return jsonify(res), 200

        # 验证ProCode是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        res = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该项目不存在")
        if res:
            return jsonify(res), 200

        # 验证StruCode是否存在
        stru_code_sql = "SELECT * From structure WHERE StruCode = {}".format(f"'{stru_code}'")
        res = DBUtils.project_is_exist(cursor, stru_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该结构物不存在")
        if res:
            return jsonify(res), 200

        # 验证WorkSurCode是否存在
        stru_code_sql = "SELECT * From work_surface WHERE WorkSurCode = {}".format(f"'{work_sur_code}'")
        res = DBUtils.project_is_exist(cursor, stru_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该工作面不存在")
        if res:
            return jsonify(res), 200

        # 校验待添加的设备是否已经存在
        select_sql = "SELECT WorkSurCode From eq_control WHERE ConEquipCode = {}".format(f"'{equ_code}'")
        res = DBUtils.is_exist(cursor, select_sql, work_sur_code, EquipHttpStatus.NO_FIND_CODE.value, "该中控设备已经存在")
        if res:
            return jsonify(res), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO eq_control (ConEquipCode, ConEquipName, ConEquipIP, ProCode, TunCode, WorkSurCode, StruCode) VALUES (%s, %s, %s, %s, %s,  %s, %s)
                """
        rows = cursor.execute(insert_sql, (equ_code, equ_name, equ_ip, pro_code, tun_code, work_sur_code, stru_code))
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


@console_db.route('/deleteConsole', methods=['POST'])
def console_delete():
    """
    删除中控设备信息
    :return:
    """
    result_dict = {
        0: {
            'code': ProjectHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的中控设备不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': EquipHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多中控设备信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        equ_code = data.get('ConEquipCode')
        work_surface_code = data.get('WorkSurCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([equ_code, work_surface_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
              DELETE FROM eq_control WHERE ConEquipCode = %s and WorkSurCode = %s
              """
        rows = cursor.execute(sql, (equ_code, work_surface_code))
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


@console_db.route('/updateConsole', methods=['POST'])
def console_update():
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '中控设备信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': EquipHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多中控设备信息被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_equ_code = data.get("OldConEquipCode")
        old_work_surface_code = data.get("OldWorkSurCode")
        equ_code = data.get("ConEquipCode")
        equ_name = data.get("ConEquipName")
        equ_ip = data.get("ConEquipIP")
        pro_code = data.get("ProCode")
        tun_code = data.get("TunCode")
        work_surface_code = data.get("WorkSurCode")
        stru_code = data.get("StruCode")
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([old_equ_code, old_work_surface_code, tun_code, equ_name, equ_code, equ_ip, pro_code, tun_code,
                work_surface_code, stru_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待修改的中控设备信息是否已经存在
        select_old_sql = "SELECT WorkSurCode From eq_control WHERE ConEquipCode={}".format(f"'{old_equ_code}'")
        old_is_exist = DBUtils.is_exist(cursor, select_old_sql, old_work_surface_code, EquipHttpStatus.EXIST_CODE.value,
                                        "中控设备信息存在")
        if not old_is_exist:
            return jsonify({'code': ProjectHttpStatus.NO_FIND_CODE.value, 'msg': '中控设备信息不存在', 'data': {}}), 200

        # 校验修改后的中控设备信息是否被占用
        select_sql = "SELECT WorkSurCode From eq_control WHERE ConEquipCode={}".format(f"'{equ_code}'")
        is_exist = DBUtils.is_exist(cursor, select_sql, work_surface_code, EquipHttpStatus.EXIST_CODE.value,
                                    "中控设备编号已经被使用")
        if is_exist and old_equ_code != equ_code:
            return jsonify(is_exist), 200

        # 验证TunCode是否存在
        sql = "SELECT * From tunnel WHERE TunCode = {}".format(f"'{tun_code}'")
        res = DBUtils.project_is_exist(cursor, sql, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道不存在")
        if res:
            return jsonify(res), 200

        # 验证pro_code是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        project_is_exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                                    "修改后的隧道所属项目编号不存在")
        if project_is_exist:
            return jsonify(project_is_exist), 200

        # 验证StruCode是否存在
        stru_code_sql = "SELECT * From structure WHERE StruCode = {}".format(f"'{stru_code}'")
        res = DBUtils.project_is_exist(cursor, stru_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该结构物不存在")
        if res:
            return jsonify(res), 200

        # 验证WorkSurCode是否存在
        stru_code_sql = "SELECT * From work_surface WHERE WorkSurCode = {}".format(f"'{work_surface_code}'")
        res = DBUtils.project_is_exist(cursor, stru_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该工作面不存在")
        if res:
            return jsonify(res), 200

        sql = """
                UPDATE 
                    eq_control 
                SET 
                    ConEquipCode=%s, ConEquipName=%s, ConEquipIP=%s, ProCode=%s, TunCode=%s, WorkSurCode=%s, StruCode=%s
                Where 
                    ConEquipCode=%s AND WorkSurCode=%s;
                """
        rows = cursor.execute(sql, (
            equ_code, equ_name, equ_ip, pro_code, tun_code, work_surface_code, stru_code, old_equ_code, old_work_surface_code))
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


@console_db.route('/selectConsole', methods=['POST'])
def console_select():
    """
    获取中控设备信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'eq_control', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@console_db.route('/searchInfoByColumn', methods=['POST'])
def console_info_search_by_column():
    """
    根据中控设备表中的某个字段搜索对应的中控设备信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'eq_control', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200
