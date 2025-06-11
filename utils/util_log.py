"""
@Author: zhang_zhiyi
@Date: 2025/5/15_10:59
@FileName:util_log.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import os
import logging
from datetime import datetime

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_ROOT_PATH = os.path.join(CURRENT_PATH, '../log')


class LogUtils:
    _logger = None

    @staticmethod
    def get_logger(name, file_name, log_dir, level=logging.INFO):
        if LogUtils._logger:
            return LogUtils._logger

        log_path = os.path.join(LOG_ROOT_PATH, log_dir)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file = os.path.join(log_path, datetime.now().strftime(f"{file_name}_%Y-%m-%d.log"))

        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        LogUtils._logger = logger
        return logger
