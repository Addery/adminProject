"""
@Author: zhang_zhiyi
@Date: 2024/10/21_18:17
@FileName:anomaly.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime
import time

import requests


def anomaly_add():
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/addAnomaly"
    headers = {
        'Content-Type': 'application/json'
    }
    now = datetime.datetime.now()
    data = {
        "Identification": str(time.time()),
        "DescCode": '1016',
        "Degree": '1',
        "Region": [1, 2, 3],
        "Position": [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
        "Bas": [3, 3, 3],
        "ProCode": '1001',
        "TunCode": '1002',
        "WorkSurCode": '1002',
        "StruCode": '1001',
        "Mileage": '100',
        "ConEquipCode": '1002',
        "DataAcqEquipCode": '1002',
        "AnomalyTime": f'{now.strftime("%Y-%m-%d %H:%M:%S")}'
    }

    response = requests.post(url, json=data, headers=headers)

    print(response.json())
    print(response.status_code)


def anomaly_delete():
    """
    删除
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/deleteAnomaly"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DescCode": "1003"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def log_select():
    """
    获取信息
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/selectAnomalyLog"
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


def desc_select():
    """
    获取信息
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/selectAnomalyLogDesc"
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


def log_search_by_column():
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/searchLogByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ProCode',
        'value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def desc_search_by_column():
    url = "http://127.0.0.1:8023/api/outer/anomaly_db/searchDescByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'DescCode',
        'value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    anomaly_add()
    # anomaly_delete()
    # console_update()
    # log_select()
    # desc_select()
    # log_search_by_column()
    # desc_search_by_column()
