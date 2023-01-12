# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/logutils
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午11:19
import os
import sys

from loguru import logger

from Config import config


class LogUtils:
    """
    Log Module
    """

    def __new__(cls, *args, **kwargs):
        """
        Initialize
        :param args:
        :param kwargs:
        """
        # 解决重复打印
        logger.remove()
        logger.add(sys.stderr, level="INFO")

        logFilepath = config.Logger_root_path
        # 判断目录是否存在,不存在则创建新的目录
        if not os.path.isdir(logFilepath):
            os.makedirs(logFilepath)

        logger.add(
            logFilepath + "/{time:YYYY-MM-DD}.log",  # 指定文件
            format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | Process:{process.name}:{process.id} "
                   "| Thread:{thread.name}:{thread.id} | {file.path}:{line} | {message}",
            encoding="utf-8",
            rotation="00:00",  # 按天分割
            # serialize=True,  # 将记录的消息转化成JSON字符串
            backtrace=True,  # 回溯
            diagnose=True,  # 诊断
            enqueue=True,  # 异步写入
        )

        return logger
