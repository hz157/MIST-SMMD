# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: mist
# @FileName: config
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 3/3/2023 上午10:31

"""
    集中配置文件
"""

# BAIDU API
BAIDU_API_HOST = 'https://api.map.baidu.com'  # 百度地图开放平台 URL
BAIDU_API_AK = ''  # 百度地图开放平台访问密钥

# GOOGLE API


# TENCENT API
TENCENT_API_HOST = 'https://apis.map.qq.com'
TENCENT_API_KEY = ''
TENCENT_API_SK = ''


# LOCAL FILE PATH
ORIGINAL_CSV_PATH = r'test/test_raw_data.csv'
SAVE_CSV_PATH = r'test/dateset.csv'

# KEYWORD
TIME_REVERSE_KEYWORD = ['分', '秒', '近', '又', '日前', "几", "最近", "春", "夏", "秋", "冬"]  # 时间相关反向关键字
FAC_REVERSE_KEYWORD = ['消防', '派出所']