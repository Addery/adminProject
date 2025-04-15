"""
@Author: zhang_zhiyi
@Date: 2025/4/8_16:26
@FileName:role.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime
import requests


ip = "http://192.168.1.8"
port = "8023"


def role_add():
    url = f"{ip}:{port}/api/outer/role_db/addRole"
    headers = {
        'Content-Type': 'application/json'
    }
    now = datetime.datetime.now()
    data = {
        "RoleClass": 1,
        "Creator": "admin",
        # "CreateTime": str(now),
        "UserCode": "1",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def role_del():
    url = f"{ip}:{port}/api/outer/role_db/deleteRole"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
            "ID": 6
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def role_update():
    url = f"{ip}:{port}/api/outer/role_db/updateRole"
    headers = {
        'Content-Type': 'application/json'
    }
    now = datetime.datetime.now()
    data = {
        "OldID": 1,
        "RoleClass": 1,
        "Creator": "admin",
        "CreateTime": str(now),
        "Status": 0,
        "UserCode": "2",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def role_select():
    url = f"{ip}:{port}/api/outer/role_db/selectRole"
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


def role_info_search_by_some():
    url = f"{ip}:{port}/api/outer/role_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'ID',
        'Value': '5'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # role_add()
    # role_del()
    # role_update()
    role_select()
    # role_info_search_by_some()
