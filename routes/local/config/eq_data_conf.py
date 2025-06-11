"""
@Author: zhang_zhiyi
@Date: 2025/4/24_11:11
@FileName:eq_data_conf.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 采集设备-雷达端配置文件相关接口
"""
import time

import requests
from flask import Blueprint, jsonify, request

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.configHttpStatus import ConfigHttpStatus
from utils.util_conf import ConfUtils
from utils.util_database import DBUtils

eq_data_conf_db = Blueprint('eq_data_conf_db', __name__)

AVIA_PORT = 9023
AVIA_SUB_URL = 'api/inner/lidar_config'


@eq_data_conf_db.route('/start', methods=['POST'])
def start():
    """
    启动终端雷达设备
        1. 判断 ip 是否在线
        2. 判断终端雷达设备是否初始化
        3. 若已初始化则修改，则调用远端启动脚本
        4. 启动成功则修改设备状态
    TODO：
          1. PC端需要监控终端设备是否在线，若不在线则修改设备状态
          2. 终端在线的情况下，需要检测指定进程是否在运行状态，否不在运行状态，则调用PC相关接口修改设备状态
    """
    try:
        data = request.json
        data_code = data.get('DataAcqEquipCode')
        ip = data.get('IP')
        res = ConfUtils.eq_start(data_code, ip, 'eq_data', 'DataAcaEquipStatus', 'DataAcqEquipCode', AVIA_PORT,
                                 AVIA_SUB_URL)
        return res, 200
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '启动失败', 'data': {'exception': str(e)}})
    # result_dict = {
    #     0: {
    #         'code': BaseHttpStatus.INFO_SAME.value,
    #         'msg': '终端设备信息和原先一致',
    #         'data': ''
    #     },
    #     1: {
    #         'code': BaseHttpStatus.OK.value,
    #         'msg': '启动成功',
    #         'data': ''
    #     },
    #     2: {
    #         'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
    #         'msg': '太多终端设备记录被修改',
    #         'data': ''
    #     }
    # }
    # try:
    #     data = request.json
    #     data_code = data.get('DataAcqEquipCode')
    #     ip = data.get('IP')
    # except Exception as e:
    #     return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '启动失败', 'data': {'exception': str(e)}}), 200
    #
    # if not all([data_code, ip]):
    #     return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
    #
    # # 设备 IP 是否在线
    # if not ConfUtils.ip_is_online(ip):
    #     return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '中控设备不在线', 'data': {}}), 200
    #
    # con = None
    # cursor = None
    # try:
    #     dbu = DBUtils()
    #     con = dbu.connection()
    #     cursor = con.cursor()
    #
    #     # 验证 设备code 是否存在
    #     code_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
    #     res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
    #     if res:
    #         return jsonify(res), 200
    #
    #     # 判断设备是否已经初始化
    #     init_sql = f"SELECT Init, DataAcaEquipStatus From eq_data WHERE DataAcqEquipCode = {data_code}"
    #     cursor.execute(init_sql)
    #     res_tuple = cursor.fetchone()
    #     if res_tuple[0] == 0:
    #         return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '设备未进行初始化', 'data': {}}), 200
    #
    #     # 判断设备是否已经启动
    #     if res_tuple[1] == 1:
    #         return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '设备在线，无需启动', 'data': {}}), 200
    #
    #     # TODO: 调用远端启动脚本
    #
    #     # 修改设备状态
    #     status_sql = f"UPDATE eq_data SET DataAcaEquipStatus = 1 WHERE DataAcqEquipCode = {data_code}"
    #     rows = cursor.execute(status_sql)
    #     con.commit()
    #     return jsonify(DBUtils.kv(rows, result_dict)), 200
    # except Exception as e:
    #     if con:
    #         con.rollback()
    #     return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '启动失败', 'data': {'exception': str(e)}}), 200
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if con:
    #         DBUtils.close_connection(con)


@eq_data_conf_db.route('/stop', methods=['POST'])
def stop():
    """
    修改设备状态
    """
    try:
        data = request.json
        control_code = data.get('DataAcqEquipCode')
        ip = data.get('IP')
        res = ConfUtils.stop(control_code, 'eq_data', 'DataAcaEquipStatus', 'DataAcqEquipCode', ip, AVIA_PORT,
                             AVIA_SUB_URL)
        return res, 200
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    # result_dict = {
    #     0: {
    #         'code': BaseHttpStatus.ERROR.value,
    #         'msg': '更新失败',
    #         'data': {}
    #     },
    #     1: {
    #         'code': BaseHttpStatus.OK.value,
    #         'msg': '更新成功',
    #         'data': {}
    #     },
    #     2: {
    #         'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
    #         'msg': '多条设备状态被修改',
    #         'data': {}
    #     }
    # }
    # try:
    #     data = request.json
    #     data_code = data.get('DataAcqEquipCode')
    # except Exception as e:
    #     return jsonify(
    #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    #
    # if not all([data_code]):
    #     return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
    #
    # con = None
    # cursor = None
    # try:
    #     dbu = DBUtils()
    #     con = dbu.connection()
    #     cursor = con.cursor()
    #
    #     # 验证 设备code 是否存在
    #     code_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
    #     res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
    #     if res:
    #         return jsonify(res), 200
    #
    #     update_sql = f"UPDATE eq_data SET DataAcaEquipStatus = 0 WHERE DataAcqEquipCode = {data_code}"
    #     rows = cursor.execute(update_sql)
    #
    #     res = DBUtils.kv(rows, result_dict)
    #     if res.get('code') != 101:
    #         return jsonify(
    #             {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被修改或未发生改变', 'data': {}}), 200
    #
    #     # TODO: 远程停止终端工作
    #
    #     con.commit()
    #     return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '修改成功', 'data': {}}), 200
    # except Exception as e:
    #     if con:
    #         con.rollback()
    #     return jsonify(
    #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if con:
    #         DBUtils.close_connection(con)


@eq_data_conf_db.route('/init', methods=['POST'])
def init():
    """
    初始化终端设备配置文件
        1. 判断 ip 是否在线
        2. p判断 control_code 是否存在
        3. 若 ip 在线则向 eq_control_conf 中插入数据
        4. 插入成功后调用 ip 所在设备的接口 在中控设备PC上生成配置文件
        5. 返回插入成功响应后修改 eq_control 中的初始化状态字段
    """
    insert_result_dict = {
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
            'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '添加了多个配置信息',
            'data': ''
        }
    }
    update_result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '初始化失败',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '初始化成功',
            'data': ''
        },
        2: {
            'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '多条设备状态被修改',
            'data': ''
        }
    }

    try:
        now = str(time.time())
        data = request.json
        control_code = data.get('ConEquipCode')
        data_code = data.get('DataAcqEquipCode')
        conf_ip = data.get('ConfIP')  # 在前端控制设备 ip 必须和配置文件内的保持一致
        lp_stw = data.get('LidarParameterSTW', 0.1)
        lp_dur = data.get('LidarParameterDur', 1)
        lp_coll_inter = data.get('LidarParameterCollInter', 10)
        lp_conn_inter = data.get('LidarParameterConnInter', 10)
        lp_computer_ip = data.get('LidarParameterComputerIP', '192.168.1.7')
        lp_sensor_ip = data.get('LidarParameterSensorIP', '192.168.1.104')

        rp_username = data.get('RabbitmqParameterUsername', 'tunnel')
        rp_password = data.get('RabbitmqParameterPassword', '123456')
        rp_host = data.get('RabbitmqParameterHost', conf_ip)
        rp_post = data.get('RabbitmqParameterPort', '5672')
        rp_vhost = data.get('RabbitmqParameterVirtualHost', 'tunnel_vh')
        rp_en = data.get('RabbitmqParameterExchange', f'avia.control.{control_code}.topic')  # 交换机名称 雷达 -> 总控
        rp_et = data.get('RabbitmqParameterExchangeType', 'topic')
        rp_rk = data.get('RabbitmqParameterRoutingKey', f'avia.control.{data_code}.{control_code}')
        rp_conn_inter = data.get('RabbitmqParameterConnInterval', '10')
        rp_qn = data.get('RabbitmqParameterQueueName', f'avia.control.{data_code}.{control_code}.queue')
        conf_code = f"avia_{data_code}_{now}"
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200

    if not all(
            [data_code, conf_ip, lp_stw, lp_dur, lp_coll_inter, lp_conn_inter,
             rp_username, rp_password, rp_host, rp_post, rp_vhost,
             rp_en, rp_et, rp_conn_inter, conf_code, rp_rk, rp_qn, lp_computer_ip, lp_sensor_ip]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    # 初始化的设备 conf_ip 是否在线
    if not ConfUtils.ip_is_online(conf_ip, port=AVIA_PORT):
        return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '终端设备不在线', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 验证 设备code 是否存在
        code_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
        res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
        if res:
            return jsonify(res), 200

        # 配置信息是否存在
        code_sql = "SELECT * From eq_data_conf WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
        res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设配置不存在")
        if not res:
            # TODO: 删除已有的配置文件？
            return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '该设备的配置信息已经存在', 'data': {}}), 200

        # 插入数据
        insert_sql = """
            INSERT INTO eq_data_conf (
            ConfCode, DataAcqEquipCode, LidarParameterSTW,LidarParameterDur,LidarParameterCollInter,
            LidarParameterConnInter, RabbitmqParameterUsername, RabbitmqParameterPassword, 
            RabbitmqParameterHost, RabbitmqParameterPort, RabbitmqParameterVirtualHost, 
            RabbitmqParameterExchange, RabbitmqParameterExchangeType, RabbitmqParameterConnInterval,
             RabbitmqParameterRoutingKey, RabbitmqParameterQueueName, computerIP, sensorIP) 
            VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        insert_rows = cursor.execute(insert_sql, (
            conf_code, data_code, lp_stw, lp_dur, lp_coll_inter, lp_conn_inter, rp_username, rp_password, rp_host,
            rp_post, rp_vhost, rp_en, rp_et, rp_conn_inter, rp_rk, rp_qn, lp_computer_ip, lp_sensor_ip))

        if DBUtils.kv(insert_rows, insert_result_dict).get('code') != 101:
            return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '插入失败或存在多条相同记录', 'data': {}}), 200

        # 修改 eq_control 设备初始化字段
        update_sql = f"UPDATE eq_data SET Init = 1 WHERE DataAcqEquipCode = {data_code}"
        update_rows = cursor.execute(update_sql)

        # TODO：调用终端设备上的接口添加配置文件
        avia_url = f"http://{conf_ip}:{AVIA_PORT}/{AVIA_SUB_URL}/addConfig"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'LidarParameter': {
                'duration': lp_dur,
                'lidarCollInterval': lp_coll_inter,
                'lidarConnInterval': lp_conn_inter,
                'secsToWait': lp_stw,
                'computerIP': lp_computer_ip,
                'sensorIP': lp_sensor_ip
            },
            'RabbitmqParameter': {
                'username': rp_username,
                'password': rp_password,
                'host': rp_host,
                'port': rp_post,
                'virtualHost': rp_vhost,
                'exchange': rp_en,
                'exchangeType': rp_et,
                'connInterval': rp_conn_inter,
                'queueName': rp_qn,
                'routingKey': rp_rk
            }
        }
        response = requests.post(avia_url, json=data, headers=headers)
        if response.json().get('code') != 101:
            return response.json(), 200
        # print(response.json())
        # print(response.status_code)

        con.commit()
        return jsonify(DBUtils.kv(update_rows, update_result_dict)), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@eq_data_conf_db.route('/update', methods=['POST'])
def update():
    """
    更新终端设备配置文件
        1. 判断 ip 是否在线
        2. 若 ip 在线则修改 eq_control_conf 中的数据
        3. 修改成功后调用 ip 所在设备的接口 在中控设备PC上修改配置文件
        4. 返回修改成功响应后逻辑结束
    TODO：新设备可能处于故障状态，未做判断
    """
    result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '更新失败',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '更新成功',
            'data': ''
        },
        2: {
            'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '更新了多个配置信息',
            'data': ''
        }
    }

    update_result_dict = {
        0: {
            'code': BaseHttpStatus.ERROR.value,
            'msg': '更新失败',
            'data': ''
        },
        1: {
            'code': BaseHttpStatus.OK.value,
            'msg': '更新成功',
            'data': ''
        },
        2: {
            'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
            'msg': '多条设备状态被修改',
            'data': ''
        }
    }
    try:
        now = str(time.time())
        data = request.json
        # old_control_code 与 control_code 不一致时需要修改 eq_control 表中的 Init 字段
        old_data_code = data.get('OldDataAcqEquipCode')
        data_code = data.get('DataAcqEquipCode')
        control_code = data.get('ConEquipCode')
        old_conf_ip = data.get('OldConfIP')
        conf_ip = data.get('ConfIP')

        lp_stw = data.get('LidarParameterSTW', '0.1')
        lp_dur = data.get('LidarParameterDur', '1')
        lp_coll_inter = data.get('LidarParameterCollInter', '10')
        lp_conn_inter = data.get('LidarParameterConnInter', '10')

        rp_username = data.get('RabbitmqParameterUsername', 'tunnel')
        rp_password = data.get('RabbitmqParameterPassword', '123456')
        rp_host = data.get('RabbitmqParameterHost', conf_ip)
        rp_post = data.get('RabbitmqParameterPort', '5672')
        rp_vhost = data.get('RabbitmqParameterVirtualHost', 'tunnel_vh')
        rp_en = data.get('RabbitmqParameterExchange', f'avia.control.{control_code}.topic')
        rp_et = data.get('RabbitmqParameterExchangeType', 'topic')
        rp_rk = data.get('RabbitmqParameterRoutingKey', f'avia.control.{data_code}.{control_code}')
        rp_conn_inter = data.get('RabbitmqParameterConnInterval', '10')
        rp_qn = data.get('RabbitmqParameterQueueName', f'avia.control.{data_code}.{control_code}.queue')
        conf_code = f"avia_{data_code}_{now}"
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '更新失败', 'data': {'exception': str(e)}}), 200

    if not all(
            [old_data_code, data_code, conf_ip, lp_stw, lp_dur, lp_coll_inter, lp_conn_inter,
             rp_username, rp_password, rp_host, rp_post, rp_vhost,
             rp_en, rp_et, rp_conn_inter, conf_code, rp_rk, rp_qn, old_conf_ip]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    # 设备 IP 是否在线
    # if not ConfUtils.ip_is_online(old_conf_ip, port=AVIA_PORT):
    #     return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '当前设备不在线', 'data': {}}), 200

    # 修改后的设备 IP 是否在线
    if not ConfUtils.ip_is_online(old_conf_ip, port=AVIA_PORT):
        return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '当前设备不在线', 'data': {}}), 200

    con = None
    cursor = None
    # 是否要修改 old_control_code 在 eq_control 表中对应记录的 Init 值
    old_init_modify = False
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 验证 设备old_code 是否存在
        old_con_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{old_data_code}'")
        res = DBUtils.project_is_exist(cursor, old_con_sql, ConfigHttpStatus.NO_FIND_CODE.value, "待更新的设备不存在")
        if res:
            return jsonify(res), 200

        # 配置信息是否存在
        old_conf_sql = "SELECT * From eq_data_conf WHERE DataAcqEquipCode = {}".format(f"'{old_data_code}'")
        res = DBUtils.project_is_exist(cursor, old_conf_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设配置不存在")
        if res:
            return jsonify(res), 200

        # 删除旧数据
        old_conf_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{old_data_code}'")
        res = DBUtils.project_is_exist(cursor, old_conf_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设配置不存在")
        if not res:
            # 若存在直接删除，重新插入
            delete_sql = f"DELETE FROM eq_data_conf WHERE DataAcqEquipCode = {old_data_code}"
            delete_rows = cursor.execute(delete_sql)
            if DBUtils.kv(delete_rows, result_dict).get('code') != 101:
                # raise Exception("更新失败，在删除旧数据时")
                return jsonify(
                    {'code': ConfigHttpStatus.ERROR.value, 'msg': '更新失败在删除旧数据时', 'data': {}}), 200

            # return jsonify(
            #     {'code': ConfigHttpStatus.ERROR.value, 'msg': '修改后的配置信息所属的设备已有配置，无需重复创建',
            #      'data': {}}), 200

            # raise NotADirectoryError

        # 设备code是否发生变化
        if old_data_code != data_code:
            # 验证 设备code 是否存在
            con_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
            res = DBUtils.project_is_exist(cursor, con_sql, ConfigHttpStatus.NO_FIND_CODE.value, "修改后的设备不存在")
            if res:
                # raise Exception('修改后的设备不存在')
                return jsonify(res), 200

            # 判断新设备是否已有配置文件
            conf_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
            res = DBUtils.project_is_exist(cursor, conf_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设配置不存在")
            if not res:
                return jsonify(
                    {'code': ConfigHttpStatus.CONF_EXIST.value, 'msg': f'{data_code}设备已有配置', 'data': {}}), 200

            old_init_modify = True

            ip_sql = f"SELECT DataAcqEquipIP FROM eq_data WHERE DataAcqEquipCode = {data_code}"
            cursor.execute(ip_sql)
            ip_tuple = cursor.fetchone()
            ip = ip_tuple[0]
            consumer_rmq_host = ip_tuple[0]
            producer_rmq_host = ip_tuple[0]

            # 更新
            # update_conf_sql = """
            #     UPDATE
            #         eq_data_conf
            #     SET
            #         ConfCode=%s, DataAcqEquipCode=%s, LidarParameterSTW=%s, LidarParameterDur=%s, LidarParameterCollInter=%s,
            #         LidarParameterConnInter=%s, RabbitmqParameterUsername=%s, RabbitmqParameterPassword=%s, RabbitmqParameterHost=%s,
            #         RabbitmqParameterPort=%s, RabbitmqParameterVirtualHost=%s, RabbitmqParameterExchange=%s,
            #         RabbitmqParameterExchangeType=%s, RabbitmqParameterConnInterval=%s
            #     WHERE
            #         DataAcqEquipCode=%s;
            # """
            # rows = cursor.execute(update_conf_sql, (
            #     conf_code, data_code, lp_stw, lp_dur, lp_coll_inter, lp_conn_inter, rp_username, rp_password, rp_host,
            #     rp_post, rp_vhost, rp_en, rp_et, rp_conn_inter, old_data_code))
            # if DBUtils.kv(rows, result_dict).get('code') != 101:
            #     return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '更新失败或存在多条相同记录', 'data': {}}), 200

        # 插入数据
        insert_sql = """
                INSERT INTO eq_data_conf (
                ConfCode, DataAcqEquipCode, LidarParameterSTW,LidarParameterDur,LidarParameterCollInter,
                LidarParameterConnInter, RabbitmqParameterUsername, RabbitmqParameterPassword, 
                RabbitmqParameterHost, RabbitmqParameterPort, RabbitmqParameterVirtualHost, 
                RabbitmqParameterExchange, RabbitmqParameterExchangeType, RabbitmqParameterConnInterval, 
                RabbitmqParameterRoutingKey, RabbitmqParameterQueueName) 
                VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        insert_rows = cursor.execute(insert_sql, (
            conf_code, data_code, lp_stw, lp_dur, lp_coll_inter, lp_conn_inter, rp_username, rp_password, rp_host,
            rp_post, rp_vhost, rp_en, rp_et, rp_conn_inter, rp_rk, rp_qn))

        if DBUtils.kv(insert_rows, update_result_dict).get('code') != 101:
            # raise Exception('插入失败或存在多条相同记录')
            return jsonify(
                {'code': ConfigHttpStatus.ERROR.value, 'msg': '插入失败或存在多条相同记录', 'data': {}}), 200

        # 更新 Init
        if old_init_modify:
            old_sql = f"UPDATE eq_data SET Init = 0 WHERE DataAcqEquipCode = {old_data_code}"
            old_update_rows = cursor.execute(old_sql)
            if DBUtils.kv(old_update_rows, update_result_dict).get('code') != 101:
                # raise Exception('旧设备状态更新失败或存在多条相同记录')
                return jsonify(
                    {'code': ConfigHttpStatus.ERROR.value, 'msg': '旧设备状态更新失败或存在多条相同记录',
                     'data': {}}), 200

            sql = f"UPDATE eq_data SET Init = 1 WHERE DataAcqEquipCode = {data_code}"
            update_rows = cursor.execute(sql)
            if DBUtils.kv(update_rows, update_result_dict).get('code') != 101:
                # raise Exception('新设备状态更新失败或存在多条相同记录')
                return jsonify(
                    {'code': ConfigHttpStatus.ERROR.value, 'msg': '新设备状态更新失败或存在多条相同记录',
                     'data': {}}), 200

        # TODO：调用终端接口更新配置文件
        avia_url = f"http://{old_conf_ip}:{AVIA_PORT}/{AVIA_SUB_URL}/updateConfig"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'LidarParameter': {
                'duration': lp_dur,
                'lidarCollInterval': lp_coll_inter,
                'lidarConnInterval': lp_conn_inter,
                'secsToWait': lp_stw
            },
            'RabbitmqParameter': {
                'connInterval': rp_conn_inter,
                'exchange': rp_en,
                'exchangeType': rp_et,
                'host': rp_host,
                'port': rp_post,
                'username': rp_username,
                'password': rp_password,
                'virtualHost': rp_vhost,
                'queueName': rp_qn
            }
        }
        response = requests.post(avia_url, json=data, headers=headers)
        if response.json().get('code') != 101:
            return response.json(), 200

        con.commit()
        return jsonify({'code': ConfigHttpStatus.OK.value, 'msg': '更新成功', 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '更新失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)


@eq_data_conf_db.route('/delete', methods=['POST'])
def delete():
    """
    删除配置内容
    """
    try:
        data = request.json
        data_code = data.get('DataAcqEquipCode')
        data_ip = data.get('DataAcqEquipIP')
        res = ConfUtils.delete(data_code, 'eq_data', 'eq_data_conf', 'DataAcqEquipCode', data_ip, AVIA_PORT,
                               AVIA_SUB_URL)
        return res, 200
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '删除失败', 'data': {'exception': str(e)}}), 200
    # result_dict = {
    #     0: {
    #         'code': ConfigHttpStatus.NO_FIND_CODE.value,
    #         'msg': '删除失败，待删除的中控设备配置项不存在',
    #         'data': ''
    #     },
    #     1: {
    #         'code': BaseHttpStatus.OK.value,
    #         'msg': '删除成功',
    #         'data': ''
    #     },
    #     2: {
    #         'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
    #         'msg': '太多中控设备信息被删除',
    #         'data': ''
    #     }
    # }
    # update_result_dict = {
    #     0: {
    #         'code': BaseHttpStatus.ERROR.value,
    #         'msg': '更新失败',
    #         'data': ''
    #     },
    #     1: {
    #         'code': BaseHttpStatus.OK.value,
    #         'msg': '更新成功',
    #         'data': ''
    #     },
    #     2: {
    #         'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
    #         'msg': '多条设备状态被修改',
    #         'data': ''
    #     }
    # }
    # try:
    #     data = request.json
    #     data_code = data.get('DataAcqEquipCode')
    # except Exception as e:
    #     return jsonify(
    #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    #
    # if not all([data_code]):
    #     return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
    #
    # con = None
    # cursor = None
    # try:
    #     dbu = DBUtils()
    #     con = dbu.connection()
    #     cursor = con.cursor()
    #
    #     # 验证 设备code 是否存在
    #     code_sql = "SELECT * From eq_data WHERE DataAcqEquipCode = {}".format(f"'{data_code}'")
    #     res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
    #     if res:
    #         return jsonify(res), 200
    #
    #     delete_sql = f"DELETE FROM eq_data_conf WHERE DataAcqEquipCode = {data_code}"
    #     rows = cursor.execute(delete_sql)
    #
    #     res = DBUtils.kv(rows, result_dict)
    #     if res.get('code') != 101:
    #         return jsonify(
    #             {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被删除或没有记录被删除', 'data': {}}), 200
    #
    #     # 修改设备状态
    #     update_sql = f"UPDATE eq_data SET Init = 0 WHERE DataAcqEquipCode = {data_code}"
    #     update_rows = cursor.execute(update_sql)
    #     res = DBUtils.kv(update_rows, update_result_dict)
    #     if res.get('code') != 101:
    #         return jsonify(
    #             {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被更新或没有记录被更新', 'data': {}}), 200
    #
    #     # TODO: 远程删除终端配置文件
    #
    #     con.commit()
    #     return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '删除成功', 'data': {}}), 200
    # except Exception as e:
    #     if con:
    #         con.rollback()
    #     return jsonify(
    #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if con:
    #         DBUtils.close_connection(con)


@eq_data_conf_db.route('/selectConf', methods=['POST'])
def select_conf():
    """
    查看配置内容
    """
    try:
        data = request.json
        res = DBUtils.search_by_some_item('eq_data_conf', data.get('Item'), data.get('Value'), data=data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200
