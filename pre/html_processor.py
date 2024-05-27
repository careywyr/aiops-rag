# -*- coding: utf-8 -*-
"""
@file    : html_processor.py
@date    : 2024-05-27
@author  : leafw
"""
import xml.etree.ElementTree as ET


class DataModel:
    def __init__(self, content: str, doctype: str, catalogs: [str], keywords: [str], vector: [float]):
        # 文本内容
        self.content = content
        # 文档类型
        self.doctype = doctype
        # 目录，从上至下
        self.catalogs = catalogs
        # 关键词，目录也作为关键词存在
        self.keywords = keywords
        # 向量
        self.vector = vector


def parse_node(node, catalogs):
    if len(node) == 0:
        url = node.attrib.get('url')
        doctype = node.attrib.get('doctype')
        item = DataModel(content=url, doctype=doctype, catalogs=catalogs, keywords=catalogs, vector=[])
        return [item]
    else:
        results = []
        for child in node:
            results.extend(parse_node(child, catalogs + [child.attrib.get('name')]))
        return results


def parse_xml(nodetree_xml_path):
    tree = ET.parse(nodetree_xml_path)
    root = tree.getroot()
    data = []
    for node in root:
        data.extend(parse_node(node, [node.attrib.get('name')]))
    return data



file_path = '/Users/carey/Documents/workspace2024/aiops-rag/data/nodetree.xml'
data_models = parse_xml(file_path)

for data_model in data_models:
    print(f'Content: {data_model.content}, Doctype: {data_model.doctype}, Catalogs: {data_model.catalogs}')