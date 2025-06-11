"""
@Author: zhang_zhiyi
@Date: 2025/5/14_15:54
@FileName:util_wechat.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import json
import requests

ZUI_MG_CN_O = 'oZXDNwJai6_3S1oxQlZuiMGCn61o'

class WechatUtils(object):
    APP_ID = 'wxe58a6009379c1e6e'
    APP_SECRET = '04deba410e9763b695c06427674e961b'

    @staticmethod
    def get_access_token():
        """
        获取access_token
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'. \
            format(WechatUtils.APP_ID, WechatUtils.APP_SECRET)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        access_token = data.get('access_token')
        return access_token

    @staticmethod
    def get_user_list(access_token):
        url = f'https://api.weixin.qq.com/cgi-bin/user/get?access_token={access_token}'
        ans = requests.get(url)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    @staticmethod
    def get_user_unionid(access_token, user_open_id):
        url = f'https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={user_open_id}&lang=zh_CN'
        res = requests.get(url)
        data = res.json()
        return data

    @staticmethod
    def sendmsg(self, access_token, open_ids):
        """
        给所有用户发送消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
        now = open_ids.get('now')
        data = {
            "time2": {
                "value": f"{now.year}年{now.month}月{now.day}日 {now.hour}:{now.minute}:{now.second}",
            },
            "phrase9": {
                "value": open_ids.get('degree'),
            },
            "thing11": {
                "value": open_ids.get('describe'),
            },
            "thing66": {
                "value": open_ids.get('region'),
            }
        }
        if self.openIDs != '':
            for open_id in self.openIDs:
                if open_id == ('%s' % ZUI_MG_CN_O):  # test
                    body = {
                        "touser": open_id,
                        "template_id": self.templateID,
                        # "url": "https://www.baidu.com/",
                        "url": "https://visit.jovysoft.net/",
                        "topcolor": "#FF0000",
                        "miniprogram": {
                            "appid": "wx6d9fb84f565be54e",
                            "pagepath": "pages/index/index?Identification=9666"
                        },
                        # 对应模板中的数据模板
                        "data": data
                    }
                    send_data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))  # 将数据编码json并转换为bytes型
                    response = requests.post(url, data=send_data)
                    result = response.json()  # 将返回信息json解码
                    print(result)  # 根据response查看是否广播成功
                    break
        else:
            print("当前没有用户关注该公众号！")


if __name__ == '__main__':
    access_token = WechatUtils.get_access_token()
    WechatUtils.get_user_list(access_token)
