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
from PIL import Image

from utils.util_picture import IMGUtils

# ip = "http://192.168.1.10"
ip = "https://sat.jovysoft.net"
port = "8023"


def anomaly_add():
    url = f"{ip}:{port}/api/outer/anomaly_db/addAnomaly"
    # headers = {
    #     'Content-Type': 'application/json'
    # }

    avia_img = Image.open(r'E:\07-code\tunnelProject\adminProject\data\pic\pcd.png')
    camera_img = Image.open(r'E:\07-code\tunnelProject\adminProject\data\pic\camera.png')

    now = datetime.datetime.now()
    data = {
        'LogData': {
            'ProCode': '1001',
            'TunCode': '1001',
            'WorkSurCode': '1001',
            'StruCode': '1001',
            'Mileage': '80',
            'ConEquipCode': '1001',
            'DataAcqEquipCode': '1001',
            "AnomalyTime": f'{now.strftime("%Y-%m-%d %H:%M:%S")}'
        },
        'DescData': {
            "Degree": str(['三', '三']),
            "Region": str([100, 3306]),
            "Position": str([(8100, 254, 324), (14, 242, 30)]),
            "Bas": str([7, 6])
        },
        'ImgData': {
            'AviaPicturePath': IMGUtils.img2base64(avia_img),
            'CameraPicturePath': IMGUtils.img2base64(camera_img)
        }
    }
    # data = {
    #     "Identification": str(time.time()),
    #     "DescCode": '1017',
    #     "Degree": '1',
    #     "Region": [1, 2, 3],
    #     "Position": [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
    #     "Bas": [3, 3, 3],
    #     "ProCode": '1001',
    #     "TunCode": '1001',
    #     "WorkSurCode": '1001',
    #     "StruCode": '1001',
    #     "Mileage": '100',
    #     "ConEquipCode": '1001',
    #     "DataAcqEquipCode": '1001',
    #     "AnomalyTime": f'{now.strftime("%Y-%m-%d %H:%M:%S")}'
    # }

    # response = requests.post(url, json=data, headers=headers)
    response = requests.post(url, json=data)
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
        'PageSize': 10,
        # 'Item': ['ProCode', 'Sign'],
        # 'Value': ['1001', '0']
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
        'Item': ['ProCode', 'Mileage'],
        'Value': ['1001', '90']
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
        "Column": "AnomalyTime",
        "Start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "End": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def modify_log_status():
    url = f"{ip}:{port}/api/outer/anomaly_db/modifyLogStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "Identification": "1003_1001_49914_1745739245.2489107",
        "Operation": "1"
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def log_status():
    url = f"{ip}:{port}/api/outer/anomaly_db/statisticsStatus"
    data = {
        "Item": "CompanyCode",
        "Value": "07361dfa-defc-4a08-ba11-5a495db9e565"
    }
    response = requests.post(url, json=data)

    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # anomaly_add()
    # anomaly_delete()
    # log_select()
    # desc_select()
    # log_search_by_column()
    # desc_search_by_column()
    # section_filter()
    # modify_log_status()
    log_status()

