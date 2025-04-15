"""
@Author: zhang_zhiyi
@Date: 2025/4/8_15:27
@FileName:role.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库角色表相关路由
"""
from datetime import datetime

from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor
from utils.util_database import DBUtils

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.userHttpStatus import UserHttpStatus

role_db = Blueprint('role_db', __name__)


@role_db.route('/addRole', methods=['POST'])
def role_add():
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
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '添加了多个角色',
            'data': ''
        }
    }
    try:
        now = datetime.now()
        data = request.json
        role = data.get('RoleClass')
        creator = data.get('Creator')
        create_time = data.get('CreateTime', now)
        status = data.get('Status', 0)
        user_code = data.get('UserCode')
        reserved1 = data.get('Reserved1', 1)
        reserved2 = data.get('Reserved2', 1)
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([role, creator, user_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证 UserCode 是否存在
        user_code_sql = "SELECT * From user WHERE UserCode = {}".format(f"'{user_code}'")
        res = DBUtils.project_is_exist(cursor, user_code_sql, UserHttpStatus.NO_USER.value,
                                       "用户编号不存在")
        if res:
            return jsonify(res), 200

        insert_sql = """
                INSERT INTO role (RoleClass, Creator, CreateTime, Status, UserCode, Reserved1, Reserved2) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql, (role, creator, create_time, status, user_code, reserved1, reserved2))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@role_db.route('/deleteRole', methods=['POST'])
def role_delete():
    """
    角色删除
    :return:
    """
    result_dict = {
        0: {
            'code': UserHttpStatus.NO_USER.value,
            'msg': '删除失败，待删除的角色不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多角色被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        id = data.get('ID')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([id]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
        DELETE FROM role WHERE ID = %s 
        """
        rows = cursor.execute(sql, id)
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


@role_db.route('/updateRole', methods=['POST'])
def role_update():
    """
    更新角色信息
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '角色信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多角色被修改',
            'data': ''
        }
    }

    try:
        now = datetime.now()
        data = request.json
        old_id = data.get("OldID")
        role = data.get('RoleClass')
        creator = data.get('Creator')
        create_time = data.get('CreateTime', now)
        status = data.get('Status', 0)
        user_code = data.get('UserCode')
        reserved1 = data.get('Reserved1', 1)
        reserved2 = data.get('Reserved2', 1)
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([old_id, role, creator, user_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待修改的用户是否已经存在
        select_old_sql = "SELECT * From role WHERE ID={}".format(old_id)
        res = DBUtils.project_is_exist(cursor, select_old_sql, UserHttpStatus.NO_USER.value,
                                       "角色不存在")
        if res:
            return jsonify(res), 200

        # 验证 UserCode 是否存在
        user_code_sql = "SELECT * From user WHERE UserCode = {}".format(f"'{user_code}'")
        res = DBUtils.project_is_exist(cursor, user_code_sql, UserHttpStatus.NO_USER.value,
                                       "修改后的用户编号不存在")
        if res:
            return jsonify(res), 200

        sql = """
        UPDATE 
            role 
        SET 
            RoleClass=%s, Creator=%s, CreateTime=%s, Status=%s, UserCode=%s, Reserved1=%s, Reserved2=%s
        Where 
            ID=%s;
        """

        rows = cursor.execute(
            sql,
            (role, creator, create_time, status, user_code, reserved1, reserved2, old_id)
        )
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@role_db.route('/selectRole', methods=['POST'])
def role_select():
    """
    获取角色信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'role', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@role_db.route('/searchInfoByColumn', methods=['POST'])
def role_info_search_by_column():
    """
    根据角色表中的某个字段搜索对应的角色信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('role', data.get('Item'), data.get('Value'), data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200
