"""
@Author: zhang_zhiyi
@Date: 2025/5/12_15:35
@FileName:start_or_stop_eq.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
from test.test_api.eq_control_conf import start as c_start, stop as c_stop
from test.test_api.eq_data_conf import start as d_start, stop as d_stop


def start_eq():
    c_start()
    d_start()


def stop_eq():
    c_stop()
    d_stop()


if __name__ == '__main__':
    # start_eq()
    stop_eq()
