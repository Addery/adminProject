"""
@Author: zhang_zhiyi
@Date: 2024/10/17_18:32
@FileName:work_surface.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库工作面表相关路由
"""

from flask import jsonify, request, Blueprint

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils

work_surface_db = Blueprint('work_surface_db', __name__)


@work_surface_db.route('/addWorkSur', methods=['POST'])
def work_sur_add():
    """
    添加工作面信息
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
            'msg': '添加了多个工作面',
            'data': ''
        }
    }
    try:
        data = request.json
        work_surface_code = data.get('WorkSurCode')
        name = data.get('WorkSurName')
        tun_code = data.get('TunCode')
        pro_code = data.get('ProCode')
        stru_code = data.get('StruCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([work_surface_code, name, tun_code, pro_code, stru_code]):
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

        # 校验待添加的工作面是否已经存在
        select_sql = "SELECT TunCode From work_surface WHERE WorkSurCode = {}".format(f"'{work_surface_code}'")
        res = DBUtils.is_exist(cursor, select_sql, tun_code, ProjectHttpStatus.NO_FIND_CODE.value, "该工作面已经存在")
        if res:
            return jsonify(res), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO work_surface (WorkSurCode, WorkSurName, ProCode, TunCode, StruCode) VALUES (%s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql, (work_surface_code, name, pro_code, tun_code, stru_code))
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


@work_surface_db.route('/deleteWorkSur', methods=['POST'])
def work_sur_delete():
    """
    删除工作面信息
    :return:
    """
    result_dict = {
        0: {
            'code': ProjectHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的工作面不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多工作面信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        tun_code = data.get('TunCode')
        work_surface_code = data.get('WorkSurCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([tun_code, work_surface_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
              DELETE FROM work_surface WHERE TunCode = %s and WorkSurCode = %s
              """
        rows = cursor.execute(sql, (tun_code, work_surface_code))
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


@work_surface_db.route('/updateWorkSur', methods=['POST'])
def work_sur_update():
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '工作面信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多工作面信息被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_tun_code = data.get("OldTunCode")
        old_work_surface_code = data.get("OldWorkSurCode")
        name = data.get("WorkSurName")
        work_surface_code = data.get("WorkSurCode")
        tun_code = data.get("TunCode")
        pro_code = data.get("ProCode")
        stru_code = data.get("StruCode")
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([old_tun_code, old_work_surface_code, tun_code, name, work_surface_code, pro_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待修改的工作面信息是否已经存在
        select_old_sql = "SELECT TunCode From work_surface WHERE WorkSurCode={}".format(f"'{old_work_surface_code}'")
        old_is_exist = DBUtils.is_exist(cursor, select_old_sql, old_tun_code, ProjectHttpStatus.EXIST_CODE.value,
                                        "隧道信息存在")
        if not old_is_exist:
            return jsonify({'code': ProjectHttpStatus.NO_FIND_CODE.value, 'msg': '工作面信息不存在', 'data': {}}), 200

        # 校验修改后的隧道信息是否被占用
        select_sql = "SELECT TunCode From work_surface WHERE WorkSurCode={}".format(f"'{work_surface_code}'")
        is_exist = DBUtils.is_exist(cursor, select_sql, tun_code, ProjectHttpStatus.EXIST_CODE.value,
                                    "工作面编号已经被使用")
        if is_exist and old_tun_code != tun_code:
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

        sql = """
                UPDATE 
                    work_surface 
                SET 
                    WorkSurCode=%s, WorkSurName=%s, ProCode=%s, TunCode=%s, StruCode=%s
                Where 
                    TunCode=%s AND WorkSurCode=%s;
                """

        rows = cursor.execute(sql, (work_surface_code, name, pro_code, tun_code, stru_code, old_tun_code, old_work_surface_code))
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


@work_surface_db.route('/selectWorkSur', methods=['POST'])
def work_sur_select():
    """
    获取工作面信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'work_surface', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200


@work_surface_db.route('/searchWorkSurByColumn', methods=['POST'])
def work_sur_select_by_column():
    """
    根据工作面表中的某个字段搜索对应的工作面信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item(data, 'work_surface', data.get('item'), data.get('value'))
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}), 200
