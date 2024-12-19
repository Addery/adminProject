"""
@Author: zhang_zhiyi
@Date: 2024/9/3_15:04
@FileName:util_database.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import os
import time
from datetime import datetime
import ast

from pymysql.connections import Connection
import logging
import configparser

from pymysql.cursors import Cursor, DictCursor

from rabiitmq.construct import Tunnel
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.logHttpStatus import LogHttpStatus
from routes.local.status_code.projectHttpStatus import ProjectHttpStatus


class DBUtils(object):
    """
    数据库操作类
    """

    DEFAULT_DATABASE = "tunnel_project"
    CURRENT_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_CONFIG_PATH = os.path.join(CURRENT_PROJECT_PATH, "../config/database_config.ini")
    DEFAULT_LOG_PATH = os.path.join(CURRENT_PROJECT_PATH, "../log/database.log")
    PROJECT_COLUMNS = ['ProCode', 'ProAddress', 'LinkMan', 'Phone', 'ProCreateTime', 'ProStatus']
    TUNNEL_COLUMNS = ['TunCode', 'TunName', 'LinkMan', 'Phone', 'TunStatus', 'ProCode']
    WORK_SURFACE_COLUMNS = ['WorkSurCode', 'WorkSurName', 'ProCode', 'TunCode']
    STRUCTURE_COLUMNS = ['StruCode', 'StruName', 'FirWarningLevel', 'SecWarningLevel', 'ThirWarningLevel', 'ProCode',
                         'TunCode', 'WorkSurCode']
    CON_EQUIP_COLUMNS = ['ConEquipCode', 'ConEquipName', 'ConEquipIP', 'ProCode', 'TunCode', 'WorkSurCode', 'StruCode']
    DATA_ACQ_EQUIP_COLUMNS = ['DataAcqEquipCode', 'DataAcqEquipName', 'DataAcqEquipIP', 'DataAcqEquipInterval',
                              'Distance', 'DataAcqEquipStatus', 'ConEquipCode']
    COLUMNS = {
        'project': PROJECT_COLUMNS,
        'tunnel': TUNNEL_COLUMNS,
        'work_surface': WORK_SURFACE_COLUMNS,
        'structure': STRUCTURE_COLUMNS,
        'central_control_equipment': CON_EQUIP_COLUMNS,
        'data_acquisition_equipment': DATA_ACQ_EQUIP_COLUMNS
    }

    def __init__(self, config_path=None):
        self.config_path = config_path or DBUtils.DEFAULT_CONFIG_PATH
        self._host = None
        self._port = None
        self._user = None
        self._password = None

        # 配置日志记录器
        logging.basicConfig(
            filename=DBUtils.DEFAULT_LOG_PATH,  # 日志输出的文件
            level=logging.INFO,  # 记录 ERROR 及以上级别的日志
            format='%(asctime)s - %(levelname)s - %(message)s'  # 自定义日志格式
        )

        # 加载配置
        self._load_config()

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    def _load_config(self):
        """
        加载配置文件并读取数据库链接参数
        :return:
        """
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_path):
            logging.error(f"配置文件 {self.config_path} 不存在.")
            raise FileNotFoundError(f"配置文件 {self.config_path} 不存在.")

        try:
            config.read(self.config_path)

            self._host = config.get("parameters", "host", fallback="localhost")
            self._port = int(config.get("parameters", "port", fallback="3306"))
            self._user = config.get("parameters", "user", fallback="root")
            self._password = config.get("parameters", "password", fallback="123456")

        except configparser.NoSectionError as e:
            logging.error(f"{e}: 配置文件缺少parameters部分")
            raise
        except configparser.NoOptionError as e:
            logging.error(f"{e}: 配置文件中缺少关键配置项")
            raise
        except Exception as e:
            logging.error(f"{e}: 读取配置文件时发生错误")
            raise

        logging.info("数据库配置成功加载")

    def connection(self, database_name=DEFAULT_DATABASE, cursor_class=Cursor):
        """
        获取数据库连接对象
        :return:
        """
        try:
            # 创建数据库连接
            conn = Connection(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                autocommit=True,
                database=database_name,
                cursorclass=cursor_class
            )
            logging.info("MySQL数据库连接成功")
            return conn
        except Exception as e:
            logging.error(f"{e}: MySQL数据库连接失败")
            raise  # 抛出异常供调用者处理

    def __str__(self):
        return f"DBUtils(host: {self._host}, port: {self._port}, user: {self._user}, password: {self._password})"

    @staticmethod
    def close_connection(con: Connection):
        """
        关闭数据库连接对象
        :param con:
        :return:
        """
        if con:
            con.close()

    @staticmethod
    def get_table_columns(con: Connection, table_name):
        """
        获取表的字段信息
        :param con:
        :param table_name:
        :return:
        """
        cursor = None
        cursor_res = None
        try:
            cursor = con.cursor()
            sql = "DESC {}".format(table_name)
            cursor.execute(sql)
            cursor_res = cursor.fetchall()
            return cursor_res
        except Exception as e:
            logging.error(f"{e}: 执行get_table_columns方法是发生异常")
            return cursor_res
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def select_table(con: Connection, table_name, *args):
        """
        返回数据库中某个表的某些字段数据
            *args: ((column, column, column),)
        :param con:
        :param table_name:
        :return:
        """
        cursor = None
        cursor_res = None
        try:
            if con:
                cursor = con.cursor()
                columns_list = list(map(str, DBUtils.COLUMNS.get(table_name)))
                if args[0]:  # 如果给定select的字段名称
                    columns_list = list(map(str, args[0]))
                columns = ', '.join(columns_list)
                # 使用参数化查询来避免 SQL 注入
                sql = "SELECT {} FROM {}".format(columns, table_name)
                cursor.execute(sql)
                cursor_res = cursor.fetchall()
                return cursor_res
        except Exception as e:
            logging.error(f"{e}: 执行select_table方法时发生异常")
            return cursor_res
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def insert_table(con: Connection, table_name, insert_dict: dict):
        """
        插入信息
        :param con:
        :param table_name:
        :param insert_dict:
        :return:
        """
        cursor = None
        try:
            cursor = con.cursor()
            columns = ", ".join(list(insert_dict.keys()))
            values = "', '".join(list(insert_dict.values()))
            values = f"'{values}'"
            sql = "INSERT INTO {}({}) VALUES({})".format(table_name, columns, values)
            cursor.execute(sql)
            return "insert table success"
        except Exception as e:
            logging.error(f"{e}: 执行insert_table方法时发生异常")
            return f"{e}: 执行insert_table方法时发生异常"
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete_table(con: Connection, table_name, delete_condition: dict = None):
        """
        删除数据
        :param con:
        :param table_name:
        :param delete_condition:
        :return:
        """
        cursor = None
        delete_rows = -1
        try:
            cursor = con.cursor()
            if delete_condition is None:
                sql = 'DELETE FROM {}'.format(table_name)
            else:
                column = list(delete_condition.keys())[0]
                value = list(delete_condition.values())[0]
                sql = 'DELETE FROM {} WHERE {}={}'.format(table_name, column, f"'{value}'")
            delete_rows = cursor.execute(sql)
            # test = cursor.execute('DELETE FROM project WHERE ProCode= \'1008\'')
            # print(delete_rows, test)
            return delete_rows
        except Exception as e:
            logging.error(f"{e}: 执行delete_table方法时发生异常")
            return delete_rows
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def update_table(con: Connection, table_name, update_column, update_value, target_column, target_value):
        """
        修改表中数据
        :param target_value:
        :param target_column:
        :param update_value:
        :param update_column:
        :param con: 连接对象
        :param table_name: 表名
        :return:
        """
        cursor = None
        try:
            cursor = con.cursor()
            sql = 'UPDATE {} SET {}={} WHERE {}={}'.format(table_name, update_column, f"'{update_value}'",
                                                           target_column, f"'{target_value}'")
            cursor.execute(sql)
            # cursor.execute('UPDATE project SET ProName=\'test_update1\' WHERE ProCode=\'1006\'')
            return "update table success"
        except Exception as e:
            logging.error(f"{e}: 执行update_table方法时发生异常")
            return f"{e}: 执行update_table方法时发生异常"
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def kv(key, target_dict):
        """
        根据受影响的行数匹配返回信息
        :param key:
        :param target_dict:
        :return:
        """
        if key > 1:  # 0 和 1 以外的所有正整数
            return target_dict[2]
        return target_dict[key]

    @staticmethod
    def is_exist(cursor, sql, column, status_code, msg):
        """
        校验待添加的用户是否已经存在
        :return:
        """
        cursor.execute(sql)
        select_res = cursor.fetchall()  # [{}, {}]
        if (f'{column}',) in select_res:  # 用户存在
            return {'code': status_code, 'msg': msg, 'data': {}}
        return None

    @staticmethod
    def project_is_exist(cursor, sql, code, msg):
        """
        验证ProCode是否存在
        :param cursor:
        :param sql:
        :param code:
        :param msg:
        :return:
        """
        cursor.execute(sql)
        cursor_res = cursor.fetchall()  # []
        if not cursor_res:
            return {'code': code, 'msg': msg, 'data': {}}
        return None

    @staticmethod
    def check_existence(cursor, table, column, code, error_code, error_msg):
        sql = f"""
        SELECT * From {table} WHERE {column} = '{code}'
        """
        return DBUtils.project_is_exist(cursor, sql, error_code, error_msg)

    @staticmethod
    def paging_display(data, table_name, p, ps):
        """
        :param data: request.json
        :param table_name: 表名
        :param p: 默认的页数
        :param ps: 一页中默认的记录数
        :return:
        data = {
            'page': ...,  页码
            'page_size': ...  一页多少条数据
        }
        SELECT * FROM users LIMIT 10 OFFSET 0;
        LIMIT 10 表示每次查询 10 条记录，OFFSET 0 表示从第 0 条记录开始（即第一页）
        """
        try:
            page = data.get('Page', p)
            page_size = data.get('PageSize', ps)
            offset = (page - 1) * page_size
        except Exception as e:
            return {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '查找失败', 'data': {str(e)}}

        # 校验必填字段
        if not all([str(page), str(page_size)]):
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

        if offset < 0:
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': 'page不合法', 'data': {}}

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            with con.cursor() as cursor:
                # 查询总记录数
                cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
                total = cursor.fetchone()['total']

                sql = f"""
                SELECT * FROM {table_name} LIMIT %s OFFSET %s
                """

                cursor.execute(sql, (page_size, offset))
                items = cursor.fetchall()
                if not items:
                    return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': {}}
                data = {
                    'items': items,
                    'total': total,  # 总记录数
                    'page': page,
                    'page_size': page_size,
                    'total_page': (total + page_size - 1) // page_size  # 总页数
                }
                con.commit()
                return {'code': BaseHttpStatus.OK.value, 'msg': '查找成功', 'data': data}
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def search_by_some_item(data, table_name, item, value):
        # 校验必填字段
        if not all([item, value]):
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}, 200

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()

            # 统计符合要求的记录总数量
            cursor.execute(f"SELECT COUNT(*) as total FROM {table_name} Where {item} = %s", value)
            total = cursor.fetchone()['total']

            sql = f"""
                SELECT * FROM {table_name} WHERE {item} = %s
            """
            cursor.execute(sql, value)
            res = cursor.fetchall()
            con.commit()
            if res:
                return {
                    'code': BaseHttpStatus.OK.value,
                    'msg': '查找成功',
                    'data': {
                        'total': total,
                        'items': res
                    }
                }
            return {'code': BaseHttpStatus.ERROR.value, 'msg': '不存在符合要求的记录', 'data': {}}
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def log_insert(tunnel: Tunnel):
        """
        :param tunnel:
        :return:
        """
        # now = datetime.now()
        con = None
        cursor = None
        try:
            # 获取异常数据
            data = tunnel.get_data()
            anomaly = data.get_anomaly()
            if anomaly:
                anomaly_describe = anomaly.get_describe()
                k = list(anomaly_describe.keys())
                position, bas, degree = [], [], []
                for e in k:
                    position.append(anomaly_describe.get(e)[0])
                    bas.append(anomaly_describe.get(e)[1])
                    degree.append(anomaly_describe.get(e)[2])

                acq_code = tunnel.device_id
                dbu = DBUtils()
                con = dbu.connection(cursor_class=DictCursor)
                cursor = con.cursor()
                acq_sql = """
                SELECT ConEquipCode, Distance FROM eq_data WHERE DataAcqEquipCode = %s
                """
                cursor.execute(acq_sql, acq_code)
                acq_res = cursor.fetchone()
                if not acq_res:
                    return None

                # 数据采集器编号对应的中控设备编号
                con_code = acq_res['ConEquipCode']
                distance = acq_res['Distance']

                con_sql = """
                SELECT * FROM eq_control WHERE ConEquipCode = %s
                """
                cursor.execute(con_sql, con_code)
                con_res = cursor.fetchone()
                if not con_res:
                    return None

                data = {
                    # 'DescCode': str(time.time()),
                    'Degree': degree,
                    'Identification': str(time.time()),
                    'Region': k,
                    'Position': position,
                    'Bas': bas,
                    'ProCode': con_res['ProCode'],
                    'TunCode': con_res['TunCode'],
                    'WorkSurCode': con_res['WorkSurCode'],
                    'StruCode': con_res['StruCode'],
                    'Mileage': distance,
                    'ConEquipCode': con_code,
                    'DataAcqEquipCode': acq_code,
                    'AnomalyTime': str(data.get_time().strftime("%Y-%m-%d %H:%M:%S"))
                }
                res = DBUtils.log_insert_db(data)
                return True if res['code'] == BaseHttpStatus.OK.value else False
        except Exception as e:
            if con:
                con.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def log_insert_db(data):
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
                'code': LogHttpStatus.TOO_MANY_PROJECT.value,
                'msg': '添加了多个日志',
                'data': ''
            }
        }
        try:
            desc_code = data.get('DescCode', str(time.time()))
            degree = data.get('Degree')
            identification = data.get('Identification')
            region = data.get('Region')
            position = data.get('Position')
            bas = data.get('Bas')
            pro_code = data.get('ProCode')
            tun_code = data.get('TunCode')
            work_sur_code = data.get('WorkSurCode')
            stru_code = data.get('StruCode')
            mileage = data.get('Mileage')
            equ_code = data.get('ConEquipCode')
            acq_code = data.get('DataAcqEquipCode')
            anomaly_time = data.get('AnomalyTime')
        except Exception as e:
            return {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {str(e)}}

        # 校验必填字段
        if not all(
                [desc_code, degree, region, position, bas, pro_code, tun_code, work_sur_code, stru_code, mileage,
                 equ_code, acq_code, anomaly_time, identification]):
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection()
            cursor = con.cursor()

            # 验证DescCode是否存在
            sql = "SELECT * From anomaly_log_desc WHERE DescCode = {}".format(f"'{desc_code}'")
            res = DBUtils.project_is_exist(cursor, sql, LogHttpStatus.NO_FIND_CODE.value, "不存在")
            if not res:
                return {'code': LogHttpStatus.EXIST_CODE.value, 'msg': '日志已经存在', 'data': {}}

            # 验证各个Code
            checks = [
                ('tunnel', 'TunCode', tun_code, ProjectHttpStatus.NO_FIND_CODE.value, "该隧道不存在"),
                ('project', 'ProCode', pro_code, ProjectHttpStatus.NO_FIND_CODE.value, "该项目不存在"),
                ('structure', 'StruCode', stru_code, ProjectHttpStatus.NO_FIND_CODE.value, "该结构物不存在"),
                ('work_surface', 'WorkSurCode', work_sur_code, ProjectHttpStatus.NO_FIND_CODE.value,
                 "该工作面不存在"),
                ('eq_control', 'ConEquipCode', equ_code, ProjectHttpStatus.NO_FIND_CODE.value, "该中控设备不存在"),
                ('eq_data', 'DataAcqEquipCode', acq_code, ProjectHttpStatus.NO_FIND_CODE.value,
                 "该数据采集器不存在"),
            ]
            for table, column, code, error_code, error_msg in checks:
                res = DBUtils.check_existence(cursor, table, column, code, error_code, error_msg)
                if res:
                    return res

            desc_sql = """
                INSERT INTO anomaly_log_desc 
                (DescCode, Identification, Degree, Region, Position, Bas) VALUES (%s, %s, %s, %s, %s, %s)
                """
            log_sql = """
                INSERT INTO 
                anomaly_log 
                (
                Identification, ProCode, TunCode, WorkSurCode, StruCode, Mileage, ConEquipCode, DataAcqEquipCode, 
                AnomalyTime, Year, Month, Day, Hour, Minute, Second
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

            anomaly_len = len(degree)
            if anomaly_len <= 0:
                return {'code': LogHttpStatus.NO_ANOMALY_DATA.value, 'msg': '添加失败', 'data': {}}
            if anomaly_len == 1:
                cursor.execute(desc_sql, (
                    desc_code, identification, str(degree[0]), str(region[0]), str(position[0]), str(bas[0])))
            else:
                for d, r, p, b in zip(degree, region, position, bas):
                    cursor.execute(desc_sql, (desc_code, identification, str(d), str(r), str(p), str(b)))
                    desc_code = str(float(desc_code) + 1)

            now = datetime.strptime(anomaly_time, '%Y-%m-%d %H:%M:%S')
            rows = cursor.execute(log_sql, (
                identification, pro_code, tun_code, work_sur_code, stru_code, mileage, equ_code, acq_code,
                anomaly_time, now.year, now.month, now.day, now.hour, now.minute, now.second))
            con.commit()
            return DBUtils.kv(rows, result_dict)
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '添加失败', 'data': {str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def get_log_by_columns(data: dict):
        try:
            filters = {
                "ProCode": data.get('ProCode', None),
                "TunCode": data.get('TunCode', None),
                "WorkSurCode": data.get('WorkSurCode', None),
                "StruCode": data.get('StruCode', None),
                "ConEquipCode": data.get('ConEquipCode', None),
                "DataAcqEquipCode": data.get('DataAcqEquipCode', None),
                "Year": data.get('Year', None),
                "Month": data.get('Month', None),
                "Day": data.get('Day', None),
                "Hour": data.get('Hour', None),
                "Minute": data.get('Minute', None),
                "Second": data.get('Second', None)
            }
        except Exception as e:
            return {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '检索失败', 'data': {str(e)}}

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()

            # 构建动态查询语句
            sql = "SELECT Identification, AnomalyTime FROM anomaly_log WHERE 1=1"
            params = []
            for field, value in filters.items():
                if value:
                    sql += f" AND {field} = %s"
                    params.append(value)
            cursor.execute(sql, params)
            items = cursor.fetchall()
            if not items:
                return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': {}}

            # TODO: 同时满足多个identification条件下的desc记录
            identifications = [item['Identification'] for item in items]
            placeholders = ', '.join(['%s'] * len(identifications))
            desc_sql = f"SELECT ID, Identification, Degree, Region, Position, Bas FROM anomaly_log_desc WHERE Identification IN ({placeholders})"
            cursor.execute(desc_sql, identifications)
            desc = cursor.fetchall()

            res = {
                "items": items,
                "total": len(items),
                "id": identifications,
                "desc": desc
            }
            # 返回结果
            return {'code': BaseHttpStatus.OK.value, 'msg': '检索成功', 'data': res}
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '检索失败', 'data': {str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def pcd_path2db(path, time: datetime, tunnel: Tunnel):
        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()
            acq_sql = "SELECT ConEquipCode, Distance FROM eq_data WHERE DataAcqEquipCode = %s"
            cursor.execute(acq_sql, tunnel.device_id)
            acq_res = cursor.fetchone()
            if not acq_res:
                return None

            con_sql = "SELECT * FROM eq_control WHERE ConEquipCode = %s"
            cursor.execute(con_sql, acq_res['ConEquipCode'])
            con_res = cursor.fetchone()
            if not con_res:
                return None

            str_time = time.strftime("%Y-%m-%d %H:%M:%S")
            sql = """
            INSERT INTO pcd_log 
            (ProCode, TunCode, WorkSurCode, StruCode, Mileage, ConEquipCode, DataAcqEquipCode, 
            AnomalyTime, Year, Month, Day, Hour, Minute, Second, Path) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                con_res['ProCode'], con_res['TunCode'], con_res['WorkSurCode'], con_res['StruCode'],
                acq_res['Distance'], con_res['ConEquipCode'], tunnel.device_id, str_time, time.year,
                time.month, time.day, time.hour, time.minute, time.second, str(os.path.abspath(path))))
            con.commit()
            return True
        except Exception as e:
            if con:
                con.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def get_path_in_db(data: dict):
        """
        如果不传递任何字段，则默认返回当前最新时间点的文件路径
        如果只传递了年月日三个字段的信息，则默认返当日最新的文件路径
        :param data:
        :return:
        """
        try:
            filters = {
                "Year": data.get('Year', None),
                "Month": data.get('Month', None),
                "Day": data.get('Day', None),
                "Hour": data.get('Hour', None),
                "Minute": data.get('Minute', None),
                "Second": data.get('Second', None)
            }
        except Exception as e:
            print(e)
            return None

        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()

            sql = "SELECT Path FROM pcd_log WHERE 1=1"
            params = []
            for k, v in filters.items():
                if v:
                    sql += f" AND {k} = %s"
                    params.append(v)
            cursor.execute(sql, params)
            res = cursor.fetchall()[-1]

            if not res:
                return None
            return res['Path']
        except Exception as e:
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)


if __name__ == '__main__':
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # print(current_dir)
    dbu = DBUtils()
    conn = dbu.connection('tunnel_project')

    # list1 = ['ProName']
    # tuple1 = tuple(list1)
    # res, status = DBUtils.select_table(conn, 'project', tuple1)
    # print("select")
    # print(type(res), res)
    # print(status)
    #
    insert = {
        'ProCode': '1009',
        'ProName': 'test3',
        'ProAddress': 'test3',
        'LinkMan': 'test3',
        'Phone': 'test3',
        'ProCreateTime': '2024-9-4 17:49:30',
        'ProStatus': '100'
    }
    # status = DBUtils.insert_table(conn, 'project', insert)
    # print("insert")
    # print(status)

    delete_condition = {
        'ProCode': '1006'
    }
    DBUtils.delete_table(conn, 'project', delete_condition)

    u_column = 'ProName'
    u_value = 'test_update'
    t_column = 'ProCode'
    t_value = '1007'
    # print(DBUtils.update_table(conn, 'project', u_column, u_value, t_column, t_value))
