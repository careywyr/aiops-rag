# -*- coding: utf-8 -*-
"""
@file    : es.py
@date    : 2024-05-27
@author  : leafw
"""

from pojo import DataModel
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

index_name = 'aiops'


def store(data_models: [DataModel]):
    for data_model in data_models:
        print(f"save model, name: {data_model.name}")
        doc = {
            'root': data_model.root,
            'name': data_model.name,
            'content': data_model.content,
            'url': data_model.url,
            'doctype': data_model.doctype,
            'catalogs': data_model.catalogs,
            'keywords': data_model.keywords,
            'vector': data_model.vector
        }
        es.index(index=index_name, body=doc)


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


def delete_index():
    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(f"Index '{index_name}' has been deleted.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except NotFoundError:
        print(f"Index '{index_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
