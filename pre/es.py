# -*- coding: utf-8 -*-
"""
@file    : es.py
@date    : 2024-05-27
@author  : leafw
"""

from .pojo import DataModel
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from api import embedding
import time

# es = Elasticsearch([{'host': '192.168.0.103', 'port': 9200}])
es = Elasticsearch("http://192.168.0.103:9200")

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


def vectorize_all():
    count_result = es.count(index=index_name)
    print("Document count in index '{}': {}".format(index_name, count_result['count']))
    # 初始化scroll API
    page = es.search(
        index=index_name,
        scroll='2m',  # 维持游标查询窗口的时间
        body={
            "size": 1000,  # 每批检索的文档数量
            "query": {
                "match_all": {}
            }
        }
    )

    # 滚动处理所有数据
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']['value']

    a = 1
    while scroll_size > 0:
        for hit in page['hits']['hits']:
            # 检查vector字段是否为空
            if 'vector' not in hit['_source'] or not hit['_source']['vector']:
                print(f"处理第{a}条数据")
                vector = embedding.embedding(hit['_source']['content'])
                # 更新vector字段
                es.update(
                    index=index_name,
                    id=hit['_id'],
                    body={
                        "doc": {
                            "vector": vector
                        }
                    }
                )

        # 获取下一批数据
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        a += 1

    # 清理scroll上下文
    es.clear_scroll(scroll_id=sid)


def search_by_vector(query_vector,root_value, top_n=3):
    query = {
        "size": top_n,
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "root.keyword": root_value
                        }
                    },
                    {
                        "script_score": {
                            "query": {
                                "match_all": {}
                            },
                            "script": {
                                "source": "(cosineSimilarity(params.query_vector, 'vector') + 1.0) / 2",
                                "params": {
                                    "query_vector": query_vector
                                }
                            }
                        }
                    }
                ]
            }
        }
    }

    response = es.search(index=index_name, body=query)
    return response


# question = 'PCF与NRF对接时，一般需要配置哪些数据？'
# query_vector = embedding.embedding(question)
# r = search_by_vector(query_vector)
# print(r)