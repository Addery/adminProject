"""
@Author: zhang_zhiyi
@Date: 2025/4/21_15:38
@FileName:util_picture.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 
"""
import base64
import io

import cv2
import numpy as np
from PIL.Image import Image


class IMGUtils(object):

    @staticmethod
    def img_path2base64(path: str):
        with open(path, "rb") as image_file:
            image_bytes = image_file.read()
            base64_data = base64.b64encode(image_bytes)
            base64_string = base64_data.decode("utf-8")
        return base64_string

    @staticmethod
    def img2base64(image: Image, image_format="PNG"):
        buffered = io.BytesIO()  # 创建一个字节流对象
        image.save(buffered, format=image_format)  # 将图像保存到字节流
        img_byte_array = buffered.getvalue()  # 获取字节数据
        base64_data = base64.b64encode(img_byte_array)
        base64_string = base64_data.decode("utf-8")
        return base64_string

    @staticmethod
    def base642image(base64_string):
        image_data = base64.b64decode(base64_string)
        np_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        return img
