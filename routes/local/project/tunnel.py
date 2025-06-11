"""
@Author: zhang_zhiyi
@Date: 2024/10/17_17:07
@FileName:tunnel.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库隧道表相关路由
"""
import datetime

# import time

from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus
from utils.util_database import DBUtils
from utils.util_statistics import StUtils

tunnel_db = Blueprint('tunnel_db', __name__)


@tunnel_db.route('/addTunnel', methods=['POST'])
def tunnel_add():
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
            'msg': '添加了多个隧道',
            'data': ''
        }
    }
    try:
        now = datetime.datetime.now()
        data = request.json
        tun_code = data.get('TunCode')
        name = data.get('TunName')
        linkman = data.get('LinkMan')
        phone = data.get('Phone')
        status = data.get('TunStatus', 0)
        pro_code = data.get('ProCode')
        high = data.get('High')
        cycle = data.get('TunCycle', 0)
        create_time = data.get('TunCreateTime', now.strftime("%Y-%m-%d %H:%M:%S"))
        length = data.get('Length')
        cur_advance = data.get('CurAdvancement', 0)
        company_code = data.get('CompanyCode', '07361dfa-defc-4a08-ba11-5a495db9e565')

        # 解析日期
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        hour = str(now.hour)
        minute = str(now.minute)
        second = str(now.second)
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all(
            [tun_code, name, linkman, phone, pro_code, high, str(length), company_code, year, month, day, hour, minute,
             second, str(cur_advance)]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 验证ProCode是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        res = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该项目不存在")
        if res:
            return jsonify(res), 200

        # 校验待添加的隧道是否已经存在
        select_sql = "SELECT TunCode From tunnel WHERE TunCode = {}".format(f"'{tun_code}'")
        res = DBUtils.is_exist(cursor, select_sql, tun_code, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道已经存在")
        if res:
            return jsonify(res), 200

        # 若为新项目则执行添加操作
        insert_sql = """
                INSERT INTO tunnel (TunCode, TunName, LinkMan, Phone, TunStatus, ProCode, High, TunCycle, TunCreateTime, Length, CompanyCode, Year, Month, Day, Hour, Minute, Second, CurAdvancement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        rows = cursor.execute(insert_sql,
                              (tun_code, name, linkman, phone, status, pro_code, high, cycle, create_time, length,
                               company_code, year,  month, day, hour, minute, second, cur_advance))
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


@tunnel_db.route('/deleteTunnel', methods=['POST'])
def tunnel_delete():
    """
    隧道信息删除
    :return:
    """
    result_dict = {
        0: {
            'code': ProjectHttpStatus.NO_FIND_CODE.value,
            'msg': '删除失败，待删除的隧道不存在',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '删除成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多隧道信息被删除',
            'data': ''
        }
    }
    try:
        data = request.json
        username = data.get('TunCode')
        pro_code = data.get('ProCode')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all([username, pro_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        sql = """
          DELETE FROM tunnel WHERE TunCode = %s and ProCode = %s
          """
        rows = cursor.execute(sql, (username, pro_code))
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


@tunnel_db.route('/updateTunnel', methods=['POST'])
def tunnel_update():
    """
    更新隧道信息
    :return:
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.INFO_SAME.value,
            'msg': '隧道信息和原先一致',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '修改成功',
            'data': ''
        },
        2: {
            'code': ProjectHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '太多隧道信息被修改',
            'data': ''
        }
    }

    try:
        data = request.json
        old_tun_code = data.get("OldTunCode")
        old_pro_code = data.get("OldProCode")
        tun_code = data.get("TunCode")
        pro_code = data.get("ProCode")
        name = data.get("TunName")
        linkman = data.get("LinkMan")
        phone = data.get("Phone")
        high = data.get("High")
        status = data.get("TunStatus", 0)
        cycle = data.get("TunCycle", 0)
        create_time = data.get('TunCreateTime')
        cur_advance = data.get('CurAdvancement')

        try:
            # 若为标准格式，如 "YYYY-MM-DD HH:MM:SS"
            create_time = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # 若为 ISO 格式（自动识别）
            create_time = datetime.datetime.fromisoformat(create_time)

        year = str(create_time.year)
        month = str(create_time.month)
        day = str(create_time.day)
        hour = str(create_time.hour)
        minute = str(create_time.minute)
        second = str(create_time.second)

        company_code = data.get('CompanyCode')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '修改失败', 'data': {'exception': str(e)}}), 200

    # 校验必填字段
    if not all(
            [old_tun_code, old_pro_code, tun_code, name, linkman, phone, pro_code, high, company_code, year, month, day,
             hour, minute, second, str(cur_advance)]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 校验待修改的隧道信息是否已经存在
        select_old_sql = "SELECT ProCode From tunnel WHERE TunCode={}".format(f"'{old_tun_code}'")
        old_is_exist = DBUtils.is_exist(cursor, select_old_sql, old_pro_code, ProjectHttpStatus.EXIST_CODE.value,
                                        "隧道信息存在")
        if not old_is_exist:
            return jsonify({'code': ProjectHttpStatus.NO_FIND_CODE.value, 'msg': '隧道信息不存在', 'data': {}}), 200

        # 校验修改后的隧道信息是否被占用
        select_sql = "SELECT ProCode From tunnel WHERE TunCode={}".format(f"'{tun_code}'")
        is_exist = DBUtils.is_exist(cursor, select_sql, pro_code, ProjectHttpStatus.EXIST_CODE.value,
                                    "隧道编号已经被使用")
        if is_exist and old_tun_code != tun_code:
            return jsonify(is_exist), 200

        # 验证pro_code是否存在
        pro_code_sql = "SELECT * From project WHERE ProCode = {}".format(f"'{pro_code}'")
        project_is_exist = DBUtils.project_is_exist(cursor, pro_code_sql, ProjectHttpStatus.NO_FIND_CODE.value,
                                                    "修改后的隧道所属项目编号不存在")

        if project_is_exist:
            return jsonify(project_is_exist), 200

        sql = """
            UPDATE 
                tunnel 
            SET 
                TunCode=%s, TunName=%s, LinkMan=%s, Phone=%s, TunStatus=%s, ProCode=%s, High=%s, TunCycle=%s, 
                TunCreateTime=%s, CompanyCode=%s, Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s, Second=%s, CurAdvancement=%s
            Where 
                TunCode=%s;
            """

        rows = cursor.execute(sql, (
            tun_code, name, linkman, phone, status, pro_code, high, cycle, create_time, company_code, year, month, day,
            hour, minute, second, str(cur_advance), old_tun_code))
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


@tunnel_db.route('/selectTunnel', methods=['POST'])
def tunnel_select():
    """
    获取隧道信息，分页展示
    :return:
    """
    try:
        data = request.json
        res = DBUtils.paging_display_condition_on_sql(data, 'tunnel', 1, 10, join=True)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@tunnel_db.route('/searchTunnelByColumn', methods=['POST'])
def tunnel_select_by_column():
    """
    根据隧道表中的某个字段搜索对应的隧道信息
    :return:
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('tunnel', data.get('Item'), data.get('Value'), join=True, data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@tunnel_db.route('/getExchangeName2Web', methods=['POST'])
def get_queue_name():
    try:
        data = request.json
        tun_code = data.get('TunCode')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}), 200

    if not all([tun_code]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的参数', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        con.autocommit(False)

        # 验证 隧道tun_code 是否存在
        tun_sql = "SELECT * From tunnel WHERE TunCode = {}".format(f"'{tun_code}'")
        res = DBUtils.project_is_exist(cursor, tun_sql, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道不存在")
        if res:
            return jsonify(res), 200

        # 判断隧道是否正在开挖过程或者已竣工过程中
        status_sql = "SELECT TunStatus FROM tunnel WHERE TunCode = {}".format(f"'{tun_code}'")
        cursor.execute(status_sql)
        items = cursor.fetchall()
        if len(items) != 1:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '隧道信息存在问题', 'data': {}}), 200
        if items[0].get('TunStatus') != 1:
            return jsonify(
                {'code': BaseHttpStatus.ERROR.value, 'msg': '隧道未开工，不能查看', 'data': {}}), 200

        # select_sql = "SELECT WebRMQQueueName FROM eq_control_conf WHERE ConEquipCode = %s"
        # cursor.execute(select_sql, control_code)
        # items = cursor.fetchall()
        # if items:
        con.commit()
        return jsonify({
            'data': {'WebRMQExchangeName': 'control.web.1001.fanout'},
            'code': BaseHttpStatus.OK.value,
            'msg': '成功'
        }), 200
    except Exception as e:
        if con:
            con.rollback()
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@tunnel_db.route('/statisticsStatus', methods=['POST'])
def statistics_status():
    """
    统计状态
    """
    try:
        data = request.json
        table = data.get("Table", "tunnel")
        time_column = data.get("TunCreateTime", "TunCreateTime")
        cycle_column = data.get("TunCycle", "TunCycle")
        item = data.get('Item', None)
        value = data.get('Value', None)
        res = StUtils.get_time_and_cycle_from_table(table, time_column, cycle_column, item, value)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}), 200
