"""
@Author: zhang_zhiyi
@Date: 2025/6/11_18:08
@FileName:wx.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import datetime

import requests

# ip = "http://192.168.1.10"
ip = "https://sat.jovysoft.net"
port = "8023"


def get_access_token():
    url = f"{ip}:{port}/api/wx/wx_db/getAccessToken"
    response = requests.post(url)
    print(response.json())
    print(response.status_code)


def sendmsg():
    url = f"{ip}:{port}/api/wx/wx_db/sendMSG"
    now = datetime.datetime.now()
    data = {
        'Info': {
            'degree': '测试等级',
            'describe': '测试描述',
            'region': '测试区域',
            'now': now.strftime('%Y-%m-%d %H:%M:%S'),
            'Identification': '1001_1001_1001_1747649435.7616796'
        },
        'OpenIDS': ['oZXDNwJai6_3S1oxQlZuiMGCn61o'],
        'AccessToken': '93_4RooYaCefOcXS33uxsEQDylBck6izlu8tDaujOmf8cTVyTEwXnpU4YYLZnUtWx3xEQxl_bD3_fLKbptsHMmAnak8PLYFnXkplbfw_XCGeqMYyyee5oGwXBr8SUQTRWcAJACAF'
    }
    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    get_access_token()
    # sendmsg()
