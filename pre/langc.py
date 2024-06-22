# -*- coding: utf-8 -*-
"""
@file    : langc.py
@date    : 2024-06-19
@author  : leafw
使用langchain进行整套的开发试试
"""

from pre import html_processor
import utils.splitter as splitter
import copy
import getpass
import os

from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

embeddings = OpenAIEmbeddings()

vectorstore = ElasticsearchStore.from_documents(
    index_name="elasticsearch-self-query-demo",
    es_url="http://localhost:9200",
)

def process_files(root_path, root_name):
    data_models = html_processor.parse_xml(root_path + '/nodetree.xml', root_name)
    print(f'要处理的文件数量: {len(data_models)}')
    loop = 1
    for data_model in data_models:
        print(
            f'loop: {loop}, root: {data_model.root}, name: {data_model.name}, url: {data_model.url}, Doctype: {data_model.doctype}, Catalogs: {data_model.catalogs}')
        # 按照url去读取文件
        dst_url = root_path + '/documents/' + data_model.url

        content = html_processor.html_to_markdown(dst_url)
        docs = splitter.split_markdown(content)

        seg_index = 0
        for doc in docs:
            save_data = copy.deepcopy(data_model)
            save_data.content = doc.get('content')
            save_data.titles = [doc.get('h1'), doc.get('h2')]
            save_data.parent = doc.get('h2') if doc.get('h2') else doc.get('h1')
            save_data.seg_index = seg_index
            seg_index += 1
        loop += 1