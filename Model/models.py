# coding: utf-8
import datetime

from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, LONGTEXT, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from Utils.logutils import LogUtils

logutils = LogUtils()

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    screen_name = Column(String(255), comment='用户名称')
    profile_image_url = Column(TEXT, comment='用户头像URL')
    profile_url = Column(TEXT, comment='用户主页')
    statuses_count = Column(Integer, comment='微博数量')
    verified = Column(Integer, comment='认证状态 boolean')
    verified_type = Column(Integer, comment='认证类型')
    verified_type_ext = Column(Integer, comment='【未知】认证相关字段')
    verified_reason = Column(LONGTEXT, comment='认证说明')
    close_blue_v = Column(Integer, comment='蓝V boolean')
    description = Column(LONGTEXT, comment='用户描述')
    gender = Column(VARCHAR(10), comment='用户性别')
    follow_count = Column(Integer, comment='关注数量')
    followers_count = Column(Integer, comment='粉丝数量')


class Article(Base):
    __tablename__ = 'article'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, comment='发布时间')
    edit_count = Column(Integer, comment='编辑次数')
    edit_at = Column(DateTime, comment='编辑时间')
    show_additional_indication = Column(Integer, comment='显示条件指示')
    text = Column(LONGTEXT, comment='文章内容')
    textLength = Column(Integer, comment='文章长度')
    source = Column(VARCHAR(50), comment='文章来源')
    pic_num = Column(Integer, comment='图片数量')
    region_name = Column(String(50), comment='区域名称')
    status_title = Column(LONGTEXT, comment='标题')
    type = Column(String(50), comment='页面类型')
    page_url = Column(TEXT, comment='页面URL')
    page_title = Column(LONGTEXT, comment='页面标题')
    title = Column(LONGTEXT)
    content1 = Column(LONGTEXT)
    content2 = Column(LONGTEXT)
    video_orientation = Column(String(255), comment='视频方向')
    play_count = Column(Integer, comment='播放次数')
    reposts_count = Column(Integer, comment='转发数')
    comments_count = Column(Integer, comment='评论数')
    reprint_cmt_count = Column(Integer, comment='【未知】')
    attitudes_count = Column(Integer, comment='点赞数')
    pending_approval_count = Column(Integer, comment='等待审批数')
    user = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                  comment='用户')
    datetime = Column(DateTime, comment='写入时间')
    spider_keyword = Column(String(255), comment='爬虫关键字')
    server_ip = Column(String(255), comment='服务器IP')
    user1 = relationship('User')


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True)
    article = Column(ForeignKey('article.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                     comment='微博文章')
    path = Column(TEXT, nullable=False, comment='文件路径')
    type = Column(Enum('image', 'video'), nullable=False, server_default=text("'image'"), comment='文件类型')
    size = Column(Integer, comment='文件大小')
    original = Column(TEXT, comment='原地址')

    article1 = relationship('Article')


class Task(Base):
    __tablename__ = 'task'

    id = Column(BigInteger, primary_key=True)
    keyword = Column(String(255), comment='关键字')
    current = Column(Integer, comment='当前页', default=1)
    page_count = Column(Integer, comment='总页数')
    priority = Column(Integer, comment='优先级')
    deadline = Column(DateTime, comment='查询起始时间')
    current_time = Column(DateTime, comment='当前查询的时间')
    work_start = Column(DateTime, comment='开始时间')
    work_end = Column(DateTime, comment='结束时间')
    status = Column(Integer, comment='状态')


def DictConvertORM(data, type: str):
    try:
        if type == "user":
            orm = User()
            orm.id = data['id']
            orm.screen_name = data['screen_name']
            orm.profile_image_url = data['profile_image_url']
            orm.profile_url = data['profile_url']
            orm.statuses_count = data['statuses_count']
            orm.verified = data['verified']
            orm.verified_type = data['verified_type']
            orm.verified_type_ext = data['verified_type_ext']
            orm.verified_reason = data['verified_reason']
            orm.close_blue_v = data['close_blue_v']
            orm.description = data['description']
            orm.gender = data['gender']
            orm.follow_count = data['follow_count']
            orm.followers_count = data['followers_count']
        elif type == "article":
            orm = Article()
            orm.id = data['id']
            orm.created_at = data['created_at']
            orm.edit_count = data['edit_count']
            orm.edit_at = data['edit_at']
            orm.show_additional_indication = data['show_additional_indication']
            orm.text = data['text']
            orm.textLength = data['textLength']
            orm.source = data['source']
            orm.pic_num = data['pic_num']
            orm.region_name = data['region_name']
            orm.status_title = data['status_title']
            orm.type = data['type']
            orm.page_url = data['page_url']
            orm.page_title = data['page_title']
            orm.title = data['title']
            orm.content1 = data['content1']
            orm.content2 = data['content2']
            orm.play_count = data['play_count']
            orm.reposts_count = data['reposts_count']
            orm.comments_count = data['comments_count']
            orm.reprint_cmt_count = data['reprint_cmt_count']
            orm.attitudes_count = data['attitudes_count']
            orm.pending_approval_count = data['pending_approval_count']
            orm.user = data['user']
            orm.datetime = datetime.datetime.now()
            orm.spider_keyword = data['spider_keyword']
            orm.server_ip = data['server_ip']
        return orm
    except Exception as e:
        logutils.error(e)
