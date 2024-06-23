# -*- coding: utf-8 -*-
"""
@file    : pojo.py
@date    : 2024-06-02
@author  : leafw
"""
import json


class DataModel:
    def __init__(self, root: str, name: str, content: str, url: str, doctype: str, catalogs: [str], keywords: [str],
                 vector: [float], titles: [str] = [], parent: str = '', seg_index: int = 0):
        # 根目录名称rcp/director/emsplus/umac
        self.root = root
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
        # 标题，从1级到2级
        self.titles = titles
        # 父标题
        self.parent = parent
        # 在这个标题下的段落序号
        self.seg_index = seg_index


class GraphExtract:
    def __init__(self, head: str, head_type: str, relation: str, tail: str, tail_type: str):
        self.head = head
        self.head_type = head_type
        self.relation = relation
        self.tail = tail
        self.tail_type = tail_type

    def to_json(self):
        return json.dumps({
            "head": self.head,
            "head_type": self.head_type,
            "relation": self.relation,
            "tail": self.tail,
            "tail_type": self.tail_type
        }, ensure_ascii=False)

    def to_dict(self):
        return {
            "head": self.head,
            "head_type": self.head_type,
            "relation": self.relation,
            "tail": self.tail,
            "tail_type": self.tail_type
        }


