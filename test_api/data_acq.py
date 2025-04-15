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


ip = "http://192.168.1.8"
port = "8023"


def data_acq_add():
    """
    添加数据采集器
    :return:
    """
    url = f"{ip}:{port}/api/outer/data_acq_db/addDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DataAcqEquipCode": "1011",
        "DataAcqEquipName": "name",
        "DataAcqEquipIP": "localhost",
        "DataAcqEquipInterval": "10",
        "Distance": "80",
        "ConEquipCode": "1001",
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_delete():
    """
    删除数据采集器
    :return:
    """
    url = f"{ip}:{port}/api/outer/data_acq_db/deleteDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ConEquipCode": "1002",
        "DataAcqEquipCode": "1005"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_update():
    """
    更新数据采集器
    :return:
    """
    url = f"{ip}:{port}/api/outer/data_acq_db/updateDataAcq"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "DataAcqEquipCode": "1005",
        "DataAcqEquipName": "name",
        "DataAcqEquipIP": "localhost",
        "DataAcqEquipInterval": "10",
        "Distance": "100",
        "ConEquipCode": "1002",
        "DataAcaEquipStatus": "1",
        "OldConEquipCode": "1002",
        "OldDataAcqEquipCode": "1005"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def data_acq_select():
    """
    信息
    :return:
    """
    url = f"{ip}:{port}/api/outer/data_acq_db/selectDataAcq"
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
    url = f"{ip}:{port}/api/outer/data_acq_db/searchInfoByColumn"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'item': 'ConEquipCode',
        'value': '1002'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def statistics_status():
    """
    测试统计设备状态接口
    """
    url = f"{ip}:{port}/api/outer/data_acq_db/statisticsStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == "__main__":
    # data_acq_add()
    # data_acq_delete()
    # data_acq_update()
    # data_acq_select()
    # data_acq_info_search_by_column()
    statistics_status()
