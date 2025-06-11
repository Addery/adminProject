"""
@Author: zhang_zhiyi
@Date: 2025/5/6_15:00
@FileName:company.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

# ip = "http://localhost"
ip = "https://sat.jovysoft.net"
port = "8023"


def company_add():
    url = f"{ip}:{port}/api/outer/company_db/addCompany"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'CompanyName': '测试网络科技有限公司',
        'CompanyAddress': '创业大厦'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def search_by_some():
    url = f"{ip}:{port}/api/outer/company_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Item': 'Code',
        'Value': '07361dfa-defc-4a08-ba11-5a495db9e565'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    company_add()
    # search_by_some()
