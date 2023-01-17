# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: app.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午9:55
import sys

from Database import *
from Model import *
from Network import *
from Utils import timeutlis
from Utils.logutils import LogUtils

logutils = LogUtils()


def main(keyword):
    logutils.info("Spider Start Working")
    session = Mysql()
    pages = getArticlePagesByKeyword(keyword)
    if pages == -1:
        logutils.error("Weibo pc cookie invalid")
    for i in range(0, pages):
        for j in getArticleMidsByKeyword(keyword, i + 1):
            # Random delay 1-10s 随机延时1-10s
            timeutlis.sleep(1, 10)
            response = getArticlePageInfo(j)
            if response is None:
                logutils.error("Weibo mobile cookie invalid")
            UserInfo = getUserInfo(response)
            ArticleInfo = getArticleInfo(response)
            try:
                ArticleInfo['spider_keyword'] = keyword
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
                    # 后面改异步执行 后面改异步执行 后面改异步执行 后面改异步执行
                    # Judge whether there are pictures  判断是否有图片
                    if len(Images) != 0:
                        # Traverse pictures 遍历图片
                        for x in Images:
                            size = downloadWeiboImage(x)
                            # Judge whether the download is successful  判断是否下载成功
                            if size is not None:
                                # Construct media orm object - Article    构造媒体ORM对象
                                media = Media(article=ArticleInfo['id'], path=x + '.jpg', type="image", size=size,
                                              original=config.Sina_OrgImage_Url + x + ".jpg")
                                session.add(media)
                    # 后面改异步执行 后面改异步执行 后面改异步执行 后面改异步执行
                    # Judge whether there are video  判断是否有视频
                    if Video is not None:
                        size = downloadWeiboVideo(ArticleInfo['id'], Video)
                        # Judge whether the download is successful  判断是否下载成功
                        if size is not None:
                            # Construct media orm object - Article    构造媒体ORM对象
                            media = Media(article=ArticleInfo['id'], path=str(ArticleInfo['id']) + '.mp4', type="video",
                                          size=size, original=Video)
                            session.add(media)
                    session.add(article)
                    session.commit()
                except Exception as e:
                    logutils.error(e)
    session.close()


if __name__ == '__main__':
    logutils.info("Python Start")
    keyword_list = ['集美天气', '思明天气']
    for i in keyword_list:
        main(i)
    logutils.error("Python End")
