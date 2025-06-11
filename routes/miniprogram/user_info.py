"""
@Author: zhang_zhiyi
@Date: 2025/5/13_9:49
@FileName:user_info.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 小程序获取用户信息
"""
import json

import requests

from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from routes.local.status_code.userHttpStatus import UserHttpStatus
from utils.util_database import DBUtils

info_db = Blueprint('info_db', __name__)

# 隧道安全小程序
APPID = 'wx6d9fb84f565be54e'
SECRET = 'bbb58a1b3306d56fe0d2c77710196a7e'
# &
URL_START = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code='
URL_END = 'grant_type=authorization_code'


@info_db.route('/getMinProUserInfo', methods=['POST'])
def get_user_info():
    try:
        data = request.json
        code = data.get('Code')
        phone = data.get('Phone')
    except Exception as e:
        return jsonify(
            {'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '添加失败', 'data': {'exception': str(e)}}), 200

    if not all([code, phone]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection()
        cursor = con.cursor()
        con.autocommit(False)

        # 访问微信接口获取小程序用户openid和unionid
        url = f"{URL_START}{code}&{URL_END}"
        response = requests.get(url).json()
        openid = response.get('openid')
        unionid = response.get('unionid')

        # 判断 phone 是否在 user 表中
        phone_exist_sql = "SELECT * From user WHERE Phone = {}".format(f"'{phone}'")
        res = DBUtils.project_is_exist(cursor, phone_exist_sql, UserHttpStatus.NO_USER.value, "用户不存在")
        if res:
            return jsonify(res), 200

        # 更新 user 表中 MiniProOpenID 和 UnionID
        update_sql = """
            UPDATE 
                user
            SET 
                MiniProOpenID=%s, UnionID=%s
            WHERE
                Phone=%s
        """
        rows = cursor.execute(update_sql, (openid, unionid, phone))
        if rows != 1:
            return jsonify(
                {"code": BaseHttpStatus.ERROR.value, "msg": "失败", "data": {}}), 200

        con.commit()
        return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '成功', 'data': {}}), 200
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({"code": BaseHttpStatus.EXCEPTION.value, "msg": "失败", "data": {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)



