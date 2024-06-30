# -*- coding: utf-8 -*-
"""
@file    : kg.py
@date    : 2024-06-13
@author  : leafw
"""

from agent import generator, retrieval, query_opt
import jsonlines


questions = './dataset/question.jsonl'
outputs = './dataset/0629/2.jsonl'


def run(query, document):
    contents = retrieval.retrieve(query, document)
    background = "\n====================\n".join(contents)
    answer = generator.answer(background, query)
    print(answer)
    return answer, background


def run_all(input_file, output_file):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        count = 1
        for obj in reader:
            print(f"开始处理第{obj['id']}个问题")
            query = obj['query']
            document = obj['document']
            answer, background = run(query, document)
            result = {
                "id": obj['id'],
                "query": query,
                "document": document,
                "answer": answer
            }
            writer.write(result)
            count += 1


run_all(questions, outputs)
# answer, background = run('PCF与NRF对接时，一般需要配置哪些数据？', 'rcp')
# print(answer)
# print('\n--------------------------------------------------------------------------------\n')
# print(background)
