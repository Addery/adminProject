"""
@Author: zhang_zhiyi
@Date: 2025/4/18_15:52
@FileName:file.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
from flask import Blueprint, jsonify, request

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils

config_file_db = Blueprint('config_file_db', __name__)


@config_file_db.route('/update_file', methods=['POST'])
def update_file():
    content = request.form.get('content')
    with open('target.txt', 'a', encoding='utf-8') as f:
        f.write(content)
    return 'Update successful'


