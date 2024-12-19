"""
@Author: zhang_zhiyi
@Date: 2024/10/17_14:36
@FileName:project.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-项目表相关
"""
import requests


ip = "http://127.0.0.1"
port = "5000"


def project_add():
    """
    添加新项目
    :return:
    """
    url = f"{ip}:{port}/api/outer/project_db/addProject"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ProCode": "1009",
        "ProName": "p",
        "ProAddress": "test",
        "LinkMan": 'user',
        "Phone": "123"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def project_delete():
    """
    删除项目
    :return:
    """
    url = f"{ip}:{port}/api/outer/project_db/deleteProject"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ProCode": "1009"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def project_update():
    """
    更新项目
    :return:
    """
    url = f"{ip}:{port}/api/outer/project_db/updateProject"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "OldProCode": "1005",
        "ProCode": "1005",
        "ProName": "pp",
        "ProAddress": "test",
        "LinkMan": 'user',
        "Phone": "123"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def project_select():
    """
    项目信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/project_db/selectProject"
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


def project_info_search_by_column():
    url = f"{ip}:{port}/api/outer/project_db/searchProjectByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ProName',
        'value': 'p'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # project_add()
    # project_delete()
    # project_update()
    # project_select()
    project_info_search_by_column()
