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

import requests


ip = "http://192.168.1.3"
port = "8023"


def tunnel_add():
    """
    添加隧道
    :return:
    """
    time_data = datetime.datetime(2025, 3, 28, 16, 29, 43, 79043)
    url = f"{ip}:{port}/api/outer/tunnel_db/addTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1011",
        "TunName": "name",
        "LinkMan": "link",
        "Phone": "12346",
        "ProCode": "1004",
        "High": '8',
        "TunCycle": '60',
        "TunCreateTime": time_data.strftime("%Y-%m-%d %H:%M:%S")
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
    data = {
        "TunCode": "1009",
        "ProCode": "1002",
        "LinkMan": "123",
        "Phone": "123456",
        "TunName": "name",
        "High": "6",
        "OldTunCode": "1008",
        "OldProCode": "1004"
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
        'item': 'TunCode',
        'value': '1003'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def tunnel_status():
    url = f"{ip}:{port}/api/outer/tunnel_db/statisticsStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # tunnel_add()
    # tunnel_delete()
    # tunnel_update()
    # tunnel_select()
    # tunnel_info_search_by_column()
    tunnel_status()
