"""
@Author: zhang_zhiyi
@Date: 2024/10/17_17:28
@FileName:tunnel.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-隧道表相关
"""
import requests


ip = "http://127.0.0.1"
port = "5000"


def tunnel_add():
    """
    添加隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/tunnel_db/addTunnel"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1007",
        "TunName": "name",
        "LinkMan": "link",
        "Phone": "12346",
        "ProCode": "1004",
        "High": '8'
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
        "TunCode": "1007",
        "ProCode": "1002",
        "LinkMan": "123",
        "Phone": "123456",
        "TunName": "name",
        "High": "6",
        "OldTunCode": "1006",
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


if __name__ == "__main__":
    # tunnel_add()
    # tunnel_delete()
    # tunnel_update()
    # tunnel_select()
    tunnel_info_search_by_column()
