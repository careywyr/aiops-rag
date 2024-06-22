# -*- coding: utf-8 -*-
"""
@file    : node_util.py
@date    : 2024-05-26
@author  : leafw
"""
import xml.etree.ElementTree as ET
from collections import deque
import json


class Node:
    def __init__(self, name, node_id, doctype, url):
        self.name = name
        self.id = node_id
        self.doctype = doctype
        self.url = url
        self.children = []

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "doctype": self.doctype,
            "url": self.url,
            "children": [child.to_dict() for child in self.children]
        }

    def to_simple_dict(self):
        return {
            "name": self.name,
            "children": [child.to_simple_dict() for child in self.children]
        }

    def to_simple_json(self):
        return json.dumps(self.to_simple_dict(), ensure_ascii=False)

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data):
        node = cls(data["name"], data["id"], data["doctype"], data["url"])
        for child_data in data["children"]:
            child_node = cls.from_dict(child_data)
            node.add_child(child_node)
        return node

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"Node(name={self.name}, id={self.id}, children={self.children})"


def parse_node(element):
    node_id = element.get('id')
    name = element.get('name')
    doctype = element.get('doctype')
    url = element.get('url')

    node = Node(name, node_id, doctype, url)

    for child in element.findall('node'):
        child_node = parse_node(child)
        node.add_child(child_node)

    return node


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    nodes = []
    for element in root.findall('node'):
        node = parse_node(element)
        nodes.append(node)

    return nodes


def display_tree(node, level=0):
    print("  " * level + f"Node(name={node.name}, id={node.id})")
    for child in node.children:
        display_tree(child, level + 1)


# if __name__ == "__main__":
#     nodes = parse_xml("D:\\Workspace\\aiops2024-challenge-dataset\\director\\nodetree.xml")
#     for node in nodes:
#         display_tree(node)
#         print(node.name, node.id, node.doctype, node.url)
