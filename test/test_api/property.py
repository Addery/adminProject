"""
@Author: zhang_zhiyi
@Date: 2025/5/9_15:04
@FileName:property.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

# ip = "http://192.168.1.8"
ip = "https://sat.jovysoft.net"
port = 8023


def get_project_all_count():
    url = f'{ip}:{port}/api/mp/property_db/getProjectAllCount'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_tunnel_all_count():
    url = f'{ip}:{port}/api/mp/property_db/getTunnelAllCount'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_all_count():
    url = f'{ip}:{port}/api/mp/property_db/getAllCount'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def get_all_count_by_join():
    url = f'{ip}:{port}/api/mp/property_db/getAllCountByJoin'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'CompanyCode',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # get_project_all_count()
    # get_tunnel_all_count()
    get_all_count()
    # get_all_count_by_join()
