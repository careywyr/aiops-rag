# -*- coding: utf-8 -*-
"""
@file    : es.py
@date    : 2024-05-27
@author  : leafw
"""

from pre.pojo import DataModel
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from api import embedding, deepseek

# es = Elasticsearch([{'host': '192.168.0.103', 'port': 9200}])
es = Elasticsearch("http://192.168.0.103:9200")

# index_name = 'aiops'
# 改进html转Markdown的拆分策略后的库
index_name = 'aiops_v2'


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
            'vector': data_model.vector,
            'titles': data_model.titles,
            'parent': data_model.parent,
            'seg_index': data_model.seg_index
        }

        es.index(index=index_name, body=doc)


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
            # if 'vector' not in hit['_source'] or not hit['_source']['vector']:
            print(f"处理第{a}页数据")
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


def search_by_root_and_keywords(root, keywords):
    query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "root.keyword": root  # 使用keyword类型进行精确匹配
                    }
                }
            ],
            "filter": [
                {
                    "terms": {
                        "keywords.keyword": keywords  # 使用terms查询进行交集匹配
                    }
                }
            ]
        }
    }

    response = es.search(
        index=index_name,
        body={
            "query": query
        }
    )

    return response


def keywords_extract_all(root_value):
    count_result = es.count(index=index_name, body={"query": {"match": {"root": root_value}}})
    print("Document count in index '{}': {}".format(index_name, count_result['count']))

    page = es.search(
        index=index_name,
        scroll='20m',
        body={
            "size": 1000,
            "query": {
                "match": {
                    "root": root_value
                }
            }
        }
    )

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']['value']
    a = 1

    while scroll_size > 0:
        for hit in page['hits']['hits']:
            print(f"处理第{a}页数据")
            existing_keywords = hit['_source'].get('keywords', [])
            if len(existing_keywords) <= 3:
                new_keywords = deepseek.extract_keywords(hit['_source']['content'])
                all_keywords = list(set(existing_keywords + new_keywords))
                try:
                    es.update(
                        index=index_name,
                        id=hit['_id'],
                        body={
                            "doc": {
                                "keywords": all_keywords
                            }
                        }
                    )
                except NotFoundError:
                    print(f"ID为{hit['_id']}的数据不存在，无法更新。")

        page = es.scroll(scroll_id=sid, scroll='20m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        a += 1

    es.clear_scroll(scroll_id=sid)


def search_by_vector(query_vector, root_value, top_n=10):
    query = {
        "size": top_n,
        "query": {
            "bool": {
                "must": [
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
                ],
                "filter": [
                    {
                        "term": {
                            "root.keyword": root_value
                        }
                    }
                ]
            }
        }
    }

    response = es.search(index=index_name, body=query)
    return response


def search_by_content(query: str, root_value, top_n=10):
    body = {
        "size": top_n,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"content": query}
                    },
                    {
                        "term": {"root.keyword": root_value}
                    }
                ]
            }

        }
    }
    response = es.search(index=index_name, body=body)
    return response


def search_documents(url, seg_index):
    # 构建查询
    query = {
        "bool": {
            "must": [
                {"term": {"url.keyword": url}},
                {"term": {"seg_index": seg_index}}
            ]
        }
    }

    # 执行查询
    response = es.search(index=index_name, body={"query": query})

    # 返回查询结果
    return response


def search_by_json(query: str):
    # 执行查询
    response = es.search(index=index_name, body=query)
    print(response)
    # 返回查询结果
    return response


# # vectorize_all()
# keywords_extract_all('director')
# keywords_extract_all('rcp')

# r = search_by_content('N7会话的ResourceURI由哪个网元在哪个消息中生成', 'rcp')
# print(r)

# query = {
#     "query": {
#         "term": {"_id": 24890}
#     }
# }
# search_by_json(query)
