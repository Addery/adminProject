"""
@Author: zhang_zhiyi
@Date: 2025/5/7_16:00
@FileName:util_auth_code.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import configparser
import os
from urllib.parse import quote

import requests
from routes.local.status_code.baseHttpStatus import BaseHttpStatus


class AuthCodeUtils(object):
    CURRENT_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    AUTH_CODE_CONFIG_PATH = "../config/auth_code_config.ini"
    DEFAULT_CONFIG_PATH = os.path.join(CURRENT_PROJECT_PATH, AUTH_CODE_CONFIG_PATH)

    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG_PATH)
    POST_URL = config.get('AuthCodeParameter', 'postURL')
    CORP_ID = config.get('AuthCodeParameter', 'corpID')
    PASSWORD = config.get('AuthCodeParameter', 'password')

    @staticmethod
    def send_auth_code(phone, code):
        try:
            content = "您的验证码" + code + "，该验证码2分钟内有效，请勿泄漏于他人！" + "【卓软网络】"
            post_data = {
                'CorpID': quote(AuthCodeUtils.CORP_ID),
                'Pwd': quote(AuthCodeUtils.PASSWORD),
                'Mobile': phone,
                'Content': quote(content),
                'Cell': '',
                'SendTime': ''
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',  # 明确指定编码
            }

            # 发送POST请求
            response = requests.post(
                AuthCodeUtils.POST_URL,
                data=post_data,  # 使用字典来表示表单数据
                headers=headers,
                allow_redirects=True
            )

            # 或者根据实际情况选择合适的编码
            try:
                response.encoding = 'utf-8'
                response_text = response.text
            except UnicodeDecodeError:
                response.encoding = 'gbk'
                response_text = response.text

            if response.status_code == 200:
                return {'code': BaseHttpStatus.OK.value, 'msg': '发送成功',
                        'data': {'auth': code, 'text': response_text}}
            else:
                return {'code': BaseHttpStatus.ERROR.value, 'msg': '发送失败',
                        'data': f"Error: Received HTTP status code {response.status_code}"}
        except Exception as e:
            return {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '发送失败', 'data': f"Exception occurred: {e}"}


if __name__ == '__main__':
    print(AuthCodeUtils.send_auth_code('15202411793'))
