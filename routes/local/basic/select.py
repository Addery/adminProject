"""
@Author: zhang_zhiyi
@Date: 2024/12/25_15:15
@FileName:select.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
from flask import Blueprint, jsonify, request

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils

base_select_db = Blueprint('base_select_db', __name__)


@base_select_db.route('/selectSome', methods=['Post'])
def select_some():
    """
    在某个表中获取某些字段的值
    """
    try:
        data = request.json
        res = DBUtils.search(data)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200

