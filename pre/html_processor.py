# -*- coding: utf-8 -*-
"""
@file    : html_processor.py
@date    : 2024-05-27
@author  : leafw
"""
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import html2text
from pojo import DataModel
# import es
import copy
from utils.splitter import CustomMarkdownSplitter
import utils.splitter as splitter
from pprint import pprint
import consts


def parse_node(node, catalogs, root_name):
    """
    这个方法只读最后的叶子节点，考虑ES里面只需要叶子节点的数据即可
    :param root_name: 根目录名称
    :param node: 节点
    :param catalogs: 目录
    :return:
    """
    name = node.attrib.get('name')
    url = node.attrib.get('url')
    url = url.replace('\\', '/')
    doctype = node.attrib.get('doctype')
    if len(node) == 0:
        item = DataModel(root=root_name, name=name, content='', url=url, doctype=doctype, catalogs=catalogs,
                         keywords=catalogs,
                         vector=[])
        return [item]
    else:
        results = []
        for child in node:
            results.extend(parse_node(child, catalogs + [child.attrib.get('name')], root_name))
        return results


def parse_xml(nodetree_xml_path, root_name):
    tree = ET.parse(nodetree_xml_path)
    root = tree.getroot()
    data = []
    for node in root:
        data.extend(parse_node(node, [node.attrib.get('name')], root_name))
    return data


def html_to_markdown(dst_url):
    try:
        with open(dst_url, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        with open(dst_url, 'r', encoding='gb2312') as f:
            html_content = f.read()
    # 解析HTML内容
    soup_root = BeautifulSoup(html_content, 'html.parser')

    body = soup_root.find('body')

    soup = BeautifulSoup(str(body), 'html.parser')

    # 根据class属性修改HTML结构
    for element in soup.find_all(class_=["title", "topictitle"]):
        if "topictitle" in element.get("class", []):
            element.name = "h1"  # 将class为title的标签转换为<h1>
        elif "title" in element.get("class", []):
            element.name = "h2"  # 将class为topictitle的标签转换为<h1>

    # 处理表格部分
    markdown_tables = {}
    table_id = 0
    for table in soup.find_all('table'):
        markdown_table = convert_table_to_markdown(table)
        placeholder = f"[[TABLE_{table_id}]]"
        markdown_tables[placeholder] = markdown_table
        table.replace_with(soup.new_string(placeholder))
        table_id += 1

    # 使用html2text处理剩余的HTML内容
    h = html2text.HTML2Text()
    h.ignore_links = True
    markdown = h.handle(str(soup))

    # 替换占位符为转换后的Markdown表格
    for placeholder, markdown_table in markdown_tables.items():
        markdown = markdown.replace(placeholder, markdown_table)

    # 移除多余的空行
    markdown = '\n'.join([line for line in markdown.split('\n') if line.strip() != ''])

    return markdown


def convert_table_to_markdown(table):
    rows = table.find_all('tr')
    markdown = []

    for row in rows:
        cols = row.find_all(['th', 'td'])
        col_text = [col.get_text(strip=True) for col in cols]
        markdown.append('| ' + ' | '.join(col_text) + ' |')

    # 添加表头分隔符
    if len(rows) > 1:
        header_cols = rows[0].find_all(['th', 'td'])
        header_separator = '| ' + ' | '.join(['---'] * len(header_cols)) + ' |'
        markdown.insert(1, header_separator)

    # 将表格内容用换行符连接起来
    return '\n'.join(markdown) + '\n\n'  # 添加两个换行符


def read_file(root_path, root_name):
    data_models = parse_xml(root_path + '/nodetree.xml', root_name)
    print(f'要处理的文件数量: {len(data_models)}')
    loop = 1
    for data_model in data_models:
        print(
            f'loop: {loop}, root: {data_model.root}, name: {data_model.name}, url: {data_model.url}, Doctype: {data_model.doctype}, Catalogs: {data_model.catalogs}')
        # 按照url去读取文件
        dst_url = root_path + '/documents/' + data_model.url

        content = html_to_markdown(dst_url)
        docs = splitter.split_markdown(content)

        seg_index = 0
        for doc in docs:
            save_data = copy.deepcopy(data_model)
            save_data.content = doc.get('content')
            save_data.titles = [doc.get('h1'), doc.get('h2')]
            save_data.parent = doc.get('h2') if doc.get('h2') else doc.get('h1')
            save_data.seg_index = seg_index
            seg_index += 1
            # es.store([save_data])
        loop += 1


def run():
    # read_file(consts.HTML_ROOT_EMSPLUS[0], consts.HTML_ROOT_EMSPLUS[1])
    # print('============ emsplus end ============')

    # read_file(consts.HTML_ROOT_DIRECTOR[0], consts.HTML_ROOT_DIRECTOR[1])
    # print('============ director end ============')

    # 这里面有表格一行数据就超过512了，把chunk_size调大一下
    # 8288 有问题，主要是因为splitter对于长表格处理问题，改进就行嘞
    read_file(consts.HTML_ROOT_RCP[0], consts.HTML_ROOT_RCP[1])
    print('============ rcp end ============')


    # read_file(consts.HTML_ROOT_UMAC[0], consts.HTML_ROOT_UMAC[1])
    # print('============ umac end ============')

run()