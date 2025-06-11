"""
@Author: zhang_zhiyi
@Date: 2025/4/21_15:23
@FileName:warn.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime
import time

import cv2
import requests

from utils.util_picture import IMGUtils

ip = "http://192.168.1.5"
# ip = "https://sat.jovysoft.net"
# ip = "https://172.25.107.170"
port = "8023"
# port = "8024"


def log_select():
    """
    获取信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/mp_warn_db/selectWarn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Page': 1,
        'PageSize': 10
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def search_warn():
    url = f"{ip}:{port}/api/outer/mp_warn_db/searchWarn"
    # url = "https://sat.jovysoft.net:8023/api/outer/mp_warn_db/searchWarnByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Identification': '1001',
    }
    response = requests.post(url, json=data, headers=headers)
    # res = response.json()
    # item = res.get('data').get('items')[0]
    # avia = IMGUtils.base642image(item.get('AviaPicturePath'))
    # camera = IMGUtils.base642image(item.get('CameraPicturePath'))
    # cv2.imwrite("avia.png", avia)
    # cv2.imwrite("camera.png", camera)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # log_select()
    search_warn()
