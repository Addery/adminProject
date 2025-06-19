"""
@Author: zhang_zhiyi
@Date: 2025/4/15_15:23
@FileName:histroy.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import base64
import datetime
import json
import os
import pickle
import time

import pandas as pd
import requests

# ip = "http://127.0.0.1"
ip = "https://sat.jovysoft.net"
port = "8023"


def log_select():
    url = f"{ip}:{port}/api/outer/history_db/selectHistory"
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
    url = f"{ip}:{port}/api/outer/history_db/searchLogByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'ProCode',
        'Value': '1003'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def section_filter():
    url = f"{ip}:{port}/api/outer/history_db/sectionFilter"
    headers = {
        'Content-Type': 'application/json'
    }
    start_time = datetime.datetime(2025, 4, 1, 0, 0, 0)
    end_time = datetime.datetime(2025, 5, 1, 0, 0, 0)
    data = {
        "Column": "Mileage",  # AnomalyTime Mileage
        "Start": "60",
        "End": "70"
        # "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        # "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def upload_anomaly_file():
    url = f"{ip}:{port}/api/outer/history_db/uploadAnomalyFile"
    df = pd.read_csv(r'E:\07-code\tunnelProject\controlProject\data\test.csv')
    binary_df = base64.b64encode(pickle.dumps(df)).decode('utf-8')
    str_df = json.dumps(binary_df)
    data = {
        'Region': {'1': str_df},
        'Describe': {'1': [[1, 2, 3], 0.06, 1]},
        'ProCode': '1001',
        'TunCode': '1001',
        'ConEquipCode': '1001',
        'LogUUID': 'test'
    }

    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)


def upload_init_file():
    url = f"{ip}:{port}/api/outer/history_db/uploadInitFile"
    df = pd.read_csv(r'E:\07-code\tunnelProject\adminProject\test\data\1731656822.6120367_0.csv')
    binary_df = base64.b64encode(pickle.dumps(df)).decode('utf-8')
    str_df = json.dumps(binary_df)

    region = {}
    region_path = r'E:\07-code\tunnelProject\adminProject\test\data\region'
    with os.scandir(region_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.csv'):
                csv_path = entry.path
                df_region = pd.read_csv(csv_path)
                binary_region = base64.b64encode(pickle.dumps(df_region)).decode('utf-8')
                region[entry.name.split('.')[0]] = json.dumps(binary_region)
    now = datetime.datetime.now()
    data = {
        'Region': region,
        'IntactData': str_df,
        'ProCode': '1001',
        'TunCode': '1001',
        'ConEquipCode': '1001',
        'LogUUID': 'test',
        'updateTime': now.strftime('%Y-%m-%d %H:%M:%S')
    }

    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)


def add_history():
    url = f"{ip}:{port}/api/outer/history_db/addHistory"
    now = datetime.datetime.now()
    data = {
        'PCDLogUID': 'test',
        'ProCode': '1001',
        'TunCode': '1001',
        'WorkSurCode': '1001',
        'StruCode': '1001',
        'Mileage': 'test',
        'ConEquipCode': '1001',
        'DataAcqEquipCode': '1001',
        'AnomalyTime': f'{now.strftime("%Y-%m-%d %H:%M:%S")}',
        'CompanyCode': 'test',
        'AnomalyRegionPath': 'test',
        'AnomalyDescribePath': 'test',
        'UpdateInitCount': 10,
    }
    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # log_select()
    # log_search_by_column()
    # section_filter()
    # upload_anomaly_file()
    upload_init_file()
    # add_history()
