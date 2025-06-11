"""
@Author: zhang_zhiyi
@Date: 2025/5/15_11:05
@FileName:test_log.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
from utils.util_log import LogUtils


# 获取 logger 实例
logger = LogUtils.get_logger('test_logger', 'test_log', 'test_log')

# 示例
logger.info("定时任务启动")
logger.warning("这是一条警告")
# logger.error("出现异常", exc_info=True)
