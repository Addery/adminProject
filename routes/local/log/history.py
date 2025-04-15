"""
@Author: zhang_zhiyi
@Date: 2025/4/15_15:10
@FileName:history.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 历史记录
"""
from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils
from utils.util_statistics import StUtils

history_db = Blueprint('history_db', __name__)


@history_db.route('/selectHistory', methods=['POST'])
def log_select():
    try:
        data = request.json
        res = DBUtils.paging_display(data, 'pcd_log', 1, 10)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/searchLogByColumn', methods=['POST'])
def log_search_by_column():
    try:
        data = request.json
        res = DBUtils.search_by_some_item('pcd_log', data.get('Item'), data.get('Value'), data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/viewPCD', methods=['POST'])
def view_pcd():
    try:
        data = request.json
        # TODO: 显示点云数据
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@history_db.route('/sectionFilter', methods=['POST'])
def section_filter():
    try:
        data = request.json
        column = data.get('column', None)
        if column is None:
            return jsonify(
                {'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200
        res = StUtils.section_filter('pcd_log', column, data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200