"""
@Author: zhang_zhiyi
@Date: 2025/5/6_14:46
@FileName:company.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime
import time
import uuid

from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils

company_db = Blueprint('company_db', __name__)


@company_db.route('/addCompany', methods=['POST'])
def add_company():
    try:
        data = request.json
        now = time.time()
        now_datetime = datetime.datetime.now()
        name = data.get("CompanyName")
        address = data.get("CompanyAddress")
        buy_time = data.get("BuyTime", now_datetime)
        code = str(uuid.uuid4())  # 使用 UUID 生成唯一 code
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([name, address, buy_time, code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 若为新用户则执行添加操作
        insert_sql = """
        INSERT INTO company (Code, Name, Address, BuyTime) VALUES(%s, %s, %s, %s)
        """
        rows = cursor.execute(insert_sql, (code, name, address, buy_time))
        if rows != 1:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '添加失败，在插入时', 'data': {}}), 200
        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '添加成功', 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@company_db.route('/deleteCompany', methods=['POST'])
def company_delete():
    try:
        data = request.json
        code = data.get('Code')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

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
        DELETE FROM company WHERE Code = %s
        """
        rows = cursor.execute(sql, code)
        if rows != 1:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '删除失败', 'data': {}}), 200
        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '删除成功', 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@company_db.route('/updateCompany', methods=['POST'])
def company_update():
    try:
        data = request.json
        old_code = data.get("OldCode")
        code = data.get("Code", old_code)
        name = data.get("Name")
        address = data.get("Address")
        buy_time = data.get("BuyTime")
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([old_code, code, name, address, buy_time]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        sql = """
        UPDATE 
            company 
        SET 
            Code = %s, Name = %s, Address = %s, BuyTime = %s
        Where 
            Code=%s;
        """
        rows = cursor.execute(sql, (code, name, address, buy_time, old_code))
        if rows != 1:
            return jsonify({'code': BaseHttpStatus.ERROR.value, 'msg': '修改失败', 'data': {}}), 200
        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '修改成功', 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@company_db.route('/selectCompany', methods=['POST'])
def company_select():
    """
    获取公司信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'company', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@company_db.route('/searchInfoByColumn', methods=['POST'])
def user_info_search_by_column():
    """
    根据公司表中的某个字段搜索对应的用户信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('company', data.get('Item'), data.get('Value'), data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200
