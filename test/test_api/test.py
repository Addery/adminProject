"""
@Author: zhang_zhiyi
@Date: 2024/10/17_14:34
@FileName:test.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests


ip = "http://127.0.0.1"
port = "5000"


def test_history():
    url = f"{ip}:{port}/outer/service/history"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'project_name': 'test_project_name',
        'tunnel_name': 'test_tunnel_name',
        'working_face': 'test_working_face',
        'mileage': 'test_mileage',
        'device_id': 'test_device_id',
        'year': 2024,
        'month': 8,
        'day': 29,
        'hour': None,
        'minute': None,
        'second': None
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.json())


def test_tree():
    url = f"{ip}:{port}/api/outer/pcd_op/tree"

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'project_name': 'test_project_name',
        'tunnel_name': 'test_tunnel_name',
        'working_face': 'test_working_face',
        'mileage': 'test_mileage',
        'device_id': 'test_device_id',
        'year': 2024,
        'month': 8,
        'day': 29
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_log():
    url = f"{ip}:{port}/outer/service/log"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'project_name': 'test_project_name',
        'tunnel_name': 'test_tunnel_name',
        'working_face': 'test_working_face',
        'mileage': 'test_mileage',
        'device_id': 'test_device_id',
        'year': 2024,
        'month': 8,
        'day': 29,
        'hour': None,
        'minute': None,
        'second': None,
        'page': 1,
        'count': 10
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_log_data_visual():
    url1 = f"{ip}:{port}/outer/service/log"
    url2 = f"{ip}:{port}/outer/service/log_data_visual"
    headers = {
        'Content-Type': 'application/json'
    }
    data1 = {
        'project_name': 'test_project_name',
        'tunnel_name': 'test_tunnel_name',
        'working_face': 'test_working_face',
        'mileage': 'test_mileage',
        'device_id': 'test_device_id',
        'year': 2024,
        'month': 8,
        'day': 29,
        'second': None,
        'page': 1,
        'count': 10
    }
    response = requests.post(url1, json=data1, headers=headers)
    print(response.json())
    print(response.status_code)

    data = response.json()
    single_data = data[1][-1]
    tag = single_data.get('tag')
    index = single_data.get('index')
    print(f"tag:{type(tag)}, {tag}")

    data2 = {
        'tag': tag,
        'index': index
    }
    response = requests.post(url2, json=data2, headers=headers)
    print(response.json())
    print(response.status_code)


def test_compare():
    url = f"{ip}:{port}/outer/service/compare"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'root': {
            'project_name': 'test_project_name',
            'tunnel_name': 'test_tunnel_name',
            'working_face': 'test_working_face',
            'mileage': 'test_mileage',
            'device_id': 'test_device_id',
            'year': 2024,
            'month': 8,
            'day': 29,
            'hour': 14
        },
        'comparison': {
            'project_name': 'test_project_name',
            'tunnel_name': 'test_tunnel_name',
            'working_face': 'test_working_face',
            'mileage': 'test_mileage',
            'device_id': 'test_device_id',
            'year': 2024,
            'month': 8,
            'day': 29,
            'hour': 15
        }
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_select_from_any_table():
    url = f"{ip}:{port}/api/outer/service/project/select"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'database_name': 'tunnel_project',
        'table_name': 'project',
        'table_columns': ['ProCode', 'ProName']
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_insert_into_any_table():
    url = f"{ip}:{port}/api/any_table/insert"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'database_name': 'tunnel_project',
        'table_name': 'tunnel',
        'insert_data': {
            'TunCode': '1006',
            'TunName': 'test',
            'LinkMan': 'test',
            'Phone': 'test',
            'ProCode': '1004'
        }
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_delete():
    url = f"{ip}:{port}/api/outer/project/delete"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'table_name': 'project',
        'delete_condition': {
            'ProCode': '1009'
        }
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


def test_update():
    url = f"{ip}:{port}/api/outer/project/update"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'table_name': 'project',
        'update_column': 'ProAddress',
        'update_value': 'test update address',
        'column': 'ProCode',
        'value': '1008'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    # start = time.time()
    # test_history()
    # print(f"history耗时：{time.time() - start}")
    # start = time.time()
    test_tree()
    # print(f"tree耗时：{time.time() - start}")
    # test_compare()
    # start = time.time()
    # test_log()
    # print(f"log耗时：{time.time() - start}")
    # test_log_data_visual()
    # test_compare()
    # test_select_from_any_table()
    """
    data = {
        'database_name': 'tunnel_project',
        'table_name': 'tunnel',
        'insert_data': {
            'TunCode': '1002',
            'TunName': 'test',
            'LinkMan': 'test',
            'Phone': 'test',
            'ProCode': '1003'
        }
    }
    data = {
        'database_name': 'tunnel_project',
        'table_name': 'project',
        'insert_data': {
            'ProCode': '1008',
            'ProName': 'test3',
            'ProAddress': 'test3',
            'LinkMan': 'test3',
            'Phone': 'test3',
            'ProCreateTime': '2024-9-4 17:49:30',
            'ProStatus': '1'
        }
    }
    """
    # test_insert_into_any_table()
    # test_delete()
    # test_update()
