"""
@Author: zhang_zhiyi
@Date: 2024/10/17_17:28
@FileName:tunnel.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-隧道表相关
"""
import datetime
import time

import requests

# ip = "http://192.168.1.8"
ip = "https://sat.jovysoft.net"
port = "8023"


def tunnel_add():
    """
    添加隧道
    :return:
    """
    now = datetime.datetime.now()
    url = f"{ip}:{port}/api/outer/tunnel_db/addTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1007",
        "TunName": "测试隧道_1007",
        "LinkMan": "小明",
        "Phone": "13905236569",
        "ProCode": "1002",
        "High": '8',
        "TunCycle": '240',
        "TunCreateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Length": 5000
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_delete():
    """
    删除隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/tunnel_db/deleteTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1007",
        "ProCode": "1004"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_update():
    """
    删除隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/tunnel_db/updateTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    now = datetime.datetime.now()
    data = {
        "TunCode": "1007",
        "ProCode": "1002",
        "LinkMan": "测试管理员",
        "Phone": "18886666999",
        "TunName": "测试隧道_1007",
        "High": "8",
        "OldTunCode": "1007",
        "OldProCode": "1002",
        "TunCreateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "CurAdvancement": 100.0,
        "CompanyCode": "07361dfa-defc-4a08-ba11-5a495db9e565"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_select():
    """
    隧道信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/tunnel_db/selectTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Page': 1,
        'PageSize': 10
        # 'Item': 'ProCode',
        # 'Value': '1002'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_info_search_by_column():
    url = f"{ip}:{port}/api/outer/tunnel_db/searchTunnelByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'TunCode',
        'Value': '1003'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_status():
    url = f"{ip}:{port}/api/outer/tunnel_db/statisticsStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_exchange_name():
    url = f"{ip}:{port}/api/outer/tunnel_db/getExchangeName2Web"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1001"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # tunnel_add()
    # tunnel_delete()
    # tunnel_update()
    # start = time.time()
    # tunnel_select()
    # print(time.time() - start)
    # tunnel_info_search_by_column()
    # tunnel_status()
    get_exchange_name()
