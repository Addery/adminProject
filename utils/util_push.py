"""
@Author: zhang_zhiyi
@Date: 2025/5/19_20:15
@FileName:util_push.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 微信公众号推送消息工具类
"""
import datetime
import json

import requests


class PushUtils(object):
    """
    微信公众号推送消息工具类
    """

    APPID = 'wxe58a6009379c1e6e'  # 公众号appid
    APPSECRET = '04deba410e9763b695c06427674e961b'  # 公众号app secret
    TEMPLATEID = 'dXGwzbJovV_fXDuDlfhmxrN8ofdjJkt9yr4VXJJhdfg'  # 公众号消息推送模版 id
    MPAPPID = 'wx6d9fb84f565be54e'  # 小程序appid

    @staticmethod
    def get_access_token():
        """
        获取 access token
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'. \
            format(PushUtils.APPID, PushUtils.APPSECRET)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        return access_token

    @staticmethod
    def get_user_list(access_token):
        url = f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={access_token}'
        ans = requests.get(url)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    @staticmethod
    def sendmsg(open_ids, info, access_token):
        """
        给所有用户发送消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
        now = info.get('now')
        data = {
            "time2": {
                "value": f"{now.year}年{now.month}月{now.day}日 {now.hour}:{now.minute}:{now.second}",
            },
            "phrase9": {
                "value": info.get('degree'),
            },
            "thing11": {
                "value": info.get('describe'),
            },
            "thing66": {
                "value": info.get('region'),
            }
        }
        if open_ids != '':
            for open_id in open_ids:
                # 构建请求体
                body = PushUtils.build_request_body(open_id, data, info.get('Identification'))

                send_data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))  # 将数据编码json并转换为bytes型
                response = requests.post(url, data=send_data)
                result = response.json()  # 将返回信息json解码
                print(result)  # 根据response查看是否广播成功
                break
        else:
            print("当前没有用户关注该公众号！")

    @staticmethod
    def build_request_body(open_id, data, log_code):
        """构建微信消息模板请求体"""
        return {
            "touser": open_id,
            "template_id": PushUtils.TEMPLATEID,
            "url": "https://visit.jovysoft.net/",
            "topcolor": "#FF0000",
            "miniprogram": {
                "appid": PushUtils.MPAPPID,
                "pagepath": f"pages/index/index?Identification={log_code}"
            },
            "data": data
        }


if __name__ == '__main__':
    # ['oZXDNwJai6_3S1oxQlZuiMGCn61o', 'oZXDNwBJUjM-FsswcwYQKAIpHOtw']
    access_token = PushUtils.get_access_token()
    PushUtils.sendmsg(
        PushUtils.get_user_list(access_token),
        {
            'degree': '测试等级',
            'describe': '测试描述',
            'region': '测试区域',
            'now': datetime.datetime.now(),
            'Identification': '1001_1001_1001_1747649435.7616796'
        },
        access_token
    )

