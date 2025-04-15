"""
@Author: zhang_zhiyi
@Date: 2024/10/11_9:35
@FileName:pcd_file_op.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 点云数据操作路由 本地文件保存日志和点云数据
"""
import os.path
from flask import jsonify, request, Blueprint

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.pcdHttpStatus import PCDHttpStatus
from utils.util_pcd import get_path, get_history, show_log, data_visual, compare_data

pcd_file_op = Blueprint('pcd_file_op', __name__)

INIT_PATH = "data"
INIT_ALL_DATA_NAME = "init.csv"
INIT_REGIONS_NAME = "regions"


@pcd_file_op.route('/tree', methods=['POST'])
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
            return jsonify({'code': PCDHttpStatus.PARAMETER_ERROR.value, 'msg': 'parameter error', data: {}}), 200
        # 获取目录结构
        res_dict = get_path(data, INIT_PATH, 'log', 'tree')
        # res_dict[0]['config']
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '访问成功', 'data': res_dict}), 200
    except Exception as e:
        return jsonify({'code': PCDHttpStatus.EXCEPTION.value, 'msg': 'Exception, defeat', 'data': {'exception': str(e)}}), 200


@pcd_file_op.route('/history', methods=['POST'])
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
        path, data_path = get_path(data, INIT_PATH, 'history', 'history')
        if not os.path.exists(data_path):
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file', 'data': {}}), 200
        init_region_path = os.path.join(path, 'data', 'init', INIT_REGIONS_NAME)
        if not os.path.exists(init_region_path):
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file', 'data': {}}), 200
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
            return jsonify({'code': PCDHttpStatus.NO_FIND_DATA.value, 'msg': msg, 'data': {}}), 200
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '访问成功', 'data': {res}}), 200
    except Exception as e:
        return jsonify({'code': PCDHttpStatus.EXCEPTION.value, 'msg': 'Exception, defeat', 'data': {'exception': str(e)}}), 200


@pcd_file_op.route('/log', methods=['POST'])
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
        _, data_path = get_path(data, INIT_PATH, 'log', 'log')
        if not os.path.exists(data_path):
            return jsonify(
                {'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file get_path()', 'data': {}}), 200
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
            return jsonify(
                {'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file show_log()', 'data': {}}), 200
        # 获取分页相关字段
        page, count = data.get('page'), data.get('count')
        if page is None or count is None:
            return jsonify({'code': PCDHttpStatus.PARAMETER_ERROR.value, 'msg': 'Parameter error', 'data': {}}), 200
        # 分页
        start_index = (page - 1) * count
        end_index = page * count
        page_data = res[start_index: end_index]
        # 如果该索引下没有数据，返回错误消息
        if not page_data:
            return jsonify(
                {'code': PCDHttpStatus.NO_FIND_DATA.value, 'msg': 'no find log file page_data', 'data': {}}), 200
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
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '访问成功', 'data': {response_data}}), 200

    except Exception as e:
        return jsonify({'code': PCDHttpStatus.EXCEPTION.value, 'msg': 'Exception, defeat', 'data': {'exception': str(e)}}), 200


@pcd_file_op.route('/log_data_visual', methods=['POST'])
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
        path, data_path = get_path(data.get('tag'), INIT_PATH, 'history', 'log_data_visual')
        if not os.path.exists(data_path):
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file in get_path()',
                            'data': {}}), 200
        init_region_path = os.path.join(path, 'data', 'init', INIT_REGIONS_NAME)
        if not os.path.exists(init_region_path):
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file in get_path()',
                            'data': {}}), 200
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
            return jsonify({'code': PCDHttpStatus.NO_FIND_LOG_FILE.value, 'msg': 'no find log file in data_visual()',
                            'data': {}}), 200
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '访问成功', 'data': {res}}), 200

    except Exception as e:
        return jsonify({'code': PCDHttpStatus.EXCEPTION.value, 'msg': 'Exception, defeat', 'data': {'exception': str(e)}}), 200


@pcd_file_op.route('/compare', methods=['POST'])
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
        root_content, root_path = get_path(data.get('root'), INIT_PATH, 'history', 'compare')
        _, root_log_path = get_path(data.get('root'), INIT_PATH, 'log', 'compare')
        _, comparison_path = get_path(data.get('comparison'), INIT_PATH, 'history', 'compare')
        _, comparison_log_path = get_path(data.get('comparison'), INIT_PATH, 'log', 'compare')
        init_region_path = os.path.join(root_content, 'data', 'init', INIT_REGIONS_NAME)

        # 对比
        res = compare_data(init_region_path, root_path, comparison_path, root_log_path, comparison_log_path)
        msg = res.get('msg')
        if msg is not None:
            return jsonify({'code': PCDHttpStatus.NO_FIND_DATA.value, 'msg': msg, 'data': {}}), 200
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '访问成功', 'data': {res}}), 200

    except Exception as e:
        return jsonify({'code': PCDHttpStatus.EXCEPTION.value, 'msg': 'Exception, defeat', 'data': {'exception': str(e)}}), 200
