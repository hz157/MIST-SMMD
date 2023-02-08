# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/clean.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 24/1/2023 下午5:57

"""
@Project: Weibo Spider
@File: Clean.py
@Author: RyanZhang
@Date: 2022-10-18
"""

import re


def CleanTopic(data):
    """
    递归清理微博话题
    :param data:
    :return:
    """
    try:
        start = data.index('#')
        end = data[start + 1:len(data)].index('#') + start
        remove = data[start:end + 2]
        data = data.replace(remove, '')
        return CleanTopic(data)
    except Exception as e:
        print(e)
        return data


def Replace(data):
    """
    清理ZWSP格式空格
    :param data:
    :return:
    """
    result = data.replace('ZWSP', '').replace('<br />', ' ').replace('<br>', ' ')
    return result


def CleanAt(data):
    """
    递归清理用户@其他用户的标签
    :param data:
    :return:
    """
    try:
        start = data.index('@')
        end = data[start + 1:len(data)].index(' ') + start
        remove = data[start:end + 2]
        data = data.replace(remove, '')
        # return CleanTopic(data)
        return CleanAt(data)
    except Exception as e:
        print(e)
        return data


# 清理Emoji表情
def CleanEmoji(data):
    """
    清理Emoji表情符号
    :param data:
    :return:
    """
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub('', data)


def CleanALabel(data):
    """
    递归清理HTML<a>标签
    :param data:
    :return:
    """
    try:
        start = data.index('<a')
        end = data[start + 1:len(data)].index('</a>') + start
        remove = data[start:end + 5]
        data = data.replace(remove, '')
        return CleanALabel(data)
    except Exception as e:
        print(e)
        return data


def CleanSpanLabel(data):
    """
    递归清理HTML<span>标签
    :param data:
    :return:
    """
    try:
        start = data.index('<span')
        end = data[start + 1:len(data)].index('</span>') + start
        remove = data[start:end + 8]
        data = data.replace(remove, '')
        return CleanSpanLabel(data)
    except Exception as e:
        print(e)
        return data


def CleanBracket(data):
    """
    递归清理【】标签
    :param data:
    :return:
    """
    try:
        start = data.index('【')
        end = data[start + 1:len(data)].index('】') + start
        remove = data[start:end + 2]
        data = data.replace(remove, '')
        return CleanBracket(data)
    except Exception as e:
        print(e)
        return data


def CleanChar(data):
    return CleanBracket(CleanAt(CleanTopic(data)))


def CleanHTML(data):
    return CleanSpanLabel(CleanALabel(data))


def CleanOther(data):
    return CleanEmoji(Replace(data))


def CleanData(data):
    return CleanChar(CleanHTML(CleanOther(data)))
