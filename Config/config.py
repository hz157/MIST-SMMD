# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Config/temp_config.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午11:20

from Config import dev, prop

"""配置文件"""

# 开发环境
env = prop

server_ip = 'Virtual-Linux-Fujian'

"""Mysql Config"""
Mysql_dialect = "mysql"
Mysql_driver = "pymysql"
Mysql_host = "127.0.0.1"
Mysql_port = 53306
Mysql_username = "midep"
Mysql_password = "MXJKQzHCfy7qeUtm"
Mysql_database = "MIDEP"
Mysql_pool_size = 8  # 数据库连接池大小 默认5 设置为0表示无限制
Mysql_pool_recycle = 60 * 30  # 数据库自动断开时间
Mysql_echo = env.Mysql_echo  # ORM转话SQL语句打印

"""Files Path Config"""
# log root path
Logger_root_path = "Z:/Project/MIDEP/logs"
# ini path
temp_config_path = "Config/temp_config.ini"
# video root path
# video_root_path = "static/video"
video_root_path = "Z:/Project/MIDEP/video"
# image root path
# images_root_path = "static/image"
images_root_path = "Z:/Project/MIDEP/image"

"""Redis Config"""
Redis_host = 'localhost'
Redis_port = 6379
Redis_password = ''

"""Sina Config"""
Sina_OrgImage_Url = "https://wx3.sinaimg.cn/large/"
Sina_PC_URL = "https://s.weibo.com/weibo?q="
Sina_PC_Header = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "accept": "not-source/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": ''
}

Sina_Mobile_URL = "https://m.weibo.cn/status/"
Sina_Mobile_Header = {
    "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "accept": "not-source/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": ''}
