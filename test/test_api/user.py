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


# ip = "http://192.168.1.8"
ip = "https://sat.jovysoft.net"
port = "8023"


def user_login():
    url = f"{ip}:{port}/api/outer/user_db/login"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        # "Phone": "18835791843",
        # "AuthCode": "888888"
        "Phone": "15202411793",
        "AuthCode": "138606",
        "Code": "0f1URl0w3IBAU43jN33w3a7gTZ1URl0w"
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
        "RealName": "测试用户4",
        "Phone": "18636799504",
        "CompanyCode": "bea9d00e-e714-4e55-8b2d-b0c10f323a0f"
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
        "Phone": 123
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
        "OldPhone": "12345678910",
        "UserName": "user15",
        "PassWord": "8023",
        "RealName": "zzz",
        "RoleClass": 1,
        "Phone": "98765432100",
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
        'Phone': '15202411793',
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
        'Item': 'Name',
        'Value': 'user14'
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
        'Phone': '15202411793',
        'RoleClass': 1
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_auth_code():
    url = f"{ip}:{port}/api/outer/user_db/getAuthCode"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Phone': '15202411793'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # get_auth_code()
    # user_login()
    user_add()
    # user_del()
    # user_update()
    # user_select()
    # user_password_set()
    # user_info_search_by_some()
    # user_permission_modify()

