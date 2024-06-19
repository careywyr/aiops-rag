# -*- coding: utf-8 -*-
"""
@file    : kg.py
@date    : 2024-06-13
@author  : leafw
"""

from agent import generator, retrieval
import jsonlines


questions = './dataset/question.jsonl'
outputs = './dataset/0617002.jsonl'


def run(query, document):
    contents = retrieval.retrieve(query, document)
    real_related_contents = []
    for content in contents:
        # relation = generator.check_relation(content, query)
        # if relation == '否':
        #     continue
        real_related_contents.append(content)
    background = "\n====================\n".join(real_related_contents)
    answer = generator.answer(background, query)
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


# process_jsonl(questions, outputs)
a,b=run('N7会话的ResourceURI由哪个网元在哪个消息中生成', 'rcp')
print(a)
print(b)
