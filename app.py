# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: app.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午9:55
import sys
import datetime

from Database import *
from Model import *
from Network import *
from Utils import timeutlis
from Utils.logutils import LogUtils

logutils = LogUtils()


class MediaType(Enum):
    Image = 0,
    Video = 1


def main(task):
    logutils.info("Spider Start Working")
    isOverflow = True
    # task start work datetime
    task.work_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    while isOverflow:
        session = Mysql()
        if task.current_time < task.deadline:
            task.work_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task.status = 1
            session.add(task)
            session.commit()
            session.close()
            isOverflow = False
            return None
        task.page_count = getArticlePagesByKeyword(task.current_time, task.keyword)  # get page count
        for i in range(task.current, task.page_count + 1):
            task.current = i
            session.add(task)
            mids = getArticleMidsByKeyword(task.current_time, task.keyword, i)
            if mids is None:
                logutils.error("Weibo pc cookie invalid")
            for j in mids:
                # Random delay 1-10s 随机延时1-3s
                timeutlis.sleep(1, 3)
                response = getArticlePageInfo(j)
                if response is None:
                    logutils.error("Weibo mobile cookie invalid")
                    return
                UserInfo = getUserInfo(response)
                ArticleInfo = getArticleInfo(response)
                try:
                    ArticleInfo['spider_keyword'] = task.keyword
                    ArticleInfo['server_ip'] = config.server_ip
                except Exception as e:
                    logutils.error(e)
                Images = getArticleImage(response)
                Video = getArticleVideo(response)
                # Query whether there is article data in the database   查询数据库中是否有文章数据
                if session.query(Article).filter(Article.id == j).first() is None:
                    # Construct article orm object - Article    构造文章ORM对象
                    article = DictConvertORM(ArticleInfo, type="article")
                    try:
                        # Query whether there is user data in the database  查询数据库中是否有用户数据
                        if session.query(User).filter(User.id == UserInfo['id']).first() is None:
                            # Construct user ORM object 构造用户ORM对象
                            user = DictConvertORM(UserInfo, type='user')
                            session.add(user)
                        session.add(article)
                        # 后面改异步执行 后面改异步执行 后面改异步执行 后面改异步执行
                        # Judge whether there are pictures  判断是否有图片
                        if len(Images) != 0:
                            DownloadMedia(session, Images, ArticleInfo['id'], MediaType.Image)
                        # 后面改异步执行 后面改异步执行 后面改异步执行 后面改异步执行
                        # Judge whether there are video  判断是否有视频
                        if Video is not None:
                            DownloadMedia(session, Video, ArticleInfo['id'], MediaType.Video)
                    except Exception as e:
                        logutils.error(e)
                session.commit()
        recovery(task)
        session.add(task)
        session.commit()
        session.close()
    return None


def recovery(task: Task):
    task.current = 1
    task.page_count = None
    task.current_time = (task.current_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")


def DownloadMedia(session, data, mid: str = None, type: MediaType = MediaType.Image):
    if type == MediaType.Video:
        try:
            size = DownloadWeiboVideo(mid, data)
            # Judge whether the download is successful  判断是否下载成功
            if size is not None:
                # Construct media orm object - Article    构造媒体ORM对象
                media = Media(article=mid, path=str(mid) + '.mp4',
                              type="video", size=size, original=data)
                session.add(media)
        except Exception as e:
            print(e)

    if type == MediaType.Image:
        try:
            for x in data:
                size = DownloadWeiboImage(x)
                # Judge whether the download is successful  判断是否下载成功
                if size is not None:
                    # Construct media orm object - Article    构造媒体ORM对象
                    media = Media(article=mid, path=x + '.jpg', type="image", size=size,
                                  original=config.Sina_OrgImage_Url + x + ".jpg")
                    session.add(media)
        except Exception as e:
            print(e)
    # session.close()


if __name__ == '__main__':
    logutils.info("Python Start")
    while True:
        try:
            session = Mysql()
            task = session.query(Task).filter(Task.status == 0).order_by(Task.priority).first()
            session.close()
            main(task)
        except Exception as e:
            logutils.error(e)
