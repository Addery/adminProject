"""
@Author: zhang_zhiyi
@Date: 2024/10/12_9:14
@FileName:user.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库用户表相关路由
"""

from flask import jsonify, request, Blueprint, Flask
from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils
from routes.local.status_code.userHttpStatus import UserHttpStatus

user_db = Blueprint('user_db', __name__)


@user_db.route('/login', methods=['POST'])
def user_login():
    """
    用户登录
    :return:
    """
    try:
        data = request.json
        # 获取用户登录信息
        phone = data.get('Phone')
        password = data.get('PassWord')
    except Exception as e:
        return jsonify({"code": BaseHttpStatus.GET_DATA_ERROR.value, "msg": "登录失败", "data": {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([phone, password]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        sql = "SELECT * FROM user WHERE Phone = {}".format(f"'{phone}'")
        cursor.execute(sql)
        user = cursor.fetchone()
        con.commit()
        if not user:
            return jsonify({"code": UserHttpStatus.NO_USER.value, "msg": "该账号未注册", "data": {}}), 200
        elif user['PassWord'] == password:  # 用户名和密码匹配成功
            return jsonify({"code": BaseHttpStatus.OK.value, "msg": "登陆成功",
                            "data": {"ID": user["ID"], "UserName": user["UserName"],
                                     "PassWord": user["PassWord"],
                                     "RealName": user["RealName"],
                                     "RoleClass": user["RoleClass"],
                                     "RoleID": user["RoleID"], "Phone": user["Phone"],
                                     "ProCode": user["ProCode"],
                                     "Status": user["Status"]}}), 200
        else:
            return jsonify({"code": UserHttpStatus.LOGIN_PASSWORD_ERROR.value, "msg": "密码不正确", 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({"code": BaseHttpStatus.EXCEPTION.value, "msg": f"登录失败", "data": {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@user_db.route('/addUser', methods=['POST'])
def user_add():
    """
    添加用户、用户注册
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
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '添加了多个用户',
            'data': ''
        }
    }
    try:
        data = request.json
        username = data.get("UserName")
        password = data.get("PassWord")
        real_name = data.get("RealName")
        role_class = data.get("RoleClass", 1)
        role_id = data.get("UserCode", 1)
        phone = data.get("Phone")
        pro_code = data.get("ProCode")
        status = data.get("Status", 0)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([username, password, real_name, phone, pro_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    # 校验手机号码格式
    if len(phone) != 11:
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '手机号格式不对', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 验证ProCode是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        res = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                       "用户所属项目编号不存在")
        if res:
            return jsonify(res), 200

        # 校验待添加的用户是否已经存在
        # select_sql = "SELECT ProCode From user WHERE UserName={}".format(f"'{username}'")
        # 验证手机号码是否存在
        select_sql = "SELECT Phone From user"
        res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value, "该用户已经存在")
        if res:
            return jsonify(res), 200

        # 若为新用户则执行添加操作
        insert_sql = """
        INSERT INTO user (UserName, PassWord, RealName, RoleClass, UserCode, Phone, ProCode, Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        rows = cursor.execute(insert_sql, (username, password, real_name, role_class, role_id, phone, pro_code, status))
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


@user_db.route('/deleteUser', methods=['POST'])
def user_delete():
    """
    用户删除
    :return:
    """
    result_dict = {
        0: {
            'code': UserHttpStatus.NO_USER.value,
            'msg': '删除失败，待删除的用户不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多用户被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        # username = data.get('UserName')
        # pro_code = data.get('ProCode')
        phone = data.get('Phone')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    # if not all([username, pro_code]):
    if not all([phone]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        sql = """
        DELETE FROM user WHERE Phone = %s
        """
        rows = cursor.execute(sql, phone)
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


@user_db.route('/updateUser', methods=['POST'])
def user_update():
    """
    更新用户信息
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '用户信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多用户被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_phone = data.get("OldPhone")
        password = data.get("PassWord")
        username = data.get("UserName")
        real_name = data.get("RealName")
        role_class = data.get("RoleClass")
        role_id = data.get("UserCode", 1)
        phone = data.get("Phone")
        pro_code = data.get("ProCode")
        status = data.get("Status", 0)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([old_phone, username, password, real_name, role_class, phone, pro_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    # 校验手机号码格式
    if len(phone) != 11 or len(old_phone) != 11:
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '手机号格式不对', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待修改的用户是否已经存在
        select_sql = "SELECT phone From user"
        old_is_exist = DBUtils.is_exist(cursor, select_sql, old_phone,
                                        UserHttpStatus.USER_HAS_EXISTED.value, "用户存在")
        if not old_is_exist:
            return jsonify({'code': UserHttpStatus.NO_USER.value, 'msg': '用户信息不存在', 'data': {}}), 200

        # 验证新手机号码是否存在
        res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value, "该用户已经存在")
        if res:
            return jsonify(res), 200

        # 用户信息是否发生变化
        # if old_pro_code == pro_code and old_username == username:
        #     return jsonify({'code': UserHttpStatus.INFO_SAME.value, 'msg': '用户信息未发生更改', 'data': {}}), 200

        # 校验修改后的用户信息是否被占用
        # select_sql = "SELECT ProCode From user WHERE UserName={}".format(f"'{username}'")
        # is_exist = DBUtils.is_exist(cursor, select_sql, pro_code, UserHttpStatus.USER_INFO_CLASH.value,
        #                             "用户名已经被使用")
        # if is_exist and old_username != username:
        #     return jsonify(is_exist), 200

        # 验证pro_code是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        project_is_exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                                    "修改后的用户所属项目编号不存在")

        if project_is_exist:
            return jsonify(project_is_exist), 200

        sql = """
        UPDATE 
            user 
        SET 
            UserName=%s, PassWord=%s, RealName=%s, RoleClass=%s, UserCode=%s, Phone=%s, ProCode=%s, Status=%s 
        Where 
            Phone=%s;
        """

        rows = cursor.execute(
            sql,
            (username, password, real_name, role_class, role_id, phone, pro_code, status, old_phone)
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


@user_db.route('/selectUser', methods=['POST'])
def user_select():
    """
    获取用户信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'user', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@user_db.route('/searchInfoByColumn', methods=['POST'])
def user_info_search_by_column():
    """
    根据用户表中的某个字段搜索对应的用户信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('user', data.get('Item'), data.get('Value'), data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@user_db.route('/modifyUserPermission', methods=['POST'])
def user_permission_modify():
    """
    用户权限修改
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '没有用户被修改，请检查待修改的用户信息是否正确',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '权限修改成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多用户被修改',
            'data': ''
        }
    }
    try:
        data = request.json
        phone = data.get('Phone')
        role_class = data.get('RoleClass', 1)
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '权限修改失败', 'data': {str(e)}}), 200

    # 校验必填字段
    if not all([phone, str(role_class)]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待用户是否存在
        select_sql = "SELECT Phone From user"
        res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value,
                               "该用户已经存在")
        if not res:
            return jsonify({'code': UserHttpStatus.NO_USER.value, 'msg': '用户不存在', 'data': {}}), 200

        sql = """
        UPDATE user SET RoleClass = %s WHERE Phone = %s
        """
        rows = cursor.execute(sql, (role_class, phone))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '权限修改失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@user_db.route('/setUserPassword', methods=['POST'])
def user_password_set():
    """
    重置密码
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '不能和原先密码一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '重置成功',
            'data': ''
        },
        2: {
            'code': UserHttpStatus.TOO_MANY_USER.value,
            'msg': '太多用户被修改',
            'data': ''
        }
    }
    try:
        data = request.json
        phone = data.get('Phone')
        password = data.get('PassWord')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '重置失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([phone, password]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()

        # 校验待用户是否存在
        select_sql = "SELECT Phone From user"
        res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value,
                               "用户存在")
        if not res:
            return jsonify({'code': UserHttpStatus.NO_USER.value, 'msg': '用户不存在', 'data': {}}), 200

        sql = """
        UPDATE user SET PassWord=%s WHERE Phone = %s
        """
        rows = cursor.execute(sql, (password, phone))
        con.commit()
        return jsonify(DBUtils.kv(rows, result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '重置失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


if __name__ == "__main__":
    user_add()


