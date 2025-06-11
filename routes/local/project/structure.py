"""
@Author: zhang_zhiyi
@Date: 2024/10/18_9:31
@FileName:structure.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库结构物表相关路由
"""

from flask import jsonify, request, Blueprint

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils

structure_db = Blueprint('structure_db', __name__)


@structure_db.route('/addStructure', methods=['POST'])
def structure_add():
    """
    添加结构物信息
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
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个结构物',
            'data': ''
        }
    }
    try:
        data = request.json
        code = data.get('StruCode')
        name = data.get('StruName')
        fir_level = data.get('FirWarningLevel')
        sec_level = data.get('SecWarningLevel')
        thir_level = data.get('ThirWarningLevel')
        company_code = data.get('CompanyCode', '07361dfa-defc-4a08-ba11-5a495db9e565')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([code, name, fir_level, sec_level, thir_level, company_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 校验待添加的结构物是否已经存在
        select_sql = "SELECT StruCode From structure WHERE StruCode = {}".format(f"'{code}'")
        res = DBUtils.is_exist(cursor, select_sql, code, ProjectHttpStatus.NO_FIND_CODE.value, "待添加的结构物已经存在")
        if res:
            return jsonify(res), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO structure (StruCode, StruName, FirWarningLevel, SecWarningLevel, ThirWarningLevel, CompanyCode) VALUES (%s, %s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql, (code, name, fir_level, sec_level, thir_level, company_code))
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


@structure_db.route('/deleteStructure', methods=['POST'])
def structure_delete():
    """
    删除结构物信息
    :return:
    """
    result_dict = {
        0: {
            'code': ProjectHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的结构物不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多结构物信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        code = data.get('StruCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        sql = """
              DELETE FROM structure WHERE StruCode = %s
              """
        rows = cursor.execute(sql, code)
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


@structure_db.route('/updateStructure', methods=['POST'])
def structure_update():
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '结构物信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多结构物信息被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_code = data.get("OldStruCode")
        code = data.get("StruCode")
        name = data.get("StruName")
        fir_level = data.get("FirWarningLevel")
        sec_level = data.get("SecWarningLevel")
        thir_level = data.get("ThirWarningLevel")
        company_code = data.get('CompanyCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([old_code, code, name, fir_level, sec_level, thir_level, company_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 校验待修改的结构物信息是否已经存在
        select_old_sql = "SELECT StruCode From structure WHERE StruCode={}".format(f"'{old_code}'")
        old_is_exist = DBUtils.is_exist(cursor, select_old_sql, old_code, ProjectHttpStatus.EXIST_CODE.value,
                                        "结构物信息存在")
        if not old_is_exist:
            return jsonify(
                {'code': ProjectHttpStatus.NO_FIND_CODE.value, 'msg': '待修改的结构物信息不存在', 'data': {}}), 200

        # 校验修改后的结构物信息是否被占用
        select_sql = "SELECT StruCode From structure WHERE StruCode={}".format(f"'{code}'")
        is_exist = DBUtils.is_exist(cursor, select_sql, code, ProjectHttpStatus.EXIST_CODE.value,
                                    "结构物编号已经被使用")
        if is_exist and old_code != code:
            return jsonify(is_exist), 200

        sql = """
                    UPDATE 
                        structure 
                    SET 
                        StruCode=%s, StruName=%s, FirWarningLevel=%s, SecWarningLevel=%s, ThirWarningLevel=%s, CompanyCode=%s
                    Where 
                        StruCode=%s
                    """

        rows = cursor.execute(sql, (code, name, fir_level, sec_level, thir_level, company_code, old_code))
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


@structure_db.route('/selectStructure', methods=['POST'])
def structure_select():
    """
    获取结构物信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display_condition_on_sql(data, 'structure', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@structure_db.route('/searchStructureByColumn', methods=['POST'])
def structure_select_by_column():
    """
    根据结构物表中的某个字段搜索对应的结构物信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('structure', data.get('Item'), data.get('Value'), data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200
