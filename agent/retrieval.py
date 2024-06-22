# -*- coding: utf-8 -*-
"""
@file    : retrieval.py
@date    : 2024-06-16
@author  : leafw

"""

from db import es
from api import embedding, reranker


def retrieve(query: str, document: str, top_n=10):
    # 向量检索
    vec = embedding.embedding(query)
    kg = es.search_by_vector(vec, document, top_n=top_n)
    hits = kg['hits']['hits']

    # keywords = deepseek.extract_keywords(query)
    # kg_by_kw = es.search_by_root_and_keywords(document, keywords)['hits']['hits']

    # 全文检索
    # kg_text = es.search_by_content(query, document, top_n)
    # hits_text = kg_text['hits']['hits']

    # 找到对应的上下文
    combines = hits_wrapper(hits)
    # combines_text = hits_wrapper(kg_by_kw)
    # combines.extend(combines_text)

    # 合并重复段落
    distinct_results = merge_combinations(combines)
    distinct_contents = ["\n".join(item['content'] for item in sublist) for sublist in distinct_results]
    sorted_contents = reranker.sort(query, distinct_contents)
    # if len(sorted_contents) > 5:
    #     sorted_contents = sorted_contents[:5]
    return sorted_contents


def hits_wrapper(hits):
    """
    把上下文也带上
    :param hits:
    :return:
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



