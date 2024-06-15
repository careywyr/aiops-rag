# -*- coding: utf-8 -*-
"""
@file    : kg.py
@date    : 2024-06-13
@author  : leafw
"""
from pre import es
from api import embedding
from agent import final_answer
import jsonlines


questions = './dataset/question.jsonl'
outputs = './dataset/second.jsonl'


def run(query, document):
    vec = embedding.embedding(query)
    kg = es.search_by_vector(vec, document)
    contents = [hit['_source']['content'] for hit in kg['hits']['hits']]
    background = "\n\n".join(contents)
    answer = final_answer.answer(background, query)
    print(answer)
    return answer, background


def process_jsonl(input_file, output_file):
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


process_jsonl(questions, outputs)
