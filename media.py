# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: mediadown
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/2/2023 下午10:39
from sqlalchemy import and_

from Database.Mysql import Mysql
from Model.models import Media
from Network.Files import DownloadWeiboVideo, DownloadWeiboImage
from Utils.logutils import LogUtils

logutils = LogUtils()


def downloadMedia():
    session = Mysql()
    media = (session.query(Media).filter(and_(Media.path == None, Media.size == None))).first()
    if media.type == 'video':
        try:
            response = DownloadWeiboVideo(media.article, media.original)
            if response is not None:
                media.size = response[0]
                media.path = response[1]
                session.add(media)
        except Exception as e:
            logutils.error(e)
    else:
        try:
            response = DownloadWeiboImage(media.original)
            if response is not None:
                media.size = response[0]
                media.path = response[1]
                session.add(media)
        except Exception as e:
            logutils.error(e)
    session.commit()
    session.close()
