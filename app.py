# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: app.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午9:55
import sys
import datetime
from enum import Enum

from Database.Mysql import Mysql
from Model.models import Task, Article, User, Media, DictConvertORM
from Network.Sina import *
from Utils import timeutlis
from Utils.clean import CleanData
from Utils.logutils import LogUtils
from Utils.nlputils import translate_zh_en, relevant

logutils = LogUtils()


class MediaType(Enum):
    Image = 0,
    Video = 1


def main(task):
    logutils.info("Spider Start Working")
    isOverflow = True
    # task start work datetime
    if task.work_start is None:
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
        task.page_count = getArticlePagesByKeyword(task.keyword, task.current_time)  # get page count
        for i in range(task.current, task.page_count + 1):
            task.current = i
            session.add(task)
            mids = getArticleMidsByKeyword(task.current_time, task.keyword, i)
            if mids is None:
                logutils.error("Weibo pc cookie invalid")
            for j in mids:
                # Random delay 1-10s 随机延时1-3s
                # timeutlis.sleep(1, 3)
                response = getArticlePageInfo(j)
                if response is None:
                    logutils.error("Weibo mobile cookie invalid")
                    return
                UserInfo = getUserInfo(response)
                ArticleInfo = getArticleInfo(response)
                try:
                    ArticleInfo['spider_keyword'] = task.keyword
                    ArticleInfo['server_name'] = config.server_name
                    ArticleInfo['clean_text'] = CleanData(ArticleInfo['text'])
                    ArticleInfo['relevant'] = relevant(translate_zh_en(ArticleInfo['clean_text']))
                except Exception as e:
                    logutils.error(e)
                Images = getArticleImage(response)
                Video = getArticleVideo(response)
                # Query whether there is article data in the database   查询数据库中是否有文章数据
                if session.query(Article).filter(Article.id == j).first() is None:
                    # Construct article orm object - Article    构造文章ORM对象
                    article = DictConvertORM(ArticleInfo, table="article")
                    try:
                        # Query whether there is user data in the database  查询数据库中是否有用户数据
                        user = session.query(User).filter(User.id == UserInfo['id']).first()
                        if user is None:
                            # Construct user ORM object 构造用户ORM对象
                            user = DictConvertORM(UserInfo, table='user')
                        else:
                            user = DictConvertORM(UserInfo, table='update_user', obj1=[user])
                        session.add(user)
                        session.add(article)
                        # Judge whether there are pictures  判断是否有图片
                        if len(Images) != 0:
                            for image in Images:
                                media = Media(article=ArticleInfo['id'], path=None, type="image", size=None,
                                              original=config.Sina_OrgImage_Url + image + ".jpg")
                                session.add(media)
                            # DownloadMedia(session, Images, ArticleInfo['id'], MediaType.Image)
                        # Judge whether there are video  判断是否有视频
                        if Video is not None:
                            media = Media(article=ArticleInfo['id'], path=None, type="video", size=None, original=Video)
                            session.add(media)
                            # DownloadMedia(session, Video, ArticleInfo['id'], MediaType.Video)
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



if __name__ == '__main__':
    logutils.info("Python Start")
    session = Mysql()
    # dblist = session.query(Article).filter(Article.spider_keyword == "山洪").all()
    # SaveCsvData(dblist)
    while True:
        try:
            session = Mysql()
            task = session.query(Task).filter(Task.status == 0).order_by(Task.priority).first()
            session.close()
            main(task)
        except Exception as e:
            logutils.error(e)
