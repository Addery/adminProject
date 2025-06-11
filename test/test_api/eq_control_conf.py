"""
@Author: zhang_zhiyi
@Date: 2025/4/23_16:43
@FileName:eq_control_conf.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

ip = "http://192.168.1.8"
port = "8023"


def start():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/start"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'ConEquipCode': '1001',
        'IP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def init():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/init"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'TunCode': '1001',
        'ConEquipCode': '1001',
        'ConfIP': '192.168.1.8',
        'IP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def update():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/update"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'OldConEquipCode': '1001',
        'ConEquipCode': '1001',
        'TunCode': '1001',
        'OldConfIP': '192.168.1.8',
        'ConfIP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def select_conf():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/selectConf"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'ConEquipCode',
        'Value': '1007'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def stop():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/stop"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'ConEquipCode': '1001',
        'IP': '192.168.1.8'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def delete():
    url = f"{ip}:{port}/api/outer/eq_con_conf_db/delete"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'ConEquipCode': '1001',
        'ConEquipIP': '192.168.1.8',
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # start()
    init()
    # update()
    # select_conf()
    # stop()
    # delete()
