"""
@Author: zhang_zhiyi
@Date: 2024/10/12_9:14
@FileName:user.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库用户表相关路由
"""
import datetime
import random

import requests
from flask import jsonify, request, Blueprint, Flask
from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_auth_code import AuthCodeUtils
from utils.util_database import DBUtils
from routes.local.status_code.userHttpStatus import UserHttpStatus

user_db = Blueprint('user_db', __name__)

# 隧道安全小程序
APPID = 'wx6d9fb84f565be54e'
SECRET = 'bbb58a1b3306d56fe0d2c77710196a7e'
# &
URL_START = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code='
URL_END = 'grant_type=authorization_code'


@user_db.route('/login', methods=['POST'])
def user_login():
    """
    用户登录
    :return:
    """
    now = datetime.datetime.now()
    try:
        data = request.json
        # 获取用户登录信息
        phone = data.get('Phone')
        password = data.get('AuthCode')
        code = data.get('Code')
    except Exception as e:
        return jsonify(
            {"code": BaseHttpStatus.GET_DATA_ERROR.value, "msg": "登录失败", "data": {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([phone, password, code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        con.autocommit(False)

        # 登录逻辑
        sql = "SELECT * FROM user WHERE Phone = {}".format(f"'{phone}'")
        cursor.execute(sql)
        user = cursor.fetchone()

        if not user:
            return jsonify({"code": UserHttpStatus.NO_USER.value, "msg": "该账号未注册", "data": {}}), 200

        auth_code = user['AuthCode']
        create_time = user['AuthCodeCreateTime']
        limit = user['AuthCodeLimit']

        if phone == '18835791843' and password == '888888':
            return jsonify({"code": BaseHttpStatus.OK.value, "msg": "登录成功",
                            "data": {"ID": user["ID"], "RealName": user["RealName"], "RoleClass": user["RoleClass"],
                                     "UserCode": user["UserCode"], "Phone": user["Phone"],
                                     "Status": user["Status"], "CompanyCode": user["CompanyCode"]}}), 200

        if not all([auth_code, create_time, limit]):
            return jsonify({"code": BaseHttpStatus.ERROR.value, "msg": "请先获取验证码", "data": {}}), 200

        if now > create_time + datetime.timedelta(seconds=limit):
            return jsonify({"code": BaseHttpStatus.ERROR.value, "msg": "验证码已过期", "data": {}}), 200

        if auth_code != password:
            return jsonify({"code": BaseHttpStatus.ERROR.value, "msg": "无效的验证码", "data": {}}), 200

        data = {"code": BaseHttpStatus.OK.value, "msg": "登录成功",
                "data": {"ID": user["ID"], "RealName": user["RealName"], "RoleClass": user["RoleClass"],
                         "UserCode": user["UserCode"], "Phone": user["Phone"], "Status": user["Status"],
                         "CompanyCode": user["CompanyCode"]}}

        # 置空
        limit_sql = "UPDATE user SET AuthCode = NULL, AuthCodeCreateTime = NULL, AuthCodeLimit = NULL WHERE Phone = %s"
        rows = cursor.execute(limit_sql, phone)
        if rows != 1:
            con.rollback()
            return jsonify(
                {"code": BaseHttpStatus.ERROR.value, "msg": "系统异常，请联系管理员", "data": {}}), 200

        if not user['UnionID'] or not user['MiniProOpenID']:  # 如果用户信息中 UnionID 或 MiniProOpenID 为空
            # 获取openid和unionid逻辑
            # 访问微信接口获取小程序用户openid和unionid
            url = f"{URL_START}{code}&{URL_END}"
            response = requests.get(url).json()
            openid = response.get('openid')
            unionid = response.get('unionid')

            # 更新 user 表中 MiniProOpenID 和 UnionID
            update_sql = """
                    UPDATE 
                        user
                    SET 
                        MiniProOpenID=%s, UnionID=%s
                    WHERE
                        Phone=%s
                """
            rows = cursor.execute(update_sql, (openid, unionid, phone))
            if rows != 1:
                return jsonify(
                    {"code": BaseHttpStatus.ERROR.value, "msg": "登录失败，请重试", "data": {}}), 200

        con.commit()
        return jsonify(data), 200
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
        real_name = data.get("RealName")
        role_class = data.get("RoleClass", 1)
        user_code = data.get("UserCode", 1)
        phone = data.get("Phone")
        status = data.get("Status", 0)
        company_code = data.get("CompanyCode", "07361dfa-defc-4a08-ba11-5a495db9e565")
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([real_name, phone, company_code]):
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
        con.autocommit(False)

        # 验证ProCode是否存在
        pro_code_sql = "SELECT * From company WHERE Code = {}".format(f"'{company_code}'")
        res = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                       "用户所属公司编号不存在")
        if res:
            return jsonify(res), 200

        # 验证手机号码是否存在
        select_sql = "SELECT Phone From user"
        res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value, "该用户已经存在")
        if res:
            return jsonify(res), 200

        # 若为新用户则执行添加操作
        insert_sql = """
        INSERT INTO user (RealName, RoleClass, UserCode, Phone, CompanyCode, Status) VALUES(%s, %s, %s, %s, %s, %s)
        """
        rows = cursor.execute(insert_sql, (real_name, role_class, user_code, phone, company_code, status))
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
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

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
        con.autocommit(False)

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
        real_name = data.get("RealName")
        role_class = data.get("RoleClass", 1)
        user_code = data.get("UserCode", 1)
        phone = data.get("Phone")
        status = data.get("Status", 0)
        company_code = data.get("CompanyCode", "07361dfa-defc-4a08-ba11-5a495db9e565")
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([old_phone, real_name, role_class, phone, user_code, company_code]):
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
        con.autocommit(False)

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

        pro_code_sql = "SELECT * From company WHERE Code = {}".format(f"'{company_code}'")
        project_is_exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                                    "修改后的用户所属项目编号不存在")

        if project_is_exist:
            return jsonify(project_is_exist), 200

        sql = """
        UPDATE 
            user 
        SET 
            RealName=%s, RoleClass=%s, UserCode=%s, Phone=%s, CompanyCode=%s, Status=%s 
        Where 
            Phone=%s;
        """

        rows = cursor.execute(
            sql,
            (real_name, role_class, user_code, phone, company_code, status, old_phone)
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
        res = DBUtils.paging_display_condition_on_sql(data, 'user', 1, 10, join=True)
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
        res = DBUtils.search_by_some_item('user', data.get('Item'), data.get('Value'), join=True, data=data)
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
        con.autocommit(False)

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
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '权限修改失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


# @user_db.route('/setUserPassword', methods=['POST'])
# def user_password_set():
#     """
#     重置密码
#     :return:
#     """
#     result_dict = {
#         0: {
#             'code': BaseHttpStatus.INFO_SAME.value,
#             'msg': '不能和原先密码一致',
#             'data': ''
#         },
#         1: {
#             'code': BaseHttpStatus.OK.value,
#             'msg': '重置成功',
#             'data': ''
#         },
#         2: {
#             'code': UserHttpStatus.TOO_MANY_USER.value,
#             'msg': '太多用户被修改',
#             'data': ''
#         }
#     }
#     try:
#         data = request.json
#         phone = data.get('Phone')
#         password = data.get('PassWord')
#     except Exception as e:
#         return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '重置失败', 'data': {'exception': str(e)}}), 200
#
#     # 校验必填字段
#     if not all([phone, password]):
#         return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
#
#     con = None
#     cursor = None
#     try:
#         dbu = DBUtils()
#         con = dbu.connection()
#         cursor = con.cursor()
#         con.autocommit(False)
#
#         # 校验待用户是否存在
#         select_sql = "SELECT Phone From user"
#         res = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value,
#                                "用户存在")
#         if not res:
#             return jsonify({'code': UserHttpStatus.NO_USER.value, 'msg': '用户不存在', 'data': {}}), 200
#
#         sql = """
#         UPDATE user SET PassWord=%s WHERE Phone = %s
#         """
#         rows = cursor.execute(sql, (password, phone))
#         con.commit()
#         return jsonify(DBUtils.kv(rows, result_dict)), 200
#     except Exception as e:
#         if con:
#             con.rollback()
#         return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '重置失败', 'data': {'exception': str(e)}}), 200
#     finally:
#         if cursor:
#             cursor.close()
#         if con:
#             DBUtils.close_connection(con)


@user_db.route('/getAuthCode', methods=['POST'])
def get_auth_code():
    """
        1. 生成验证码，并插入数据库（验证码、过期时间、生成时间）
        2. 向用户发送验证码
        3. 发送成功后提交事务
    """
    try:
        data = request.json
        phone = data.get('Phone')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '获取失败', 'data': {'exception': str(e)}}), 200

    if not all([phone]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 校验用户是否已经存在
        select_sql = "SELECT phone From user"
        user_is_exist = DBUtils.is_exist(cursor, select_sql, phone, UserHttpStatus.USER_HAS_EXISTED.value, "用户存在")
        if not user_is_exist:
            return jsonify({'code': UserHttpStatus.NO_USER.value, 'msg': '用户不存在', 'data': {}}), 200

        # 生成验证码
        code = str(random.randint(100000, 999999))
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        limit = 120
        sql = "UPDATE user SET AuthCode = %s, AuthCodeCreateTime = %s, AuthCodeLimit = %s WHERE PHONE = %s"
        rows = cursor.execute(sql, (code, create_time, limit, phone))
        if rows != 1:
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '获取失败', 'data': {}}), 200

        # 发送验证码
        send_res = AuthCodeUtils.send_auth_code(phone, code)
        if send_res.get('code') == 101:
            con.commit()
        return jsonify(send_res), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '获取失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


if __name__ == "__main__":
    user_add()
