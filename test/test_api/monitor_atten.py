"""
@Author: zhang_zhiyi
@Date: 2025/5/14_11:56
@FileName:monitor_atten.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import requests

# IP = "http://192.168.1.8"
# IP = "https://sat.jovysoft.net"
IP = "https://wechat.jovysoft.net"
PORT = "443"


def monitor_atten():
    url = f"{IP}:{PORT}/api/mp/monitor_db/wechatMonitor"
    res = requests.post(url).text
    print(res)


if __name__ == '__main__':
    monitor_atten()
