# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/temp_config.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午12:10
import configparser
import os

from Config import config as system_config
from Utils.logutils import LogUtils

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
        if not os.path.exists(system_config.temp_config_path):
            config.add_section(section)
            config.set(section, option, data)
            config.write(open(system_config.temp_config_path, "w"))
        else:
            config.read(system_config.temp_config_path, encoding="utf-8")
            config.set(section, option, data)
            config.write(open(system_config.temp_config_path, "w"))
        logger.info(f"Write temp config file (section: {section}, option: {option}, value: {data})")
    except Exception as e:
        logger.error(e)
    return None


def readConfig(section, option):
    """
    Read ini file
    :param section:
    :param option:
    :return:
    """
    try:
        config = configparser.ConfigParser()
        config.read(system_config.temp_config_path, encoding="utf-8")
        logger.info(f"Read temp config file (section: {section}, option: {option})")
        return config[section][option]
    except Exception as e:
        logger.error(e)
    return None
