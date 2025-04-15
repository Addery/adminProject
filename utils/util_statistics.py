"""
@Author: zhang_zhiyi
@Date: 2025/4/9_14:43
@FileName:util_statistics.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime
from collections import Counter

from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils


class StUtils(object):
    """
    数据统计计算工具类
    """

    @staticmethod
    def eq_status(table, column):
        """
        统计设备状态
        """
        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()

            # 查找设备表中状态字段数据
            sql = f"SELECT {column} FROM {table}"
            cursor.execute(sql)
            res = cursor.fetchall()
            # 分状态统计
            status_list = [item[column] for item in res]
            counter = Counter(status_list)
            # 返回结果
            return {
                "total": len(res),
                "off_line": counter.get(0),  # 0: 离线
                "on_line": counter.get(1),  # 1: 在线
                "fault": counter.get(2),  # 2: 故障
                'code': BaseHttpStatus.OK.value,
                'msg': '成功'
            }
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def pro_status(create_times, pro_cycles):
        """
        统计项目状态
        项目状态：0表示施工中，1表示即将竣工，2表示已竣工，3表示未开工
        TODO:
            建立时间 + 工程周期 = 结束时间
            结束时间 - 当前时间 = 时间差
            时间差 <= 0 已竣工,
            时间差 < 0 施工中, -3 <= 时间差 < 0 即将竣工

        :create_time: 建立时间
        :pro_cycle: 工程周期
        """
        not_start, proceeding, near_completion, completed = 0, 0, 0, 0
        count = 0
        now_time = datetime.datetime.now()  # 当前时间
        for time, cycle in zip(create_times, pro_cycles):
            count += 1
            end_time = time + datetime.timedelta(days=cycle)  # 项目理论竣工时间
            bas_time = end_time - now_time  # 距离理论竣工时间的剩余时间

            if (time - now_time).days > 0:
                not_start += 1  # 未开工
                continue

            if bas_time.days < 0:
                completed += 1  # 已竣工
            else:
                if bas_time.days <= 3:
                    near_completion += 1  # 即将竣工
                    continue
                proceeding += 1  # 施工中
        return {
            "total": count,  # 合计
            "not_start": not_start,  # 未开工
            "proceeding": proceeding,  # 施工中
            "near_completion": near_completion,  # 即将竣工
            "completed": completed,  # 已竣工
            'code': BaseHttpStatus.OK.value,
            'msg': '成功'
        }

    @staticmethod
    def get_time_and_cycle_from_table(table, time_column, cycle_column):
        """
        获取表中的 create_time 和 cycle
        """
        create_times, pro_cycles = [], []
        con = None
        cursor = None
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()

            sql = f"SELECT {time_column}, {cycle_column} FROM {table}"
            cursor.execute(sql)
            res = cursor.fetchall()

            for item in res:
                create_times.append(item.get(time_column))
                pro_cycles.append(item.get(cycle_column))

            return StUtils.pro_status(create_times, pro_cycles)
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)

    @staticmethod
    def section_filter(table, column, data):
        """
        根据区间筛选
        """
        try:
            start = data.get('start')
            end = data.get('end')
        except Exception as e:
            return {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '筛选失败', 'data': {'exception': str(e)}}

        # 校验必填字段
        if not all([start, end]):  # 校验必填字段
            return {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}

        and_list = ['AnomalyTime', 'Mileage']
        con = None
        cursor = None
        sql = ''
        try:
            dbu = DBUtils()
            con = dbu.connection(cursor_class=DictCursor)
            cursor = con.cursor()
            if column in and_list:
                sql = f"SELECT * FROM {table} WHERE {column} BETWEEN '{start}' AND '{end}'"
                print(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            return {
                    'items': res,
                    'total': len(res),
                    'code': BaseHttpStatus.OK.value,
                    'msg': '成功'
                }
        except Exception as e:
            if con:
                con.rollback()
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}
        finally:
            if cursor:
                cursor.close()
            if con:
                DBUtils.close_connection(con)


if __name__ == '__main__':
    # times = [
    #     datetime.datetime(2025, 3, 16, 16, 29, 43, 79043),
    #     datetime.datetime(2025, 4, 10, 16, 29, 43, 79043),
    #     datetime.datetime(2025, 4, 17, 16, 29, 43, 79043),
    #     datetime.datetime(2025, 3, 18, 16, 29, 43, 79043),
    # ]
    # cycles = [60, 60, 60, 60]
    # print(StUtils.pro_status(times, cycles))

    # table = "tunnel"
    # time_column = "TunCreateTime"
    # cycle_column = "TunCycle"
    # print(StUtils.get_time_and_cycle_from_table(table, time_column, cycle_column))
    # StUtils.section_filter('pcd_log', 'Mileage', '60', '70')
    start_time = datetime.datetime(2025, 4, 1, 0, 0, 0)
    end_time = datetime.datetime(2025, 5, 1, 0, 0, 0)
    data = {
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    print(StUtils.section_filter('pcd_log', 'AnomalyTime', data))
