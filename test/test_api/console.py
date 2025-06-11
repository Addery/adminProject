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

# ip = "http://192.168.1.8"
ip = "https://sat.jovysoft.net"
port = "8023"


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
        "ConEquipCode": "1004",
        "ConEquipName": "测试总控设备_1004",
        "ConEquipIP": "192.168.1.8",
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
        "ConEquipCode": "8899",
        # "WorkSurCode": "1002"
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
        "ConEquipCode": "888",
        "ConEquipName": "name",
        "ConEquipIP": "1002",
        "TunCode": "1011",
        "ProCode": "80241",
        "StruCode": "88899",
        "OldConEquipCode": "999",
        "OldWorkSurCode": "888866"
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
        'Item': 'ConEquipCode',
        'Value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def statistics_status():
    """
    测试统计设备状态接口
    """
    url = f"{ip}:{port}/api/outer/console_db/statisticsStatus"
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


def get_exchange_name():
    url = f"{ip}:{port}/api/outer/console_db/getExchangeName2Web"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1001"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_init_and_working():
    url = f"{ip}:{port}/api/outer/console_db/getInitAndWorking"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "CompanyCode": "07361dfa-defc-4a08-ba11-5a495db9e565"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # console_add()
    # console_delete()
    # console_update()
    # console_select()
    console_info_search_by_column()
    # statistics_status()
    # get_exchange_name()
    # get_init_and_working()
