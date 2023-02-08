# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/nlputils.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 7/2/2023 下午3:01

"""
    - JacCardSimilarity by downdawn (https://github.com/downdawn/Similarity)
    - SimHashSimilarity by downdawn (https://github.com/downdawn/Similarity)
"""
import datetime
# 正则
import re
# html 包
import html
# 数学包
import math
# 自然语言处理包
import jieba
import jieba.analyse

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline, AutoModelForSeq2SeqLM
import requests
import spacy


class JacCardSimilarity(object):
    """
    jaccard相似度
    """

    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words('./files/stopwords.txt')

        # 分词与关键词提取
        keywords_x = self.extract_keyword(self.s1)
        keywords_y = self.extract_keyword(self.s2)

        # jaccard相似度计算
        intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
        union = len(list(set(keywords_x).union(set(keywords_y))))
        # 除零处理
        sim = float(intersection) / union if union != 0 else 0
        return sim


class SimHashSimilarity(object):
    """
    SimHash
    """

    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def get_bin_str(source):  # 字符串转二进制
        if source == "":
            return 0
        else:
            t = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                t = ((t * m) ^ ord(c)) & mask
            t ^= len(source)
            if t == -1:
                t = -2
            t = bin(t).replace('0b', '').zfill(64)[-64:]
            return str(t)

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=True)
        return keywords

    def run(self, keywords):
        ret = []
        for keyword, weight in keywords:
            bin_str = self.get_bin_str(keyword)
            key_list = []
            for c in bin_str:
                weight = math.ceil(weight)
                if c == "1":
                    key_list.append(int(weight))
                else:
                    key_list.append(-int(weight))
            ret.append(key_list)
        # 对列表进行"降维"
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words('./files/stopwords.txt')

        # 提取关键词
        s1 = self.extract_keyword(self.s1)
        s2 = self.extract_keyword(self.s2)

        sim_hash1 = self.run(s1)
        sim_hash2 = self.run(s2)
        # print(f'相似哈希指纹1: {sim_hash1}\n相似哈希指纹2: {sim_hash2}')
        length = 0
        for index, char in enumerate(sim_hash1):
            if char == sim_hash2[index]:
                continue
            else:
                length += 1
        return length


def SpacySimilarity(text1: str, text2: str):
    nlp = spacy.load('zh_core_web_md')
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def relevant(text: str):
    tokenizer = AutoTokenizer.from_pretrained("AI/dimbat_disaster_distilbert")
    model = TFAutoModelForSequenceClassification.from_pretrained("AI/dimbat_disaster_distilbert")
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(text)
    print(result)
    if result[0]['label'] == 'LABEL_0':
        return 1 - result[0]['score']
    else:
        return result[0]['score']


def translate_zh_en(text: str):
    tokenizer = AutoTokenizer.from_pretrained("AI/opus-mt-zh-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("AI/opus-mt-zh-en")
    zh2en = pipeline("translation_zh_to_en", model=model, tokenizer=tokenizer)
    result = zh2en(text)
    print(result)
    return result[0]['translation_text']


