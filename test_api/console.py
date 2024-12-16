"""
@Author: zhang_zhiyi
@Date: 2024/10/18_15:27
@FileName:console.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-中控设备表相关
"""
import requests


def console_add():
    """
    添加中控设备
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/console_db/addConsole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1005",
        "ConEquipName": "e_name",
        "ConEquipIP": "localhost",
        "ProCode": "1005",
        "TunCode": "1006",
        "WorkSurCode": "1002",
        "StruCode": "1003",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_delete():
    """
    删除
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/console_db/deleteConsole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1005",
        "WorkSurCode": "1004"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_update():
    """
    更新
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/console_db/updateConsole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "WorkSurCode": "1003",
        "ConEquipCode": "1006",
        "ConEquipName": "name",
        "ConEquipIP": "1002",
        "TunCode": "1006",
        "ProCode": "1003",
        "StruCode": "1003",
        "OldConEquipCode": "1005",
        "OldWorkSurCode": "1002"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_select():
    """
    获取信息
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/console_db/selectConsole"
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


def console_info_search_by_column():
    url = "http://127.0.0.1:8023/api/outer/console_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ConEquipCode',
        'value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # console_add()
    # console_delete()
    console_update()
    # console_select()
    # console_info_search_by_column()
