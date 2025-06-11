"""
@Author: zhang_zhiyi
@Date: 2025/5/6_17:43
@FileName:property.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 小程序端资产统计接口
"""
from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_statistics import StUtils

property_db = Blueprint('property_db', __name__)


@property_db.route('/getProjectAllCount', methods=['POST'])
def get_project_all_count():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        return jsonify(StUtils.get_table_record_count('project', item, value)), 200
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200


@property_db.route('/getTunnelAllCount', methods=['POST'])
def get_tunnel_all_count():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        return jsonify(StUtils.get_table_record_count('tunnel', item, value)), 200
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200


@property_db.route('/getAviaAllCount', methods=['POST'])
def get_avia_all_count():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        return jsonify(StUtils.get_table_record_count('eq_data', item, value)), 200
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200


@property_db.route('/getControlAllCount', methods=['POST'])
def get_control_all_count():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        return jsonify(StUtils.get_table_record_count('eq_control', item, value)), 200
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200


@property_db.route('/getAllCount', methods=['POST'])
def get_all_count():
    try:
        data = request.json
        item = data.get('Item')
        value = data.get('Value')
        eq_control = StUtils.get_table_record_count('eq_control', item, value)
        eq_data = StUtils.get_table_record_count('eq_data', item, value)
        tunnel = StUtils.get_table_record_count('tunnel', item, value)
        project = StUtils.get_table_record_count('project', item, value)
        if eq_control.get('code') == 101 and eq_data.get('code') == 101 and tunnel.get('code') == 101 and project.get('code') == 101:
            return jsonify(
                {
                    'code': BaseHttpStatus.OK.value,
                    'msg': '统计成功',
                    'data': {
                        'project': project.get('data').get('count'),
                        'tunnel': tunnel.get('data').get('count'),
                        'eq_control': eq_control.get('data').get('count'),
                        'eq_data': eq_data.get('data').get('count')
                    }
                }
            ), 200

        return jsonify({'code': BaseHttpStatus.ERROR.value, 'msg': '统计失败', 'data': {}})
    except Exception as e:
        return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200


# @property_db.route('/getAllCountByJoin', methods=['POST'])
# def get_all_count_by_join():
#     try:
#         data = request.json
#         item = data.get('Item')
#         value = data.get('Value')
#         return jsonify(StUtils.get_batch_table_record_count(item, value)), 200
#     except Exception as e:
#         return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '统计失败', 'data': {'exception': str(e)}}, 200

