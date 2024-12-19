"""
@Author: zhang_zhiyi
@Date: 2024/10/18_10:09
@FileName:structure.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-结构物表相关
"""

import requests


ip = "http://127.0.0.1"
port = "5000"


def structure_add():
    """
    添加结构物
    :return:
    """
    url = f"{ip}:{port}/api/outer/structure_db/addStructure"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "StruCode": "1002",
        "StruName": "default",
        "FirWarningLevel": "0.008",
        "SecWarningLevel": "0.02",
        "ThirWarningLevel": "0.04"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def structure_delete():
    """
    删除结构物
    :return:
    """
    url = f"{ip}:{port}/api/outer/structure_db/deleteStructure"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "StruCode": "1003"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def structure_update():
    """
    删除结构物
    :return:
    """
    url = f"{ip}:{port}/api/outer/structure_db/updateStructure"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "OldStruCode": "1002",
        "StruCode": "1002",
        "StruName": "default",
        "FirWarningLevel": "2",
        "SecWarningLevel": "4",
        "ThirWarningLevel": "6"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def structure_select():
    """
    隧道信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/structure_db/selectStructure"
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


def structure_info_search_by_column():
    url = f"{ip}:{port}/api/outer/structure_db/searchStructureByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'StruCode',
        'value': '1002'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # structure_add()
    # structure_delete()
    # structure_update()
    # structure_select()
    structure_info_search_by_column()
