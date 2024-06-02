# -*- coding: utf-8 -*-
"""
@file    : html_processor.py
@date    : 2024-05-27
@author  : leafw
"""
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import html2text
import es
from pojo import DataModel


def parse_node(node, catalogs):
    """
    这个方法只读最后的叶子节点，考虑ES里面只需要叶子节点的数据即可
    :param node:
    :param catalogs:
    :return:
    """
    name = node.attrib.get('name')
    url = node.attrib.get('url')
    url = url.replace('\\', '/')
    doctype = node.attrib.get('doctype')
    if len(node) == 0:
        item = DataModel(name=name, content='', url=url, doctype=doctype, catalogs=catalogs, keywords=catalogs, vector=[])
        return [item]
    else:
        results = []
        for child in node:
            results.extend(parse_node(child, catalogs + [child.attrib.get('name')]))
        return results


def parse_xml(nodetree_xml_path):
    tree = ET.parse(nodetree_xml_path)
    root = tree.getroot()
    data = []
    for node in root:
        data.extend(parse_node(node, [node.attrib.get('name')]))
    return data


def html_to_markdown(html_content):
    # 创建一个HTML2Text对象
    h = html2text.HTML2Text()

    # 不保留超链接
    h.ignore_links = True

    # 将HTML转换为Markdown
    markdown = h.handle(html_content)
    return markdown


def read_file(root_path):
    data_models = parse_xml(root_path + '/nodetree.xml')

    for data_model in data_models:
        print(f'name: {data_model.name}, url: {data_model.url}, Doctype: {data_model.doctype}, Catalogs: {data_model.catalogs}')
        # 按照url去读取文件
        dst_url = root_path + '/documents/' + data_model.url
        with open(dst_url, 'r') as f:
            html_content = f.read()
        # 解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        body = soup.find('body')
        body = html_to_markdown(str(body))
        data_model.content = body
        es.store_to_elasticsearch([data_model])
        break


file_path = '/Users/carey/Documents/workspace2024/aiops2024-challenge-dataset/zedxzip/director'
read_file(file_path)
