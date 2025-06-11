"""
@Author: zhang_zhiyi
@Date: 2025/4/23_17:49
@FileName:util_conf.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 配置文件相关工具
"""
import socket

import requests
from flask import jsonify

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.configHttpStatus import ConfigHttpStatus
from utils.util_database import DBUtils


class ConfUtils(object):
    AVIA_PORT = 9023
    AVIA_SUB_URL = 'api/inner/lidar_config'

    @staticmethod
    def ip_is_online(ip, port=3306, timeout=1):
        """
        判断 ip 是否在线
        三种方法：ping / 尝试连接常见端口（如 22/80/5000）/ 批量扫描整个局域网
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
                return True
            except Exception as e:
                return False

    @staticmethod
    def eq_start(eq_code, ip, table_name, status_column, code_column, port, sub_url):
        """
        启动设备通用方法
        """
        result_dict = {
            0: {
                'code': BaseHttpStatus.INFO_SAME.value,
                'msg': '设备信息和原先一致',
                'data': ''
            },
            1: {
                'code': BaseHttpStatus.OK.value,
                'msg': '启动成功',
                'data': ''
            },
            2: {
                'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
                'msg': '太多设备记录被修改',
                'data': ''
            }
        }
        if not all([eq_code, ip, table_name, status_column, code_column, port, sub_url]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}})

        # 设备 IP 是否在线
        if not ConfUtils.ip_is_online(ip, port=ConfUtils.AVIA_PORT):
            return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '设备不在线', 'data': {}})

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection()
            cursor = con.cursor()
            con.autocommit(False)

            # 验证 设备code 是否存在
            code_sql = f"SELECT * From {table_name} WHERE {code_column} = {eq_code}"
            res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
            if res:
                return jsonify(res)

            # 判断设备是否已经初始化
            init_sql = f"SELECT Init, {status_column} From {table_name} WHERE {code_column} = {eq_code}"
            cursor.execute(init_sql)
            res_tuple = cursor.fetchone()
            if res_tuple[0] == 0:
                return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '设备未进行初始化', 'data': {}})

            # 判断设备是否已经启动
            if res_tuple[1] == 1:
                return jsonify({'code': ConfigHttpStatus.ERROR.value, 'msg': '设备在线，无需启动', 'data': {}})

            # TODO: 调用远端启动脚本
            url = f"http://{ip}:{port}/{sub_url}/start"
            headers = {
                'Content-Type': 'application/json'
            }
            data = {}
            response = requests.post(url, json=data, headers=headers)
            if response.json().get('code') != 101:
                raise Exception(str(response.json()))

            # 修改设备状态
            status_sql = f"UPDATE {table_name} SET {status_column} = 1 WHERE {code_column} = {eq_code}"
            rows = cursor.execute(status_sql)
            con.commit()
            return jsonify(DBUtils.kv(rows, result_dict))
        except Exception as e:
            if con:
                con.rollback()
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '启动失败', 'data': {'exception': str(e)}})
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def stop(eq_code, table_name, status_column, code_column, ip, port, sub_url):
        """
        修改设备状态
        """
        result_dict = {
            0: {
                'code': BaseHttpStatus.ERROR.value,
                'msg': '更新失败',
                'data': {}
            },
            1: {
                'code': BaseHttpStatus.OK.value,
                'msg': '更新成功',
                'data': {}
            },
            2: {
                'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
                'msg': '多条设备状态被修改',
                'data': {}
            }
        }
        # try:
        #     data = request.json
        #     control_code = data.get('ConEquipCode')
        # except Exception as e:
        #     return jsonify(
        #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200

        if not all([eq_code, table_name, status_column, code_column, ip]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}})

        # 设备 IP 是否在线
        if not ConfUtils.ip_is_online(ip, port=ConfUtils.AVIA_PORT):
            return jsonify({'code': ConfigHttpStatus.NO_EXIST.value, 'msg': '设备不在线', 'data': {}})

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection()
            cursor = con.cursor()
            con.autocommit(False)

            # 验证 设备code 是否存在
            code_sql = f"SELECT * From {table_name} WHERE {code_column} = {eq_code}"
            res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
            if res:
                return jsonify(res), 200

            update_sql = f"UPDATE {table_name} SET {status_column} = 0 WHERE {code_column} = {eq_code}"
            rows = cursor.execute(update_sql)

            res = DBUtils.kv(rows, result_dict)
            if res.get('code') != 101:
                return jsonify(
                    {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被修改或未发生改变', 'data': {}})

            # TODO: 远程停止设备工作
            url = f"http://{ip}:{port}/{sub_url}/stop"
            headers = {
                'Content-Type': 'application/json'
            }
            data = {}
            response = requests.post(url, json=data, headers=headers)
            if response.json().get('code') != 101:
                raise Exception(str(response.json()))

            con.commit()
            return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '停止成功', 'data': {}})
        except Exception as e:
            if con:
                con.rollback()
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}})
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def delete(eq_code, eq_table_name, conf_table_name, code_column, control_ip, port, sub_url):
        """
        删除配置内容
        """
        result_dict = {
            0: {
                'code': ConfigHttpStatus.NO_FIND_CODE.value,
                'msg': '删除失败，待删除的设备配置项不存在',
                'data': ''
            },
            1: {
                'code': BaseHttpStatus.OK.value,
                'msg': '删除成功',
                'data': ''
            },
            2: {
                'code': ConfigHttpStatus.TOO_MANY_PROJECT.value,
                'msg': '太多设备信息被删除',
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
        # try:
        #     data = request.json
        #     control_code = data.get('ConEquipCode')
        # except Exception as e:
        #     return jsonify(
        #         {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '初始化失败', 'data': {'exception': str(e)}}), 200

        if not all([eq_code, eq_table_name, conf_table_name, code_column, control_ip, port, sub_url]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}})

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection()
            cursor = con.cursor()
            con.autocommit(False)

            # 验证 设备code 是否存在
            code_sql = f"SELECT * From {eq_table_name} WHERE {code_column} = {eq_code}"
            res = DBUtils.project_is_exist(cursor, code_sql, ConfigHttpStatus.NO_FIND_CODE.value, "该设备不存在")
            if res:
                return jsonify(res)

            delete_sql = f"DELETE FROM {conf_table_name} WHERE {code_column} = {eq_code}"
            rows = cursor.execute(delete_sql)

            res = DBUtils.kv(rows, result_dict)
            if rows != 1:
                print(rows)
                # if res.get('code') != 101:
                return jsonify(
                    {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被删除或没有记录被删除', 'data': {}})

            # 修改设备状态
            update_sql = f"UPDATE {eq_table_name} SET Init = 0 WHERE {code_column} = {eq_code}"
            update_rows = cursor.execute(update_sql)
            res = DBUtils.kv(update_rows, update_result_dict)
            if update_rows != 1:
                return jsonify(
                    {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '多条记录被更新或没有记录被更新', 'data': {}})

            # TODO: 远程删除设备配置文件
            avia_url = f"http://{control_ip}:{port}/{sub_url}/deleteConfig"
            headers = {
                'Content-Type': 'application/json'
            }
            data = {}
            response = requests.post(avia_url, json=data, headers=headers)
            if response.json().get('code') != 101:
                return response.json(), 200

            con.commit()
            return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '删除成功', 'data': {}})
        except Exception as e:
            if con:
                con.rollback()
            return jsonify(
                {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '删除失败', 'data': {'exception': str(e)}})
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)


if __name__ == '__main__':
    # print(ConfUtils.ip_is_online('192.168.1.10'))
    # print(ConfUtils.eq_start('1001', '192.168.1.8', 'eq_data', 'DataAcaEquipStatus', 'DataAcqEquipCode'))
    print(ConfUtils.delete('1001', 'eq_data', 'eq_data_conf', 'ConEquipCode', '192.168.1.8', '7023', 'api/inner/control_config'))
