"""
@Author: zhang_zhiyi
@Date: 2025/4/24_19:25
@FileName:eq_data_conf.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

ip = "http://192.168.1.8"
port = "8023"


def start():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/start"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'DataAcqEquipCode': '1001',
        'IP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def init():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/init"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'ConEquipCode': '1001',
        'DataAcqEquipCode': '1001',
        'ConfIP': '192.168.1.8',
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def stop():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/stop"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'DataAcqEquipCode': '1001',
        'IP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def update():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/update"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'OldDataAcqEquipCode': '1001',
        'DataAcqEquipCode': '1001',
        'ConEquipCode': '1001',
        'OldConfIP': '192.168.1.8',
        'ConfIP': '192.168.1.10'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def select_conf():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/selectConf"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'DataAcqEquipCode',
        'Value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def delete():
    url = f"{ip}:{port}/api/outer/eq_data_conf_db/delete"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'DataAcqEquipCode': '1001',
        'DataAcqEquipIP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    start()
    # init()
    # stop()
    # update()
    # select_conf()
    # delete()
