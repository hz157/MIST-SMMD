# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: Network/Files
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午5:13
import os
import urllib

import requests

from Config import config
from Utils.logutils import LogUtils

logutils = LogUtils()


def downloadWeiboImage(pid):
    try:
        IMAGE_URL = f"{config.Sina_OrgImage_Url}{pid}.jpg"
        r = requests.get(IMAGE_URL)
        path = f'{config.images_root_path}/{pid}.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)
        if os.path.exists(path):
            return os.path.getsize(path)
        else:
            return None
    except Exception as e:
        logutils.error(e)
    return None


def downloadWeiboVideo(mid, url):
    try:
        path = f'{config.video_root_path}/{mid}.mp4'
        urllib.request.urlretrieve(url, path)
        if os.path.exists(path):
            return os.path.getsize(path)
        else:
            return None
    except Exception as e:
        logutils.error(e)
    return None
