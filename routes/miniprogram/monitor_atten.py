"""
@Author: zhang_zhiyi
@Date: 2025/5/14_11:49
@FileName:monitor_atten.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 监听微信公众号新关注
"""
import datetime
import json

import requests

from flask import jsonify, request, Blueprint
from routes.local.status_code.baseHttpStatus import BaseHttpStatus

monitor_db = Blueprint('monitor_db', __name__)

TOKEN = "jovysoftweigh"  # 和微信后台填写的一致


@monitor_db.route("/wechatMonitor", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        pass

    if request.method == "POST":
        xml_data = request.data.decode("utf-8")
        if "<Event><![CDATA[subscribe]]></Event>" in xml_data:
            # 可以用 xml 解析库提取 openid 等字段
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"{current_time} 有新用户关注公众号！\n"
            with open("subscribe_log.txt", "a", encoding="utf-8") as f:
                f.write(log_message)
            # 可以写入数据库、发送欢迎消息等

        return 'success'  # 必须返回 success，否则微信会多次重试
