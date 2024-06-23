# -*- coding: utf-8 -*-
"""
@file    : kg.py
@date    : 2024-05-26
@author  : leafw
"""
from pre.pojo import GraphExtract
from py2neo import Graph, Node, Relationship


# 连接到Neo4j数据库
graph = Graph("bolt://192.168.0.103:7687", auth=("neo4j", "password"))


# 存储GraphExtract对象到Neo4j中
def store_graph_extract(graph_extract: GraphExtract):
    # 创建或获取head节点
    head_node = graph.nodes.match(graph_extract.head_type, name=graph_extract.head).first()
    if not head_node:
        head_node = Node(graph_extract.head_type, name=graph_extract.head)
        graph.create(head_node)

    # 创建或获取tail节点
    tail_node = graph.nodes.match(graph_extract.tail_type, name=graph_extract.tail).first()
    if not tail_node:
        tail_node = Node(graph_extract.tail_type, name=graph_extract.tail)
        graph.create(tail_node)

    # 创建关系
    relationship = Relationship(head_node, graph_extract.relation, tail_node)
    graph.create(relationship)


def store_graph_extracts(graph_extracts):
    for graph_extract in graph_extracts:
        store_graph_extract(graph_extract)
