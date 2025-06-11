"""
@Author: zhang_zhiyi
@Date: 2025/5/15_9:11
@FileName:wechat_sync.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 微信公众号定时任务
"""
import os
import sys
import time
from datetime import datetime

# 获取当前脚本路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 假设 utils 在项目上一层 adminProject 目录中
project_root = os.path.dirname(current_dir)

# 加入项目根目录到 sys.path，保证能导入 utils.*
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.util_log import LogUtils
from utils.util_wechat import WechatUtils
from utils.util_database import DBUtils

logger = LogUtils.get_logger(name='wechat_logger', log_dir='wecaht_log', file_name='wechat_sync')

# 数据库连接对象
dub = DBUtils()
con = dub.connection()
con.autocommit(False)


def insert_into_temp(users):
    """
    用户信息插入临时表
    """
    with con.cursor() as cursor:
        cursor.execute("TRUNCATE wechat_user_temp")
        for user in users:
            cursor.execute("""
                INSERT INTO wechat_user_temp (OffAccOpenID, UnionID, SubscribeTime) VALUES (%s, %s, %s)
            """, (
                user.get('openid'),
                user.get('unionid'),
                datetime.fromtimestamp(user.get('subscribe_time', time.time()))
            ))
        con.commit()


def sync_main_table():
    """
    同步更新用户表
    """
    with con.cursor() as cursor:
        # 更新已有用户
        cursor.execute("""
            UPDATE user u
            JOIN wechat_user_temp t ON u.UnionID = t.UnionID
            SET
                u.UnionID = t.UnionID,
                u.OffAccOpenID = t.OffAccOpenID,
                u.SubscribeTime = T.SubscribeTime,
                u.SubscribeStatus = 'subscribed'
        """)
        # 删除取关用户（逻辑删除
        cursor.execute("""
            UPDATE user
            SET SubscribeStatus = 'unsubscribed'
            WHERE UnionID NOT IN (SELECT UnionID FROM wechat_user_temp)
        """)
        # 添加新增用户
        cursor.execute("""
            UPDATE user u 
            JOIN wechat_user_temp t ON u.UnionID = t.UnionID
            SET
                u.OffAccOpenID = t.OffAccOpenID,
                u.SubscribeStatus = 'subscribed'
            WHERE u.OffAccOpenID IS NULL
        """)
        con.commit()


def main():
    try:
        logger.info("定时任务启动")
        access_token = WechatUtils.get_access_token()
        openids = WechatUtils.get_user_list(access_token)

        # 获取已关注的用户信息
        users = []
        for i, openid in enumerate(openids):
            user_info = WechatUtils.get_user_unionid(access_token, openid)
            if user_info.get('subscribe', 0) == 1:
                users.append(user_info)
            time.sleep(0.05)  # 防止QPS限制

        logger.info("成功访问微信接口")

        # 插入临时表
        insert_into_temp(users)

        logger.info(f"临时成功插入{len(users)}条数据")

        # 同步数据
        sync_main_table()
        logger.info("正式表同步成功")
    except Exception as e:
        logger.error(f"出现异常{str(e)}", exc_info=True)
        if con:
            con.rollback()
    finally:
        if con:
            DBUtils.close_connection(con)


if __name__ == '__main__':
    main()
