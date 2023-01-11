# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/timeutils.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午1:03

import time
import random
from Utils.logutils import LogUtils

logutils = LogUtils()


def sleep(min: int, max: int):
    """
    Delay sleep
    :param min: min time
    :param max: max time
    :return: None
    """
    try:
        t = random.randint(min, max)
        logutils.info(f"delay sleep: {t}s")
        sleepCountDown(t)
    except Exception as e:
        logutils.error(e)


def sleepCountDown(duration: int):
    while duration > 0:
        print(f"thread sleep count down: {duration}s")
        time.sleep(1)
        duration = duration - 1


