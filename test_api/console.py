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


ip = "http://127.0.0.1"
port = "5000"


def console_add():
    """
    添加中控设备
    :return:
    """
    url = f"{ip}:{port}/api/outer/console_db/addConsole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1001",
        "ConEquipName": "e_name",
        "ConEquipIP": "localhost",
        "ProCode": "1001",
        "TunCode": "1001",
        "WorkSurCode": "1001",
        "StruCode": "1001",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_delete():
    """
    删除
    :return:
    """
    url = f"{ip}:{port}/api/outer/console_db/deleteConsole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1005",
        "WorkSurCode": "1002"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_update():
    """
    更新
    :return:
    """
    url = f"{ip}:{port}/api/outer/console_db/updateConsole"
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
        "OldConEquipCode": "1006",
        "OldWorkSurCode": "1003"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def console_select():
    """
    获取信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/console_db/selectConsole"
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
    url = f"{ip}:{port}/api/outer/console_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ConEquipCode',
        'value': '1002'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    console_add()
    # console_delete()
    # console_update()
    # console_select()
    # console_info_search_by_column()
