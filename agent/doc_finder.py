# -*- coding: utf-8 -*-
"""
@file    : doc_finder.py
@date    : 2024-05-26
@author  : leafw

寻找最有可能存在答案的文档

思路是通过文档树来找，因为是树状结构，因此实际上最终的文件在叶子节点上，但不能忽略路径上的文件或文件夹名称
log.html可以先忽略，里面是缩略词的词典，后面再想想怎么用
四个分类的nodetree可能很大，一次性塞不进去，那么可以一层层的问
"""
from utils import node_util, prompt_template
from api import deepseek, glm


def answer_node(node: node_util.Node, question: str, docs: [str]):
    # 为了避免内容太长了，只保留name和children
    node_json = node.to_simple_dict()
    prompt = prompt_template.find_doc(node_json, question)
    if len(prompt) > 3000:
        for child in node.children:
            answer_node(child, question, docs)
    else:
        doc = glm.chat(prompt)
        print(doc)
        if doc != '无关':
            docs.append(doc)


class DocFinder:
    def __init__(self, root_path: str):
        # 根目录，那么nodetree.xml直接就在这个目录下
        self.root_path = root_path

    def finder(self, question: str):
        answer_docs = []
        nodes = node_util.parse_xml(self.root_path + '/nodetree.xml')
        for node in nodes:
            # 先忽略log.html
            if node.name == '缩略语':
                continue
            answer_node(node, question, answer_docs)
        return answer_docs


# if __name__ == '__main__':
#     doc_finder = DocFinder('D:\\Workspace\\aiops2024-challenge-dataset\\director')
#     docs = doc_finder.finder('Director接收南向告警的snmp端口号是多少?')
#     print(docs)
