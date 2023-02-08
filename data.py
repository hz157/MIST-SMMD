# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: dev
# @FileName: data
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 6/2/2023 下午3:58
import json
from enum import Enum

from Database.Mysql import Mysql
from Model.models import Article
from Utils.clean import CleanData


class CleanStatus(Enum):
    """
    文本数据状态枚举
    """
    unclean = 0,
    clean = 1


class ArticleColumn(Enum):
    """
    文章数据字段枚举
    """
    id = "id",
    create_at = 'create_at',
    edit_count = 'edit_count',
    edit_at = 'edit_at',
    show_additional_indication = 'show_additional_indication',
    text = 'text',
    textLength = 'textLength',
    source = 'source',
    pic_num = 'pic_num',
    region_name = 'region_name',
    status_title = 'status_title',
    type = 'type',
    page_url = 'page_url',
    page_title = 'page_title',
    title = 'title',
    content1 = 'content1',
    content2 = 'content2',
    video_orientation = 'video_orientation',
    play_count = 'play_count',
    reposts_count = 'reposts_count',
    comments_count = 'comments_count',
    reprint_cmt_count = 'reprint_cmt_count',
    attitudes_count = 'attitudes_count',
    pending_approval_count = 'pending_approval_count',
    user = 'user',
    datetime = 'datetime',
    spider_keyword = 'spider_keyword',
    server_ip = 'server_ip',


def SaveJsonData(dbList: Article):
    cleanList = []
    for i in dbList:
        if i is not None or i != "":
            cleanList.append(CleanData(i.text))
    Note = open('static/output/data1.txt', 'a', encoding="utf-8")
    line = 1
    for i in cleanList:
        dataDic = {"id": line, "text": i}
        line = line + 1
        jsonData = json.dumps(dataDic, ensure_ascii=False)
        Note.write(f'{jsonData}\n')  # \n 换行符
    Note.close  # 关闭文件


def getData(keyword: str = None, type: CleanStatus = CleanStatus.unclean, columns: list = None):
    """
    获取数据
    :param keyword: 关键字 默认返回全部
    :param type: 数据类型，CleanStatus枚举
    :param columns: 数据字段，使用list, 载荷ArticleColumn枚举
    :return: json数据
    """
    session = Mysql()
    if keyword is None:
        articleList = session.query(Article).filter().all()
    else:
        articleList = session.query(Article).filter(Article.spider_keyword == keyword).all()
    data = []
    for artilce in articleList:
        temp = {}
        for column in columns:
            if column == ArticleColumn.id: temp['id'] = artilce.id
            if column == ArticleColumn.create_at: temp['create_at'] = str(artilce.created_at)
            if column == ArticleColumn.edit_count: temp['edit_count'] = artilce.edit_count
            if column == ArticleColumn.edit_at: temp['edit_at'] = artilce.edit_at
            if column == ArticleColumn.show_additional_indication: temp[
                'show_additional_indication'] = artilce.show_additional_indication
            if column == ArticleColumn.text:
                temp['text'] = artilce.text if type == CleanStatus.unclean else CleanData(artilce.text)
            if column == ArticleColumn.textLength: temp['textLength'] = artilce.textLength
            if column == ArticleColumn.source: temp['source'] = artilce.source
            if column == ArticleColumn.pic_num: temp['pic_num'] = artilce.pic_num
            if column == ArticleColumn.region_name: temp['region_name'] = artilce.region_name
            if column == ArticleColumn.status_title: temp['status_title'] = artilce.status_title
            if column == ArticleColumn.type: temp['type'] = artilce.type
            if column == ArticleColumn.page_url: temp['page_url'] = artilce.page_url
            if column == ArticleColumn.page_title: temp['page_title'] = artilce.page_title
            if column == ArticleColumn.title: temp['title'] = artilce.title
            if column == ArticleColumn.content1: temp['content1'] = artilce.content1
            if column == ArticleColumn.content2: temp['content2'] = artilce.content2
            if column == ArticleColumn.video_orientation: temp['video_orientation'] = artilce.video_orientation
            if column == ArticleColumn.play_count: temp['play_count'] = artilce.play_count
            if column == ArticleColumn.reposts_count: temp['reposts_count'] = artilce.reposts_count
            if column == ArticleColumn.comments_count: temp['comments_count'] = artilce.comments_count
            if column == ArticleColumn.reprint_cmt_count: temp['reprint_cmt_count'] = artilce.reprint_cmt_count
            if column == ArticleColumn.attitudes_count: temp['attitudes_count'] = artilce.attitudes_count
            if column == ArticleColumn.pending_approval_count: temp[
                'pending_approval_count'] = artilce.pending_approval_count
            if column == ArticleColumn.user: temp['user'] = artilce.user
            if column == ArticleColumn.datetime: temp['datetime'] = artilce.datetime
            if column == ArticleColumn.spider_keyword: temp['spider_keyword'] = artilce.spider_keyword
            if column == ArticleColumn.server_ip: temp['server_ip'] = artilce.server_ip
        data.append(temp)
    return data


data = getData("同安内涝", CleanStatus.clean, [ArticleColumn.id, ArticleColumn.text, ArticleColumn.create_at])
for i in data:
    print(i)
