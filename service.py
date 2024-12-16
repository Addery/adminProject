"""
@Author: zhang_zhiyi
@Date: 2024/7/24_11:45
@FileName:service.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 本地外部接口
"""
import os.path
import traceback

import pandas as pd
from flask import Flask, jsonify, request

from outer.utils.util_database import DBUtils
from outer.routes.local.status_code.userHttpStatus import HttpStatus
from outer.utils.util_pcd import write_df2pcd, get_path, get_history, show_log, data_visual, compare_data
from deprecated import deprecated

app = Flask(__name__)

# RECEIVE_DEFAULT_SAVE_PATH = "../data/history"
# COMPARE_DEFAULT_SAVE_PATH = "../data/compare"
# PICTURE_DEFAULT_SAVE_PATH = "../data/picture"
# LOG_DEFAULT_SAVE_PATH = "../data/log"
# INIT_DEFAULT_SAVE_PATH = "../data/init"
INIT_PATH = "data"
INIT_ALL_DATA_NAME = "init.csv"
INIT_REGIONS_NAME = "regions"

# app.config['PATH'] = RECEIVE_DEFAULT_SAVE_PATH
# app.config['COMPARE'] = COMPARE_DEFAULT_SAVE_PATH
# app.config['PICTURE'] = PICTURE_DEFAULT_SAVE_PATH
# app.config['LOG'] = LOG_DEFAULT_SAVE_PATH
# app.config['INIT'] = INIT_DEFAULT_SAVE_PATH
app.config['PATH'] = INIT_PATH
app.config['INIT_NAME'] = INIT_ALL_DATA_NAME
app.config['INIT_REGIONS'] = INIT_REGIONS_NAME


@deprecated(reason="Use ./config.ini/receive")
@app.route('/outer/service/receive', methods=['POST'])
def receive():
    try:
        time = request.headers.get('time')
        data = request.json
        df_list = [pd.DataFrame.from_dict(df) for df in data['dataframes']]
        write_df2pcd(time, app.config['PATH'], df_list)
        return jsonify({'config': 'success'}), HttpStatus.OK.value

    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify({'msg': 'defeat'}), HttpStatus.ERROR.value


@app.route('/outer/service/tree', methods=['POST'])
def tree():
    try:
        """
        参数：项目信息、年月日
        config = {
            'project_name':,
            'tunnel_name':,
            'working_face':
            'mileage':,
            'device_id':,
            'year': ,
            'month': ,
            'day': 
        }
        """
        data = request.json
        """
            异常情况: response.status_code=HttpStatus.ERROR.value 401
            res_dict = {
                'msg': '' 
            }
            正常情况: response.status_code=HttpStatus.OK.value 200
            res_dict = {
                'config': ['12:14:17', '12:23:14', '12:05:46', '13:09:54', ...]
            }
        """
        if len(data.keys()) != 8:
            return jsonify({'msg': 'parameter error'}), HttpStatus.PARAMETER_ERROR.value

        # 获取目录结构
        res_dict = get_path(data, app.config['PATH'], 'log', 'tree')
        return jsonify(res_dict), HttpStatus.OK.value

    except Exception as e:
        print(f"{str(e)}: a error in tree")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value


@app.route('/outer/service/history', methods=['POST'])
def history():
    try:
        """
        config = {
            'project_name':,
            'tunnel_name':,
            'working_face':
            'mileage':,
            'device_id':,
            'year': ,
            'month': ,
            'day': ,
            'hour': .
            'minute': 
        }
        """
        # 最小到分
        data = request.json
        # 获取目录路径
        path, data_path = get_path(data, app.config['PATH'], 'history', 'history')
        if not os.path.exists(data_path):
            return jsonify({'msg': 'no find log file'}), HttpStatus.NO_FIND_FILE_ERROR.value
        init_region_path = os.path.join(path, 'data', 'init', app.config['INIT_REGIONS'])
        if not os.path.exists(init_region_path):
            return jsonify({'msg': 'no find log file'}), HttpStatus.NO_FIND_FILE_ERROR.value
        """
            异常情况: response.status_code=HttpStatus.ERROR.value 401
            res = {
                'msg': '' 
            }
            正常情况: response.status_code=HttpStatus.OK.value 200
            res = {
                'xyz': [x, y, z, x, y, z, x, y, z, ...],
                'rgb': [r, g, b, r ,g ,b, r, g ,b, ...] 
            }
        """
        # 获取结果
        res = get_history(data_path, init_region_path)
        msg = res.get('msg')
        if msg is not None:
            return jsonify({'msg': msg}), HttpStatus.ERROR.value
        return jsonify(res), HttpStatus.OK.value

    except Exception as e:
        print(f"{str(e)}: a error in history")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value


@app.route('/outer/service/log', methods=['POST'])
def log():
    """
    日志接口
    :return:
    """
    try:
        """
        固定字段：year、month、day、page、count
        config = {
            'date':{
                'project_name':,
                'tunnel_name':,
                'working_face':
                'mileage':,
                'device_id':,
                'year': ,
                'month': ,
                'day': ,
                'page': ,
                'count': 
            }
        }
        """
        data = request.json
        # 获取目录路径
        _, data_path = get_path(data, app.config['PATH'], 'log', 'log')
        if not os.path.exists(data_path):
            return jsonify({'msg': 'no find log file get_path()'}), HttpStatus.NO_FIND_FILE_ERROR.value
        """
        全部日志
        res = [
            {
                'time': ,
                'degree': ,
                'message': [str],
                'index': [int],
                'tag': {} 
            },
            ...
        ]
        """
        res = show_log(data_path)
        if res is None:
            return jsonify({'msg': 'no find log file show_log()'}), HttpStatus.NO_FIND_FILE_ERROR.value
        # 获取分页相关字段
        page, count = data.get('page'), data.get('count')
        if page is None or count is None:
            return jsonify({'msg': 'Parameter error'}), HttpStatus.PARAMETER_ERROR.value
        # 分页
        start_index = (page - 1) * count
        end_index = page * count
        page_data = res[start_index: end_index]
        # 如果该索引下没有数据，返回错误消息
        if not page_data:
            return jsonify({'msg': 'no find log file page_data'}), HttpStatus.NO_FIND_FILE_ERROR.value
        """
        分页后的日志
        异常情况: response.status_code=HttpStatus.ERROR.value 401
        {
            'msg': '' 
        }
        正常情况: response.status_code=HttpStatus.OK.value 200
        response_data = [
            total,
            [
                {
                    'time': ,
                    'degree': ,
                    'message': [str],
                    'index': [int],
                    'tag': {} 
                },
                ...
            ]
        ]
        如：[3, [{}, {}, {}]]
        index和tag字段传入http://127.0.0.1//outer/service/log_data_visual路由，用于显示异常点云数据
        """
        res_data = [
            {
                'time': e[0],
                'degree': e[1],
                'message': e[2],
                'index': e[3],
                'tag': e[4]
            }
            for e in page_data
        ]
        response_data = [len(res), res_data]
        return jsonify(response_data), HttpStatus.OK.value

    except Exception as e:
        print(f"{str(e)}: a error in log")
        traceback.print_exc()  # 打印堆栈信息
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value


@app.route('/outer/service/log_data_visual', methods=['POST'])
def log_data_visual():
    """
    获取日志异常点云数据接口
    :return:
    """
    try:
        """
        config = {
            'index': [int],
            'tag': {项目信息+年月日时分} 
        }
        """
        data = request.json

        # 获取数据所在目录路径
        path, data_path = get_path(data.get('tag'), app.config['PATH'], 'history', 'log_data_visual')
        if not os.path.exists(data_path):
            return jsonify({'msg': 'no find log file in get_path()'}), HttpStatus.NO_FIND_FILE_ERROR.value
        init_region_path = os.path.join(path, 'data', 'init', app.config['INIT_REGIONS'])
        if not os.path.exists(init_region_path):
            return jsonify({'msg': 'no find log file in get_path()'}), HttpStatus.NO_FIND_FILE_ERROR.value
        """
        异常情况: response.status_code=HttpStatus.ERROR.value 401
        res = {
            'msg': '' 
        }
        正常情况: response.status_code=HttpStatus.OK.value 200
        res = {
            'xyz': [x, y, z, x, y, z, x, y, z, ...],
            'rgb': [r, g, b, r ,g ,b, r, g ,b, ...] 
        }
        """
        # 查询数据
        res = data_visual(data_path, init_region_path)
        if res is None:
            return jsonify({'msg': 'no find log file in data_visual()'}), HttpStatus.NO_FIND_FILE_ERROR.value
        return jsonify(res), HttpStatus.OK.value

    except Exception as e:
        print(f"{str(e)}: a error in log_data_visual")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value


@app.route('/outer/service/compare', methods=['POST'])
def compare():
    """
    对比接口
        1.以第一个时间点的数据为基准
        2.找出第二个时间点中不同的异常区域
        3.将两者之间相同的异常区域通过日志信息进行比对
        4.用后者不同于前者或者差距较大的数据替换前者中的数据
    :return:
    """
    try:
        """
        config = {
            root = {
                'project_name':,
                'tunnel_name':,
                'working_face':
                'mileage':,
                'device_id':,
                'year': ,
                'month': ,
                'day': ,
                'hour': ,
                'minute': ,
            },
            comparison = {
                'project_name':,
                'tunnel_name':,
                'working_face':
                'mileage':,
                'device_id':,
                'year': ,
                'month': ,
                'day': ,
                'hour': ,
                'minute': ,
            }
        }
        """
        data = request.json

        # 构造路径
        root_content, root_path = get_path(data.get('root'), app.config['PATH'], 'history', 'compare')
        _, root_log_path = get_path(data.get('root'), app.config['PATH'], 'log', 'compare')
        _, comparison_path = get_path(data.get('comparison'), app.config['PATH'], 'history', 'compare')
        _, comparison_log_path = get_path(data.get('comparison'), app.config['PATH'], 'log', 'compare')
        init_region_path = os.path.join(root_content, 'data', 'init', app.config['INIT_REGIONS'])

        # 对比
        res = compare_data(init_region_path, root_path, comparison_path, root_log_path, comparison_log_path)
        msg = res.get('msg')
        if msg is not None:
            return jsonify({'msg': msg}), HttpStatus.NO_FIND_FILE_ERROR.value
        return jsonify(res), HttpStatus.OK.value

    except Exception as e:
        print(f"{str(e)}: a error in compare")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value


@app.route("/api/any_table/select", methods=['POST'])
def select_from_any_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'table_columns': [table_column1, table_column2, table_column3, ...]
        }
        如果table_columns为空列表，则默认执行select * from table_name，返回全部数据
        """
        data = request.json
        database_name = data.get('database_name')
        table_name, table_columns = data.get('table_name'), tuple(data.get('table_columns'))
        dbu = DBUtils()
        con = dbu.connection(database_name)
        res, status = DBUtils.select_table(con, table_name, table_columns)
        if res is None:
            return jsonify({'msg': 'database select error'}), status
        return jsonify(list(res)), status
    except Exception as e:
        print(f"{e}, a error in api/any_table/select")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value
    finally:
        if con:
            DBUtils.close_connection(con)


@app.route("/api/any_table/insert", methods=['POST'])
def insert_into_any_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'insert_data': {
                'column1': 'value1',
                'column2': 'value2',
                'column3': 'value3',
                ...
            }
        }
        """
        data = request.json
        database_name, table_name = data.get('database_name'), data.get('table_name')
        insert_data = data.get('insert_data')
        dbu = DBUtils()
        con = dbu.connection(database_name)
        status = DBUtils.insert_table(con, table_name, insert_data)
        return jsonify({}), status
    except Exception as e:
        print(f"{e}, a error in /api/any_table/insert")
        return jsonify({'msg': 'Exception, defeat'}), HttpStatus.ERROR.value
    finally:
        if con:
            DBUtils.close_connection(con)


@app.route('/api/any_table/delete', methods=['POST'])
def delete_any_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'delete_condition': {
                'column': 'value'
            }
        }
        如果没有delete_condition字段，则默认执行delete from table_name，删除全部数据
        """
        data = request.json
        database_name, table_name = data.get('database_name'), data.get('table_name')
        delete_condition = data.get('delete_condition')
        dbu = DBUtils()
        con = dbu.connection(database_name)
        res, status = DBUtils.delete_table(con, table_name, delete_condition)
        return jsonify({}), status
    except Exception as e:
        print(f"{e}, a error in /api/any_table/delete")
    finally:
        if con:
            DBUtils.close_connection(con)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8024, debug=True)
