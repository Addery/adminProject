"""
@Author: zhang_zhiyi
@Date: 2024/10/17_11:35
@FileName:project.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库项目表相关路由
"""
from datetime import datetime

from flask import jsonify, request, Blueprint
# from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils

project_db = Blueprint('project_db', __name__)


@project_db.route('/addProject', methods=['POST'])
def project_add():
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
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个项目',
            'data': ''
        }
    }
    try:
        now = datetime.now()
        data = request.json
        pro_code = data.get('ProCode')
        name = data.get('ProName')
        address = data.get('ProAddress')
        linkman = data.get('LinkMan')
        phone = data.get('Phone')
        create_time = data.get('ProCreateTime', now.strftime("%Y-%m-%d %H:%M:%S"))
        status = data.get('ProStatus', 0)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([pro_code, name, address, linkman, phone]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证ProCode是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        res = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                       "不存在该项目编号")
        if not res:
            return jsonify({'code': ProjectHttpStatus.EXIST_CODE.value, 'msg': '该项目已经存在', 'data': {}}), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO project (ProCode, ProName, ProAddress, LinkMan, Phone, ProCreateTime, ProStatus) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql, (pro_code, name, address, linkman, phone, create_time, status))
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


@project_db.route('/deleteProject', methods=['POST'])
def project_delete():
    """
    项目删除
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '删除失败, 不存在该项目',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '删除了多个项目',
            'data': ''
        }
    }
    try:
        data = request.json
        pro_code = data.get('ProCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([pro_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 项目存在执行删除操作
        sql = """
        DELETE FROM project WHERE ProCode = %s
        """
        rows = cursor.execute(sql, (pro_code,))
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


@project_db.route('/updateProject', methods=['POST'])
def project_update():
    """
    项目更新
    :return:
    """
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
            'msg': '更新了多个项目',
            'data': ''
        }
    }
    try:
        data = request.json
        old_pro_code = data.get('OldProCode')
        pro_code = data.get('ProCode')
        name = data.get('ProName')
        address = data.get('ProAddress')
        linkman = data.get('LinkMan')
        phone = data.get('Phone')
        now = datetime.now()
        create_time = data.get('ProCreateTime', now.strftime("%Y-%m-%d %H:%M:%S"))
        status = data.get('ProStatus', 0)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '更新失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([old_pro_code, pro_code, name, address, linkman, phone]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证old_pro_code是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{old_pro_code}'")
        exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "项目不存在")
        if exist:
            return jsonify(exist), 200

        # 验证pro_code是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "项目编号不存在")
        if not exist and old_pro_code != pro_code:
            return jsonify({'code': ProjectHttpStatus.EXIST_CODE.value, 'msg': '修改后的项目编号已经存在'}), 200

        sql = """
           UPDATE 
                project 
           SET 
                ProCode=%s, ProName=%s, ProAddress=%s, LinkMan=%s, Phone=%s, ProCreateTime=%s, ProStatus=%s
           WHERE 
                ProCode = %s
           """
        rows = cursor.execute(sql, (pro_code, name, address, linkman, phone, create_time, status, old_pro_code))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '更新失败', 'data': {str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@project_db.route('/selectProject', methods=['POST'])
def project_select():
    """
    项目信息分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'project', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@project_db.route('/searchProjectByColumn', methods=['POST'])
def project_search():
    """
    根据项目表中的某个字段搜索对应的项目信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'project', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200
