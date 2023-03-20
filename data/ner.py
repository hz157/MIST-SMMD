# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: mist
# @FileName: ner
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 3/3/2023 上午10:31

import jionlp as jio
import spacy

from api.baidu import place_v2_search
from config import config
from data.standardizing import time_standardization, spacy_standization
from unit.coordinate import bd09_to_wgs84

spacy.require_gpu()  # 使用GPU请取消该行注释
NER = spacy.load("zh_core_web_trf",
                 exclude=["tagger", "parser", "entity_linker", "entity_ruler", "textcat", "textcat_multilabel",
                          "lemmatizer", "trainable_lemmatizer", "morphologizer", "attribute_ruler", "senter",
                          "sentencizer", "tok2vec"])  # 排除部分无关标签，提升效率


def sentence_split(text, cri):
    """
        文本分句， 采用jionlp.split_sentence
        https://github.com/dongrixinyu/JioNLP/wiki/Gadget-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3#user-content-%E6%96%87%E6%9C%AC%E5%88%86%E5%8F%A5
    Args:
        text: 文本列表
        cri: 粒度 分为 coarse粗粒度 和 fine细粒度

    Returns: 文本结果 list

    """
    sentenceList = []  # 分句列表
    try:
        sentenceList.append(jio.split_sentence(text, criterion=cri))  # jionlp 文本分句
        return sentenceList
    except Exception as e:
        print(e)
        return None


def spacy_label_mark(sentence):
    """
        获取时空信息
        使用spacy， 包: zh_core_web_trf, python -m spacy download zh_core_web_trf
    Args:
        sentence: 经过jionlp分句的列表 list

    Returns: 标签信息和数据 dict

    """
    if sentence is None:
        return
    result = {}
    for item in sentence:  # 遍历jionlp分句的列表
        NER.max_length = len(max(item, key=len))
        pipe = NER.pipe(item, batch_size=1024)
        for text in pipe:
            if len(text.ents) == 0 or text.ents == '……':
                continue
            for ent in text.ents:
                if ent.label_ in result.keys():  # 之前已写入该标签
                    value = result[ent.label_]  # 获取之前写入的数据
                    value.append(ent.text)  # 追加新的数据
                    result[ent.label_] = value  # 重新赋值
                else:  # 之前未写入该标签
                    result[ent.label_] = [ent.text]  # 赋值
    return result


def create_write_data(native_data, label_info):
    result = [[]] * 15
    check = [[]] * 15
    sentence = ''
    if 'FAC' in label_info.keys():  # 判断是否有空间信息，无则弃之
        if 'TIME' in label_info.keys() or 'DATE' in label_info.keys():  # 判断是否有时间信息，无则弃之
            sentence = []
            for item in native_data['sentence']:
                tmp = ''
                for i in item:
                    tmp = tmp + i
                sentence.append(tmp)
            result[0] = native_data['text']  # 原始文本
            result[1] = sentence  # jionlp 拆分的句子
            result[2] = native_data['create_at']  # 博文时间
            TIME = []
            if 'DATE' in label_info.keys():  # 判断是否有DATE标签
                TIME = label_info['DATE']
            if 'TIME' in label_info.keys():
                TIME = TIME + label_info['TIME']  # spacy 时间
            result[3] = TIME  # spacy 时间
            if 'GPE' in label_info.keys():
                result[4] = label_info['GPE']  # spacy 行政区
            else:
                result[4] = ''
            if label_info['FAC'] in config.FAC_REVERSE_KEYWORD:  # 设施反向关键字 修改config/config.py
                result[5] = ''  # 反向关键字排除，添加空数据
            else:
                result[5] = label_info['FAC']  # spacy 设施
            ner_time, ner_time_status = time_standardization(TIME,
                                                             native_data['create_at'])  # 获取标准化时间
            result[6] = ner_time  # 追加ner时间数据
            result[7] = ner_time_status  # 追加ner时间状态
            ner_spacy, ner_spacy_status = spacy_standization(label_info, native_data)
            result[8] = ner_spacy
            result[9] = ner_spacy_status
            # if ner_spacy is not None or ner_spacy != []:
            #     baidu = place_v2_search(ner_spacy[0])  # 请求百度位置
            #     if baidu is not None:
            #         wgs84 = bd09_to_wgs84(baidu['bd-09']['lng'], baidu['bd-09']['lat'])
            #         baidu['wgs-84'] = {'lng': wgs84[0], 'lat': wgs84[1]}
            #         result[10] = baidu['bd-09']['lng']  # bd-09 坐标
            #         result[11] = baidu['bd-09']['lat']  # bd-09 坐标
            #         result[12] = baidu['wgs-84']['lng']  # wgs-84 坐标
            #         result[13] = baidu['wgs-84']['lng']  # wgs-84 坐标
            #         result[14] = baidu['street_id']  # 街景地图id
            result[10] = 0
            result[11] = 0
            result[12] = 0
            result[13] = 0
            result[14] = 0
        else:
            return 'No nerTIME'
    if check == result:
        return None
    return result

