"""
@Author: zhang_zhiyi
@Date: 2024/10/17_18:37
@FileName:work_surface.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-工作面表相关
"""
import requests


ip = "http://192.168.1.8"
port = "8023"


def work_surface_add():
    """
    添加隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/work_surface_db/addWorkSur"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1001",
        "ProCode": "1002",
        "StruCode": "1001",
        "WorkSurCode": "1010",
        "WorkSurName": "test",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def work_surface_delete():
    """
    删除隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/work_surface_db/deleteWorkSur"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1004",
        "WorkSurCode": "1005"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def work_surface_update():
    """
    删除隧道
    :return:
    """
    url = f"{ip}:{port}/api/outer/work_surface_db/updateWorkSur"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "TunCode": "1003",
        "ProCode": "1001",
        "StruCode": "1001",
        "WorkSurName": "name",
        "WorkSurCode": "1001",
        "OldWorkSurCode": "1001",
        "OldTunCode": "1001"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def work_surface_select():
    """
    隧道信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/work_surface_db/selectWorkSur"
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


def work_surface_info_search_by_column():
    url = f"{ip}:{port}/api/outer/work_surface_db/searchWorkSurByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'WorkSurCode',
        'value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    work_surface_add()
    # work_surface_delete()
    # work_surface_update()
    # work_surface_select()
    # work_surface_info_search_by_column()
