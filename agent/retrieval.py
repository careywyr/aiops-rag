# -*- coding: utf-8 -*-
"""
@file    : retrieval.py
@date    : 2024-06-16
@author  : leafw

"""

from db import es
from api import embedding, reranker, glm
from agent import query_opt


def vector_search(query: str, document: str, top_n=10) -> [str]:
    """
    纯向量检索
    :param query:
    :param document:
    :param top_n:
    :return:
    """
    vec = embedding.embedding(query)
    kg = es.search_by_vector(vec, document, top_n=top_n)
    hits = kg['hits']['hits']
    # 找到对应的上下文
    combines = hits_wrapper(hits)
    # 合并重复段落
    distinct_results = merge_combinations(combines)
    distinct_contents = ["\n".join(item['content'] for item in sublist) for sublist in distinct_results]
    return distinct_contents


def keywords_search(keywords: [str], document: str, top_n=5) -> [str]:
    """
    纯关键词检索-本质上是关键词直接搜索，不是关键词匹配
    :param keywords:
    :param document:
    :param top_n:
    :return:
    """
    results = set()
    for keyword in keywords:
        kg = es.search_by_content(keyword, document, top_n=top_n)
        hits = kg['hits']['hits']
        contents = [item['_source'].get('content') for item in hits]
        results.update(contents)
    return results


def rerank(query: str, contents: [str]):
    return reranker.sort(query, contents)


def retrieve_by_reflection(query: str, document: str, top_n=5):
    contents = vector_search(query, document, top_n)
    background = "\n====================\n".join(contents)
    relation = glm.check_relation(query, background)
    if relation == '是':
        return contents
    # 如果不能，再用其他方式召回
    retrieve(query, document, top_n)


def retrieve(query: str, document: str, top_n=5):
    """
    三种方式查询召回，显存不够试试拆开来排序
    :param query:
    :param document:
    :param top_n:
    :return:
    """
    # hyde搜索
    hyde_content = query_opt.hyde(query)
    hyde_resp = vector_search(hyde_content, document, top_n)
    hyde_resp_scores = reranker.sort_include_score(query, hyde_resp)

    # 子查询搜索
    multi_query = query_opt.multi_query(query)
    mult_query_resp = set()
    for q in multi_query:
        a = vector_search(q, document, top_n)
        mult_query_resp.update(a)

    mult_query_resp_scores = reranker.sort_include_score(query, mult_query_resp)

    # 关键词搜索
    keywords = query_opt.keywords_query(query)
    keywords_resp = set()
    for kw in keywords:
        a = keywords_search(kw, document, top_n)
        keywords_resp.update(a)

    keywords_resp_scores = reranker.sort_include_score(query, keywords_resp)

    all_result = set()
    all_result.update(hyde_resp_scores)
    all_result.update(mult_query_resp_scores)
    all_result.update(keywords_resp_scores)
    ranked = list(all_result)
    # 按照分数从大到小排序
    ranked.sort(key=lambda x: x[1], reverse=True)
    if len(ranked) > 10:
        ranked = ranked[:10]
    results = [item[0] for item in ranked]
    return results


def hits_wrapper(hits):
    """
    把上下文也带上
    :param hits:
    :return: 每个元素是一个数组，数组里包含了连续的段落
    """
    combines = []
    for hit in hits:
        _id = hit['_id']
        source = hit['_source']
        url = source['url']
        hit_content = source['content']
        seg_index = source['seg_index']
        current_hit = {'id': _id, 'content': hit_content}

        if seg_index == 0:
            query_index = [1]
        else:
            query_index = [seg_index - 1, seg_index + 1]

        context = []
        for index in query_index:
            results = es.search_documents(url, index)
            # 相邻结果
            if len(results['hits']['hits']) == 0:
                continue

            near_hit = results['hits']['hits'][0]
            near_id = near_hit['_id']
            near_content = near_hit['_source']['content']

            content = {'id': near_id, 'content': near_content}
            context.append(content)

        if len(context) > 0:
            if len(query_index) > 1:
                if len(context) == 1:
                    combine = [context[0], current_hit]
                else:
                    combine = [context[0], current_hit, context[1]]
            else:
                combine = [current_hit, context[0]]
            combines.append(combine)
        else:
            combines.append([current_hit])
    return combines


def merge_combinations(combines):
    def find_combination_with_id(combinations, target_id):
        for combination in combinations:
            if any(item['id'] == target_id for item in combination):
                return combination
        return None

    merged_combinations = []

    for combination in combines:
        for item in combination:
            existing_combination = find_combination_with_id(merged_combinations, item['id'])
            if existing_combination:
                # 合并当前组合中的元素到已存在的组合中
                existing_combination.extend(x for x in combination if x not in existing_combination)
                break
        else:
            # 如果没有找到包含当前id的组合，则添加新的组合
            merged_combinations.append(combination)

    return merged_combinations


def filter_contents(query: str, contents: [str]):
    filtered = []
    for content in contents:
        relation = glm.check_relation(query, content)
        if relation == '是':
            filtered.append(content)
    return filtered

# resp = retrieve('PCF与NRF对接时，一般需要配置哪些数据？', 'rcp')
# r2 = rerank('PCF与NRF对接时，一般需要配置哪些数据？', resp)
# print(r2)
