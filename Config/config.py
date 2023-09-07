# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Config/config.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午11:20

import configparser
import os
import base64

from Config import dev, prop
from Utils.logutils import LogUtils

logger = LogUtils()

"""Files Path Config"""
# log root path
Logger_root_path = "D:/Project/MIDEP/logs"
# ini path
config_file_path = "Config/config.ini"
# video root path
# video_root_path = "static/video"
video_root_path = "D:/Project/MIDEP/video"
# image root path
# images_root_path = "static/image"
images_root_path = "D:/Project/MIDEP/image"


def writeConfig(section: str, option: str, data: str):
    global config_file_path
    """
    Write ini file
    :param section: ini section
    :param option: ini option
    :param data: ini value
    :return:
    """
    try:
        iniConfig = configparser.ConfigParser()
        b = bytes(data, encoding='utf-8')
        deCode = base64.b64encode(base64.b32encode(b))
        s = str(deCode, encoding='utf-8')
        isExist = False
        if not os.path.exists(config_file_path):
            iniConfig.add_section(section)
            iniConfig.set(section, option, s)
            iniConfig.write(open(config_file_path, "w"))
        else:
            if section not in iniConfig.sections():
                iniConfig.add_section(section)
            iniConfig.read(config_file_path, encoding="utf-8")
            iniConfig.set(section, option, s)
            iniConfig.write(open(config_file_path, "w"))
        logger.info(f"Write temp config file (section: {section}, option: {option}, value: {data})")
    except Exception as e:
        logger.error(e)
    return None


def readConfig(section, option):
    global config_file_path
    """
    Read ini file
    :param section:
    :param option:
    :return:
    """
    try:
        iniConfig = configparser.ConfigParser()
        iniConfig.read(config_file_path, encoding="utf-8")
        b = bytes(iniConfig[section][option], encoding='utf-8')
        s = str(base64.b32decode(base64.b64decode(b)), encoding='utf-8')
        return s
    except Exception as e:
        logger.error(e)
    return None


# from Utils import config

"""配置文件"""

# 开发环境
env = prop

server_name = readConfig('server', 'server_name')

"""Mysql Config"""
Mysql_dialect = "mysql"
Mysql_driver = "pymysql"
# Mysql_host = "127.0.0.1"
Mysql_host = readConfig('mysql', 'host')
# Mysql_port = 53306
Mysql_port = int(readConfig('mysql', 'port'))
# Mysql_username = "midep"
Mysql_username = readConfig('mysql', 'username')
# Mysql_password = "MXJKQzHCfy7qeUtm"
Mysql_password = readConfig('mysql', 'password')
# Mysql_database = "MIDEP"
Mysql_database = readConfig('mysql', 'database')
Mysql_pool_size = 8  # 数据库连接池大小 默认5 设置为0表示无限制
Mysql_pool_recycle = 60 * 30  # 数据库自动断开时间
Mysql_echo = env.Mysql_echo  # ORM转话SQL语句打印

"""Redis Config"""
Redis_host = 'localhost'
Redis_port = 6379
Redis_password = ''

"""Sina Config"""
Sina_OrgImage_Url = "https://wx3.sinaimg.cn/large/"
Sina_PC_URL = "https://s.weibo.com/weibo?q="
# Sina_PC_URL = "https://s.weibo.com/weibo?q=%E5%8E%A6%E9%97%A8%E4%B8%8B%E9%9B%A8&typeall=1&suball=1&timescope=custom%3A2023-01-05-0%3A2023-01-29-16&Refer=g&page=1"

Sina_PC_Header = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "accept": "not-source/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": readConfig('cookie', 'mobile')
}

Sina_Mobile_URL = "https://m.weibo.cn/status/"
Sina_Mobile_Header = {
    "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "accept": "not-source/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": readConfig('cookie', 'mobile')
}

Sina_Image_Header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Forwarded-For': 'localhost'
}
