# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: Network/Files
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午5:13
import datetime
import json
import os
import requests
import urllib
import uuid

from Config import config
from Utils.logutils import LogUtils

logutils = LogUtils()


def DownloadWeiboImage(pid):
    try:
        IMAGE_URL = f"{config.Sina_OrgImage_Url}{pid}.jpg"
        r = requests.get(IMAGE_URL)
        uuidCode = uuid.uuid1()
        path = f'{config.images_root_path}/{uuidCode}.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)
        if os.path.exists(path):
            return [os.path.getsize(path), uuidCode]
        else:
            return None
    except Exception as e:
        logutils.error(e)
    return None


def DownloadWeiboVideo(mid, url):
    try:
        uuidCode = uuid.uuid1()
        path = f'{config.video_root_path}/{uuidCode}.mp4'
        urllib.request.urlretrieve(url, path)
        if os.path.exists(path):
            return [os.path.getsize(path), uuidCode]
        else:
            return None
    except Exception as e:
        logutils.error(e)
    return None
