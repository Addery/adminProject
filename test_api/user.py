"""
@Author: zhang_zhiyi
@Date: 2024/7/25_11:19
@FileName:user.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-用户表相关
"""
import time
import requests


ip = "http://127.0.0.1"
port = "5000"


def user_login():
    url = f"{ip}:{port}/api/outer/user_db/login"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "UserName": "user12",
        "PassWord": "123456",
        "ProCode": "1004"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_add():
    url = f"{ip}:{port}/api/outer/user_db/addUser"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "UserName": "user14",
        "PassWord": "123456",
        "RealName": "zzz",
        # "RoleClass": 1,
        "Phone": "123",
        "ProCode": "1004",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_del():
    url = f"{ip}:{port}/api/outer/user_db/deleteUser"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "UserName": "user10",
        "ProCode": "1002"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_update():
    url = f"{ip}:{port}/api/outer/user_db/updateUser"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "OldUserName": "user12",
        "OldProCode": "1004",
        "UserName": "user15",
        "PassWord": "8023",
        "RealName": "zzz",
        "RoleClass": 1,
        "Phone": "123",
        "ProCode": "1002",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_select():
    url = f"{ip}:{port}/api/outer/user_db/selectUser"
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


def user_password_set():
    url = f"{ip}:{port}/api/outer/user_db/setUserPassword"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'UserName': 'user11',
        'ProCode': '1002',
        'PassWord': '1234'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_info_search_by_some():
    url = f"{ip}:{port}/api/outer/user_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'UserName',
        'value': 'Addery'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def user_permission_modify():
    url = f"{ip}:{port}/api/outer/user_db/modifyUserPermission"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'UserName': 'user11',
        'ProCode': '1002',
        'RoleClass': 1
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # user_login()
    # user_add()
    # user_del()
    # user_update()
    # user_select()
    # user_password_set()
    # user_info_search_by_some()
    user_permission_modify()
