"""
@Author: zhang_zhiyi
@Date: 2025/4/15_15:23
@FileName:histroy.py
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
        "column": "Mileage",  # AnomalyTime Mileage
        "start": "60",
        "end": "70"
        # "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        # "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # log_select()
    # log_search_by_column()
    section_filter()
