# -*- coding: utf-8 -*-
"""
@file    : es.py
@date    : 2024-05-27
@author  : leafw
"""

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])  # 替换为实际的Elasticsearch主机和端口

index_name = 'aiops'


def store_to_elasticsearch(data_models):
    for data_model in data_models:
        doc = {
            'content': data_model.content,
            'doctype': data_model.doctype,
            'catalogs': data_model.catalogs,
            'keywords': data_model.keywords,
            'vector': data_model.vector
        }
        es.index(index=index_name, body=doc)
