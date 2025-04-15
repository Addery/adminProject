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


ip = "http://192.168.1.3"
port = "8023"


def anomaly_add():
    url = f"{ip}:{port}/api/outer/anomaly_db/addAnomaly"
    headers = {
        'Content-Type': 'application/json'
    }
    now = datetime.datetime.now()
    data = {
        "Identification": str(time.time()),
        "DescCode": '1017',
        "Degree": '1',
        "Region": [1, 2, 3],
        "Position": [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
        "Bas": [3, 3, 3],
        "ProCode": '1001',
        "TunCode": '1001',
        "WorkSurCode": '1001',
        "StruCode": '1001',
        "Mileage": '100',
        "ConEquipCode": '1001',
        "DataAcqEquipCode": '1001',
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
    url = f"{ip}:{port}/api/outer/anomaly_db/deleteAnomaly"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DescCode": "1017"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def log_select():
    """
    获取信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/anomaly_db/selectAnomalyLog"
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
    url = f"{ip}:{port}/api/outer/anomaly_db/selectAnomalyLogDesc"
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
    url = f"{ip}:{port}/api/outer/anomaly_db/searchLogByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ProCode',
        'value': '1003'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def desc_search_by_column():
    url = f"{ip}:{port}/api/outer/anomaly_db/searchDescByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'DescCode',
        'value': '1730115219.1885593'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def section_filter():
    url = f"{ip}:{port}/api/outer/anomaly_db/sectionFilter"
    headers = {
        'Content-Type': 'application/json'
    }
    start_time = datetime.datetime(2024, 10, 1, 0, 0, 0)
    end_time = datetime.datetime(2024, 11, 1, 0, 0, 0)
    data = {
        "column": "AnomalyTime",
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # anomaly_add()
    # anomaly_delete()
    # log_select()
    # desc_select()
    # log_search_by_column()
    # desc_search_by_column()
    section_filter()
