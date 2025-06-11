"""
@Author: zhang_zhiyi
@Date: 2025/5/28_9:57
@FileName:util_file.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 文件工具类
"""
import os
import random
from decimal import Decimal, getcontext

import pandas as pd
import requests

from routes.local.status_code.baseHttpStatus import BaseHttpStatus


class FileUtils(object):
    DATA_ROOT_DIR = r'D:\tunnelProject\adminProject\data'

    # getcontext().prec = 20
    # make_decimal = Decimal

    @staticmethod
    def read_pcd_txt2str(pcd_path):
        try:
            relative_path = pcd_path.replace('https://sat.jovysoft.net:8066/', '')
            path = f'{FileUtils.DATA_ROOT_DIR}/{relative_path}'
            start_line = 11
            pcd_list = []
            # response = requests.get(pcd_path)
            # if response.status_code == 200:
            #     lines = response.text.splitlines()
            with open(path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, start=1):
                    if i >= start_line:
                        temp_line = line.strip()
                        # rgb = [Decimal(random.randint(0, 255)) for _ in range(3)]
                        temp_line_list = [float(x) for x in temp_line.split(' ')[:3]]
                        temp_line_list.append(float(random.randint(0, 255)))
                        pcd_list.extend(temp_line_list)
                return {'code': BaseHttpStatus.OK.value, 'msg': '查找成功', 'data': pcd_list}
        except Exception as e:
            return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': f"{str(e)}"}

    @staticmethod
    def read_pcd_csv2str(pcd_path):
        """
        读取 csv 点云文件，并转化为前端页面需要的格式
        """
        try:
            relative_path = pcd_path.replace('https://sat.jovysoft.net:8066/', '')
            pcd_path = f'{FileUtils.DATA_ROOT_DIR}/{relative_path}'
            df = pd.read_csv(pcd_path)
            pcd_list = []
            for row in df.itertuples(index=False):
                # 假设前3列是点云坐标，最后一列是颜色
                pcd_list.extend([float(row.X), float(row.Y), float(row.Z), float(row.Reflectivity)])
            return {'code': BaseHttpStatus.OK.value, 'msg': '查找成功', 'data': pcd_list}
        except Exception as e:
            return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': f"{str(e)}"}

    @staticmethod
    def read_region_dir_txt(region_dir):
        try:
            relative_path = region_dir.replace('https://sat.jovysoft.net:8066/', '')
            dir = f'{FileUtils.DATA_ROOT_DIR}/{relative_path}'
            region_dict = {}
            with os.scandir(dir) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith('.txt'):
                        with open(entry.path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        index = entry.name.split('.')[0]
                        region_dict[index] = content
            return {'code': BaseHttpStatus.OK.value, 'msg': '查找成功', 'data': region_dict}
        except Exception as e:
            return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': f"{str(e)}"}

    @staticmethod
    def read_region_dir_csv(region_dir):
        try:
            region_dir = region_dir.replace('https://sat.jovysoft.net:8066', 'D:/tunnelProject/adminProject/data')
            region_dict = {}
            with os.scandir(region_dir) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith('.csv'):
                        csv_path = entry.path
                        df = pd.read_csv(csv_path)
                        pcd_list = []
                        for row in df.itertuples(index=False):
                            # 假设前3列是点云坐标，最后一列是颜色
                            pcd_list.extend([float(row.X), float(row.Y), float(row.Z), float(row.Reflectivity)])
                        region_dict[entry.name.split('.')[0]] = pcd_list
            return {'code': BaseHttpStatus.OK.value, 'msg': '查找成功', 'data': region_dict}
        except Exception as e:
            return {'code': BaseHttpStatus.ERROR.value, 'msg': '查找失败', 'data': f"{str(e)}"}


if __name__ == '__main__':
    # FileUtils.read_pcd_txt2str(r'https://sat.jovysoft.net:8066/data/test/test_pcd.txt')
    FileUtils.read_region_dir(r'E:\07-code\tunnelProject\controlProject\test\region')
