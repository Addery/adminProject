"""
@Author: zhang_zhiyi
@Date: 2024/10/24_18:36
@FileName:pcd_db.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

ip = "http://127.0.0.1"
# ip = "https://sat.jovysoft.net"
port = "8023"


def log_by_code_or_date():
    url = f"{ip}:{port}/api/outer/pcd_db_op/logByCodeOrDate"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ProCode": '1001',
        # 'TunCode': '1004',
        # "WorkSurCode": "1003",
        # "StruCode": "1003",
        # "ConEquipCode": "1002",
        # "DataAcqEquipCode": "1001",
        # "Year": 2024,
        # "Month": 10,
        # "Day": 28,
        # "Hour": 19,
        # "Minute": 31,
        # "Second": 41
    }

    response = requests.post(url, json=data, headers=headers)
    res = response.json()
    print(res)
    # t = res['data']['items'][0]['AnomalyTime']
    # print(type(t), t)
    print(response.status_code)


def history_by_code_and_date():
    url = f"{ip}:{port}/api/outer/pcd_db_op/historyCodeAndDate"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DataAcqEquipCode": '1001',
        "Year": 2024,
        "Month": 10,
        "Day": 25,
        "Hour": 15,
        "Minute": 30,
        "Second": 42
    }

    response = requests.post(url, json=data, headers=headers)
    res = response.json()
    print(res)
    print(response.status_code)


def compare():
    url = f"{ip}:{port}/api/outer/pcd_db_op/compare"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'root': {
            "ProCode": '1003',
            'TunCode': '1004',
            "WorkSurCode": "1003",
            "StruCode": "1003",
            "ConEquipCode": "1002",
            "DataAcqEquipCode": "1001",
            "Year": 2024,
            "Month": 10,
            "Day": 28,
            "Hour": 19,
            "Minute": 31,
            "Second": 41
        },
        'comparison': {
            "ProCode": '1003',
            'TunCode': '1004',
            "WorkSurCode": "1003",
            "StruCode": "1003",
            "ConEquipCode": "1002",
            "DataAcqEquipCode": "1001",
            "Year": 2024,
            "Month": 10,
            "Day": 28,
            "Hour": 19,
            "Minute": 31,
            "Second": 42
        }
    }
    response = requests.post(url, json=data, headers=headers)
    res = response.json()
    print(res)
    print(res.get('msg'))


def select_pcd_by_column():
    url = f"{ip}:{port}/api/outer/pcd_db_op/selectPCDByColumn"
    data = {
        "Item": ['PCDLogUID'],
        "Value": ['test']
    }
    # data = {
    #     "Item": ['ProCode'],
    #     "Value": ['1001']
    # }

    response = requests.post(url, json=data)
    res = response.json()
    print(res.get('data'))
    print(response.status_code)


def select_region_by_column():
    url = f"{ip}:{port}/api/outer/pcd_db_op/selectRegionPCDByColumn"
    data = {
        "Item": ['PCDLogUID'],
        "Value": ['uuid_test']
    }

    response = requests.post(url, json=data)
    res = response.json()
    print(res)
    print(response.status_code)


def select_anomaly_pcd_by_column():
    url = f"{ip}:{port}/api/outer/pcd_db_op/selectAnomalyPCDByColumn"
    data = {
        "Item": ['PCDLogUID'],
        "Value": ['uuid_test']
    }

    response = requests.post(url, json=data)
    res = response.json()
    print(res)
    print(response.status_code)


def select_clearance_calculation_by_column():
    url = f"{ip}:{port}/api/outer/pcd_db_op/selectClearanceCalculationByColumn"
    data = {
        "Item": ['PCDLogUID'],
        "Value": ['test']
    }

    response = requests.post(url, json=data)
    res = response.json()
    print(res)
    print(response.status_code)


if __name__ == "__main__":
    # log_by_code_or_date()
    # history_by_code_and_date()
    # compare()
    # select_pcd_by_column()
    # select_region_by_column()
    # select_anomaly_pcd_by_column()
    select_clearance_calculation_by_column()
