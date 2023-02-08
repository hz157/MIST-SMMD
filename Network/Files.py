# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: Network/Files
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午5:13
import json
import os
import urllib
import requests

from Config import config
from Model import Article
from Utils.clean import CleanData
from Utils.logutils import LogUtils

logutils = LogUtils()


def DownloadWeiboImage(pid):
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


def DownloadWeiboVideo(mid, url):
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


def SaveJsonData(dbList: Article):
    cleanList = []
    for i in dbList:
        if i is not None or i != "":
            cleanList.append(CleanData(i.text))
    Note = open('static/output/data.txt', 'a', encoding="utf-8")
    line = 1
    for i in cleanList:
        dataDic = {"id": line, "text": i}
        line = line + 1
        jsonData = json.dumps(dataDic, ensure_ascii=False)
        Note.write(f'{jsonData}\n')  # \n 换行符
    Note.close  # 关闭文件