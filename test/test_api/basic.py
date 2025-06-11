"""
@Author: zhang_zhiyi
@Date: 2024/12/25_15:17
@FileName:basic.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 测试basic相关路由
"""
import requests


ip = 'http://192.168.1.7'
port = '8023'


def basic_search_some():
    url = f"{ip}:{port}/api/outer/basic/select/selectSome"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'TableName': 'project',
        'Columns': 'ProCode, ProName, ProAddress'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    basic_search_some()
