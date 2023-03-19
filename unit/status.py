#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @ Project: new_mist
# @ File: status
# @ Time: 7/3/2023 上午9:30
# @ Author: hz157
# @ Github: https://github.com/hz157

"""
    ner状态枚举
"""

from enum import Enum


class TimeStandardStatus(Enum):
    """
        时间标准化状态提示
    """
    unrecognized = 'Unrecognized nerTime'  # 未识别到标准化时间
    non_standardized = "Standardized time is not 'time_ Point 'or 'time_span' type"  # 标准化类型不为time_point 或是 time_span


class SpaceStandardStatus(Enum):
    accurate = 'accurate accuracy'
    near_precision = 'Near-precision accuracy'
    common = 'common accuracy'
    nodata = 'NoDATA'   # 无数据
    foreign = 'foreign'  # 国外地址
    miss_gpe = '2-Missing GPE data'  # 丢失GPE信息
    invalid = '2-Invalid completion'  # 无效信息
    miss_country = '3-missing country data'  # 丢失国家信息
    miss_city = '3-missing city data'  # 丢失城市信息
    miss_province = '3-missing province data'  # 丢失省份信息
