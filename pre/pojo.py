# -*- coding: utf-8 -*-
"""
@file    : pojo.py
@date    : 2024-06-02
@author  : leafw
"""


class DataModel:
    def __init__(self, name: str, content: str, url: str, doctype: str, catalogs: [str], keywords: [str],
                 vector: [float]):
        # 文档名称（不是文件名称）
        self.name = name
        # 文本内容
        self.content = content
        self.url = url
        # 文档类型
        self.doctype = doctype
        # 目录，从上至下
        self.catalogs = catalogs
        # 关键词，目录也作为关键词存在
        self.keywords = keywords
        # 向量
        self.vector = vector
