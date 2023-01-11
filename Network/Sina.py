# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Network/Sina.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午11:59
import json

import requests

from bs4 import BeautifulSoup


from Config import config
from Utils import temp_config
from Utils.convert import CNConvertInt, UTCConvertFormat
from Utils.logutils import LogUtils

logutils = LogUtils()


def getArticlePagesByKeyword(keyword: None):
    """
    Get Sina Weibo Article Page Count
    :param keyword: Article keyword
    :return: page count-int
    """
    logutils.info(f"Start requesting article pages by keyword (keyword: {keyword})")
    try:
        url = f"{config.Sina_PC_URL}{keyword}&nodup=1"
        head = config.Sina_PC_Header
        head['cookie'] = temp_config.readConfig("cookie", "pc")
        data = requests.get(url=url, headers=head).text
        # load bs4
        soup = BeautifulSoup(data, features="html.parser")
        # find div
        page_div = str(soup.findAll("ul", attrs={"action-type": "feed_list_page_morelist"})).split('\n')
        pages = len(page_div) - 2
        logutils.info(f"keyword: {keyword}, page count: {pages}")
        return pages
    except Exception as e:
        logutils.error(e)
    return None


def getArticleMidsByKeyword(keyword: None, page: int):
    """
    Get Sina Weibo Article Mids
    :param keyword: Article keyword
    :param page: Article Keyword Page
    :return: mid-List
    """
    logutils.info(f"Start requesting article id by keyword (keyword: {keyword}, page: {page})")
    try:
        url = f"{config.Sina_PC_URL}{keyword}&page={str(page)}"
        header = config.Sina_PC_Header
        header['cookie'] = temp_config.readConfig("cookie", "pc")
        data = requests.get(url=url, headers=header).text
        # load bs4
        soup = BeautifulSoup(data, features="html.parser")
        # find div
        div = soup.findAll("div", attrs={"action-type": "feed_list_item"})
        mids = []
        count = 0
        for i in div:
            mid = i.get("mid")
            mids.append(mid)
            count = count + 1
        logutils.info(f"keyword: {keyword}, page: {page}, data count: {count}")
        return mids
    except Exception as e:
        logutils.error(e)
    return None


def getArticlePageInfo(mid: str):
    logutils.info(f"Start requesting article page info (mid: {mid})")
    try:
        url = f"{config.Sina_Mobile_URL}{mid}"
        header = config.Sina_Mobile_Header
        header['cookie'] = temp_config.readConfig("cookie", "mobile")
        session = requests.Session()
        res = session.get(url=url, headers=header, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        script = soup.find_all('script')[2].text
        temps = script.split("var $render_data = [")[1].split("][0] || {};")[0]
        return json.loads(temps).get('status')
    except Exception as e:
        logutils.error(e)
    return None


def getUserInfo(data: dict):
    """
    Get UserInfo
    :param data: web response dict
    :return: userinfo-dict
    """
    try:
        data = data.get('user')
        result = {'id': analysisResponseDict(data, 'id', type='int'),
                  'screen_name': analysisResponseDict(data, 'screen_name'),
                  'profile_image_url': analysisResponseDict(data, 'profile_image_url'),
                  'profile_url': analysisResponseDict(data, 'profile_url'),
                  'statuses_count': analysisResponseDict(data, 'statuses_count', type='cvi'),
                  'verified': 1 if analysisResponseDict(data, 'verified') is True else 0,
                  'verified_type': analysisResponseDict(data, 'verified_type', type='cvi'),
                  'verified_type_ext': analysisResponseDict(data, 'verified_type_ext', type='cvi'),
                  'verified_reason': analysisResponseDict(data, 'verified_reason'),
                  'close_blue_v': 1 if analysisResponseDict(data, 'close_blue_v') is True else 0,
                  'description': analysisResponseDict(data, 'description'),
                  'gender': analysisResponseDict(data, 'gender'),
                  'follow_count': analysisResponseDict(data, 'follow_count', type='cvi'),
                  'followers_count': analysisResponseDict(data, 'followers_count', type='cvi')}
        return result
    except Exception as e:
        logutils.error(e)
    return None


def getArticleInfo(data: dict):
    """
    Get ArticleInfo
    :param data: web response dict
    :return: article-dict
    """
    try:
        result = {'id': analysisResponseDict(data, 'id', type='int'),
                  'created_at': analysisResponseDict(data, 'created_at', type='time'),
                  'edit_count': analysisResponseDict(data, 'edit_count', type='cvi'),
                  'edit_at': analysisResponseDict(data, 'edit_at', type='time'),
                  'show_additional_indication': analysisResponseDict(data, 'show_additional_indication', type='cvi'),
                  'text': analysisResponseDict(data, 'text'),
                  'textLength': analysisResponseDict(data, 'textLength', type='cvi'),
                  'source': analysisResponseDict(data, 'source'),
                  'pic_num': analysisResponseDict(data, 'pic_num', type='cvi'),
                  'region_name': analysisResponseDict(data, 'region_name'),
                  'status_title': data.get('status_title'),
                  'type': analysisResponseDict(data,'page_info', 'type'),
                  'page_url': analysisResponseDict(data, 'page_info', 'page_url'),
                  'page_title': analysisResponseDict(data, 'page_info', 'page_title'),
                  'title': analysisResponseDict(data, 'page_info', 'title'),
                  'content1': analysisResponseDict(data, 'page_info', 'content1'),
                  'content2': analysisResponseDict(data, 'page_info', 'content2'),
                  'video_orientation': analysisResponseDict(data, 'page_info', 'video_orientation'),
                  'reposts_count': analysisResponseDict(data, 'reposts_count', type='cvi'),
                  'comments_count': analysisResponseDict(data, 'comments_count', type='cvi'),
                  'reprint_cmt_count': analysisResponseDict(data, 'reprint_cmt_count', type='cvi'),
                  'attitudes_count': analysisResponseDict(data, 'attitudes_count', type='cvi'),
                  'pending_approval_count': analysisResponseDict(data, 'pending_approval_count', type='cvi'),
                  'play_count': analysisResponseDict(data, 'page_info', 'play_count', type='cvi'),
                  'user': analysisResponseDict(data, 'user', 'id')}
        return result
    except Exception as e:
        logutils.error(e)
    return None


def getArticleImage(data: dict):
    """
    Get Article Image
    :param data: web response dict
    :return: images-dict
    """
    try:
        pics = analysisResponseDict(data, 'pic_ids')
        if pics is not None:
            return pics
        return None
    except Exception as e:
        logutils.error(e)
    return None


def getArticleVideo(data: dict):
    """
    Get Article Video
    :param data: web response dict
    :return: video-dict
    """
    try:
        video = data.get("page_info").get("urls").get("mp4_hd_mp4")
        if video is not None:
            return video
        return None
    except Exception as e:
        logutils.error(e)
    return None


def analysisResponseDict(data: dict, option1: str, option2: str = None, type: str ="str"):
    try:
        if type == "int" and option1 is not None and option2 is not None:
            return int(data.get(option1).get(option2))
        elif type == "int" and option2 is None:
            return int(data.get(option1))
        elif type == "cvi" and option1 is not None and option2 is not None:
            return CNConvertInt(str(data.get(option1).get(option2)))
        elif type == "cvi" and option2 is None:
            return CNConvertInt(str(data.get(option1)))
        elif type == "time" and option1 is not None and option2 is not None:
            return UTCConvertFormat(str(data.get(option1).get(option2)))
        elif type == "time" and option2 is None:
            return UTCConvertFormat(str(data.get(option1)))
        elif option1 is not None and option2 is not None:
            return data.get(option1).get(option2)
        else:
            return data.get(option1)
    except Exception as e:
        logutils.error(e)
    return None

