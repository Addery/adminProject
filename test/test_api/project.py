"""
@Author: zhang_zhiyi
@Date: 2024/10/17_14:36
@FileName:project.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-项目表相关
"""
import datetime

import requests

# ip = "http://192.168.1.8"
ip = "https://sat.jovysoft.net"
port = "8023"


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
        "ProCode": "1002",
        "ProName": "测试项目_1002",
        "ProAddress": "陕西省西安市",
        "LinkMan": '测试管理员',
        "Phone": "1889996666",
        "ProCycle": "270"
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

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "OldProCode": "1002",
        "ProCode": "1002",
        "ProName": "测试项目_1002",
        "ProAddress": "陕西省西安市",
        "LinkMan": '测试管理员',
        "Phone": "18889996666",
        "ProCycle": "250",
        "ProCreateTime": now
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
        'PageSize': 10,
        # 'SearchText': 'addery'
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
        'Item': 'ProCode',
        'Value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def project_status():
    url = f"{ip}:{port}/api/outer/project_db/statisticsStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
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
    # project_status()
