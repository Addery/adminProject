"""
@Author: zhang_zhiyi
@Date: 2025/6/11_17:35
@FileName:wx.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 微信公众号推送相关
"""
import ast
import datetime
import json
import time
import uuid

import requests
from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils
from utils.util_push import PushUtils

wx_db = Blueprint('wx_db', __name__)


@wx_db.route('/getAccessToken', methods=['POST'])
def get_access_token():
    """
    获取 access token
    :return:
    """
    try:
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'. \
            format(PushUtils.APPID, PushUtils.APPSECRET)
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers)
        print("微信响应状态码：", response.status_code)
        print("微信响应内容：", response.text)

        # 安全地尝试解析 JSON
        try:
            result = response.json()
        except Exception as e:
            return jsonify(
                {
                    'code': BaseHttpStatus.EXCEPTION.value,
                    'msg': '响应不是合法 JSON',
                    'data': str(e)
                }
            ), 200

        access_token = result.get('access_token')
        if access_token:
            return jsonify(
                {
                    'code': BaseHttpStatus.OK.value,
                    'msg': '获取成功',
                    'data': access_token
                }
            ), 200
        else:
            return jsonify(
                {
                    'code': BaseHttpStatus.ERROR.value,
                    'msg': result.get('errmsg', '获取失败'),
                    'data': result
                }
            ), 200

    except Exception as e:
        return jsonify(
            {
                'code': BaseHttpStatus.EXCEPTION.value,
                'msg': '请求失败',
                'data': str(e)
            }
        ), 200


@wx_db.route('/sendMSG', methods=['POST'])
def sendmsg():
    """
    给所有用户发送消息
    """
    try:
        data = request.json
        info = data.get('Info', None)
        open_ids = data.get('OpenIDS', None)
        access_token = data.get('AccessToken', None)

        if not all([info, open_ids, access_token]):
            return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

        # 校验字段
        if not isinstance(info, dict):
            try:
                info = json.loads(info)
            except Exception as e:
                return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': 'info字段格式错误', 'data': str(e)}), 200

        if not isinstance(open_ids, list) or not open_ids:
            return jsonify({'code': BaseHttpStatus.ERROR.value, 'msg': 'open_ids 不是有效列表', 'data': {}}), 200

        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
        now = info.get('now')
        now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        data = {
            "time2": {
                "value": f"{now.year}年{now.month}月{now.day}日 {now.hour}:{now.minute}:{now.second}",
            },
            "phrase9": {
                "value": info.get('degree'),
            },
            "thing11": {
                "value": info.get('describe'),
            },
            "thing66": {
                "value": info.get('region'),
            }
        }

        count = 0
        for open_id in open_ids:
            body = PushUtils.build_request_body(open_id, data, info.get('Identification'))
            send_data = json.dumps(body, ensure_ascii=False).encode('utf-8')
            response = requests.post(url, data=send_data)
            try:
                result = response.json()
            except Exception:
                continue  # 或者记录日志

            if result.get('errcode') == 0:
                count += 1

        if count == len(open_ids):  # 判断是否所有有效用户都已成功接收到推送
            return jsonify(
                {
                    'code': BaseHttpStatus.OK.value,
                    'msg': '推送成功',
                    'data': {}
                }
            ), 200
        else:
            return jsonify(
                {
                    'code': BaseHttpStatus.ERROR.value,
                    'msg': '推送失败',
                    'data': "可能存在部分用户未接收到推送的情况"
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                'code': BaseHttpStatus.EXCEPTION.value,
                'msg': '推送失败',
                'data': str(e)
            }
        ), 200
