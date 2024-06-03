# -*- coding: utf-8 -*-
"""
@file    : es.py
@date    : 2024-05-27
@author  : leafw
"""

from elasticsearch import Elasticsearch
from pojo import DataModel

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

index_name = 'aiops'


def store(data_models: [DataModel]):
    for data_model in data_models:
        print(f"save model, name: {data_model.name}")
        doc = {
            'name': data_model.name,
            'content': data_model.content,
            'url': data_model.url,
            'doctype': data_model.doctype,
            'catalogs': data_model.catalogs,
            'keywords': data_model.keywords,
            'vector': data_model.vector
        }
        es.index(index=index_name, body=doc)
        print(f"save success, name: {data_model.name}")


def search_by_content(query: str):
    body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_by_name(query: str):
    body = {
        "query": {
            "wildcard": {
                "name": f"*{query}*"
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']

