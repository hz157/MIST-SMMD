# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: client_dev
# @FileName: config.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 3/2/2023 下午10:59
import configparser
import os

from utils.logutils import LogUtils

logger = LogUtils()


def writeConfig(section, option, data):
    """
    Write ini file
    :param section: ini section
    :param option: ini option
    :param data: ini value
    :return:
    """
    try:
        config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            config.add_section(section)
            config.set(section, option, data)
            config.write(open('config.ini', "w"))
        else:
            config.read('config.ini', encoding="utf-8")
            config.set(section, option, data)
            config.write(open('config.ini', "w"))
        logger.info(f"write config, section: {section}, option: {option}")
    except Exception as e:
        logger.error(e)
        return False
    return True


def readConfig(section, option):
    """
    Read ini file
    :param section:
    :param option:
    :return:
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding="utf-8")
        return config[section][option]
    except Exception as e:
        logger.error(e)
    return None
