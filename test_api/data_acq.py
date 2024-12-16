"""
@Author: zhang_zhiyi
@Date: 2024/10/18_15:55
@FileName:data_acq.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 接口测试-数据采集器表相关
"""
import requests


def data_acq_add():
    """
    添加数据采集器
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/data_acq_db/addDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DataAcqEquipCode": "1004",
        "DataAcqEquipName": "name",
        "DataAcqEquipIP": "localhost",
        "DataAcqEquipInterval": "10",
        "Distance": "80",
        "ConEquipCode": "1002",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_delete():
    """
    删除数据采集器
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/data_acq_db/deleteDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1003",
        "DataAcqEquipCode": "1001"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_update():
    """
    更新数据采集器
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/data_acq_db/updateDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DataAcqEquipCode": "1005",
        "DataAcqEquipName": "name",
        "DataAcqEquipIP": "localhost",
        "DataAcqEquipInterval": "10",
        "Distance": "100",
        "ConEquipCode": "1003",
        "DataAcaEquipStatus": "1",
        "OldConEquipCode": "1002",
        "OldDataAcqEquipCode": "1004"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_select():
    """
    信息
    :return:
    """
    url = "http://127.0.0.1:8023/api/outer/data_acq_db/selectDataAcq"
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


def data_acq_info_search_by_column():
    url = "http://127.0.0.1:8023/api/outer/data_acq_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ConEquipCode',
        'value': '1001'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    data_acq_add()
    # data_acq_delete()
    # data_acq_update()
    # data_acq_select()
    # data_acq_info_search_by_column()
