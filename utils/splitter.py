# -*- coding: utf-8 -*-
"""
@file    : splitter.py
@date    : 2024-06-09
@author  : leafw
"""
import re


class CustomMarkdownSplitter:
    def __init__(self, text):
        self.text = text

    def split(self, tb_pre=0, tb_after=0, chunk_size=1000, chunk_overlap=0):
        # 正则表达式匹配Markdown表格
        table_pattern = re.compile(r'(\|.*?\|\n)+')

        # 使用split时保留分隔符
        split_text = re.split(r'(\n\n)', self.text)

        documents = []
        buffer = []
        long_tables = []

        # 提前提取长表格
        for i, segment in enumerate(split_text):
            # 判断是否为长表格
            if any(len(line) > 500 for line in segment.split('\n') if line.startswith('|')):
                long_tables.append(segment)
                split_text[i] = ''

        for i, segment in enumerate(split_text):
            if table_pattern.match(segment):
                # 获取前面tb_pre段
                start_index = max(0, i - 2 * tb_pre)
                # 获取后面tb_after段
                end_index = min(len(split_text), i + 2 * tb_after + 1)

                combined_segments = split_text[start_index:i] + [segment] + split_text[i + 1:end_index]
                document = ''.join(combined_segments).strip()
                self.add_document(documents, document, chunk_size, chunk_overlap)
            elif segment != '\n\n':
                buffer.append(segment)
            if segment == '\n\n' or i == len(split_text) - 1:
                if buffer:
                    self.add_document(documents, ''.join(buffer).strip(), chunk_size, chunk_overlap)
                    buffer = []

        # 单独处理长表格
        for table in long_tables:
            self.add_document(documents, table.strip(), chunk_size, chunk_overlap)

        return documents

    def add_document(self, documents, doc, chunk_size, chunk_overlap):
        while len(doc) > chunk_size:
            split_point = doc[:chunk_size].rfind('\n\n')
            if split_point == -1:
                split_point = chunk_size

            overlap_start = max(0, split_point - chunk_overlap)
            documents.append(doc[:split_point].strip())
            doc = doc[overlap_start:].strip()
        documents.append(doc)


# # 示例Markdown文本
# markdown_text = """
# # 标题
#
# 这是一个段落。
#
# absfewfrwefewf
# 这是另一个段落。
# """
#
# splitter = CustomMarkdownSplitter(markdown_text)
# documents = splitter.split(tb_pre=0, tb_after=0, chunk_size=50, chunk_overlap=2)
#
# for doc in documents:
#     print(doc)
#     print("=" * 20)
