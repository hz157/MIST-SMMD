# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: mist
# @FileName: standardizing
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 3/3/2023 下午12:50
import jionlp as jio

from config import config
from unit.status import TimeStandardStatus, SpaceStandardStatus


def time_standardization(nerTimeFormat, rawTimeFormat):
    """
        时间语义解析， 采用jionlp.parse_time
        https://github.com/dongrixinyu/JioNLP/wiki/%E6%97%B6%E9%97%B4%E8%AF%AD%E4%B9%89%E8%A7%A3%E6%9E%90-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3#user-content-%E6%97%B6%E9%97%B4%E8%AF%AD%E4%B9%89%E8%A7%A3%E6%9E%90
    Args:
        nerTimeFormat:  spacy 所检测到的时间
        rawTimeFormat:  微博数据原生的时间

    Returns:    param1：标准化后的时间  param2：标准化的结果

    """
    rawSplit = rawTimeFormat.split("/")  # 时间切割
    for word in config.TIME_REVERSE_KEYWORD:  # 时间相关反向关键字，修改config/config.py
        if word in rawTimeFormat:   # 遍历原生格式字符串
            return rawTimeFormat, TimeStandardStatus.unrecognized  # 未识别到标准化时间
    try:
        parseTime = jio.parse_time(nerTimeFormat,
                                   time_base={'year': int(rawSplit[0]),
                                              'month': int(rawSplit[1]),
                                              'day': int(rawSplit[2].split[0])})
        # time_base 参数其指解析时间时指定的时间基点
    except Exception as e:  # 异常捕获
        print(e)
        return rawTimeFormat, TimeStandardStatus.unrecognized  # 未识别到标准化时间
    # jionlp 提供了4种 type, 该项目只采用其中两种，分别为 time_point 和 time_span 时间点和时间间隔
    if parseTime['type'] == 'time_point' or parseTime['type'] == 'time_span':
        return parseTime['time'][0], parseTime['type']  # 返回表追时间及其jionlp所返回的时间类型 time_point(时间点) 或是 time_span(时间间隔)
    else:
        return rawTimeFormat, TimeStandardStatus.non_standardized  # 没有标准化时间


def create_full_space(data):
    locSet = []
    loc = ''
    status = []
    for item in data:
        for f in item["full_location"]:
            if f not in item['orig_location']:  # 去重
                loc += f
        if len(loc) == 1:  # 如果是单字（省、市、区）直接返回
            return locSet, SpaceStandardStatus.invalid
        if item['full_location'] == item['orig_location']:
            if item['county'] is None:
                status.append(SpaceStandardStatus.miss_country)  # 丢失国家信息
            elif item['city'] is None:
                status.append(SpaceStandardStatus.miss_city)  # 丢失城市信息
            elif item['province'] is None:
                status.append(SpaceStandardStatus.miss_province)  # 丢失省份信息
            locSet.append(item['full_location'])
            continue
        else:
            status.append(SpaceStandardStatus.accurate)
            locSet.append(item['full_location'])
    return locSet, status


def spacy_standization(labelData, rawData):
    locSet = []
    if 'GPE' not in labelData.keys():
        if len(rawData['region']) == 0:
            return [], SpaceStandardStatus.miss_gpe
        GPE = rawData['region']
        for item in labelData['FAC']:
            locSet.append(jio.parse_location(GPE + item, change2new=True, town_village=True))
        locSet, status = create_full_space(locSet)
        if not locSet:
            return locSet, SpaceStandardStatus.common
        else:
            return locSet, "返回个寂寞"
    elif 'GPE' in labelData.keys():
        flag = 0
        region = ''
        for item in labelData['GPE']:
            region += item
        try:
            jio_region = jio.recognize_location(region)
            if jio_region['foreign'] is not None and jio_region['foreign'][0][0]["country"] != "中国":
                return 'foreign', SpaceStandardStatus.foreign  # 中国大陆境外数据直接丢弃
            region = ''
            if len(labelData['GPE']) >= 1:
                # print(jio_region['domestic'])
                for key in ['province', 'city', 'county']:
                    if key in jio_region['domestic'][0][0].keys():
                        current_word = jio_region['domestic'][0][0][key]
                        if current_word is not None:
                            region += current_word
        except Exception as e:
            print(e)
        if len(labelData['FAC']) == 1 and flag == 1:
            LOC = region + labelData['FAC'][0]
            return LOC, SpaceStandardStatus.accurate
        for item in labelData['FAC']:
            locSet.append(jio.parse_location(region + item, change2new=True, town_village=True))
        if len(rawData['region']) > 0:
            LOC = rawData['region'] + labelData['FAC']
            locSet.append(jio.parse_location(LOC, change2new=True, town_village=True))
        locSet, status = create_full_space(locSet)
        if not locSet:
            return locSet, SpaceStandardStatus.nodata  # 无数据的
        else:
            # if SPACEstatus != []:
            #     return locSet, SPACEstatus
            return locSet, SpaceStandardStatus.accurate

