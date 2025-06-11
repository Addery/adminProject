"""
@Author: zhang_zhiyi
@Date: 2025/5/13_10:28
@FileName:user_info.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

code = '0f1ok10w3hhnU43kdb3w3amgbo3ok10t'
ip = "192.168.1.8"
port = '8023'


def get_info():
    url = f'http://{ip}:{port}/api/mp/info_db/getMinProUserInfo'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Code': code
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    get_info()
