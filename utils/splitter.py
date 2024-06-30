# -*- coding: utf-8 -*-
"""
@file    : splitter.py
@date    : 2024-06-09
@author  : leafw
"""
import re
from langchain.text_splitter import MarkdownHeaderTextSplitter


def split_markdown(text, max_length=512):
    """
    根据标题拆分
    :param max_length: max_length
    :param text: text
    :return: contents[ {page_content: 'xxx', metadata:{'h1': '工作流应用开发指南', 'h2': '1 工作流应用创建'}} ]
    """
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on)
    contents = markdown_splitter.split_text(text)
    results = []
    # 针对切分后的每个段落做额外处理
    for content in contents:
        paragraphs = paragraph_split(content.page_content, max_length)
        h1 = content.metadata.get('Header 1')
        h2 = content.metadata.get('Header 2')
        a = ('# ' + h1 + '\n') if h1 is not None else ''
        b = ('## ' + h2 + '\n') if h2 is not None else ''
        for paragraph in paragraphs:
            paragraph = a + b + paragraph
            item = {'content': paragraph, 'h1': h1, 'h2': h2}
            results.append(item)
    return results


def paragraph_split(page_content, max_length=512):
    """
    段落处理
    :param page_content: 段落
    :param max_length: 段落最大值
    :return:
    """
    # 如果内容长度小于512，直接返回
    if len(page_content) <= max_length:
        return [page_content]

    # 查找所有表格
    table_pattern = re.compile(r'(\|.*\|(?:\n\|.*\|)+)')
    tables = table_pattern.findall(page_content)

    # 替换表格为占位符
    placeholder = "<TABLE_PLACEHOLDER>"
    content_without_tables = table_pattern.sub(placeholder, page_content)

    # 按长度拆分段落
    paragraphs = []
    current_paragraph = ""
    for line in content_without_tables.splitlines(keepends=True):
        if len(current_paragraph) + len(line) > max_length:
            paragraphs.append(current_paragraph)
            current_paragraph = ""
        current_paragraph += line
    if current_paragraph:
        paragraphs.append(current_paragraph)

    # 恢复表格占位符
    result_paragraphs = []
    table_index = 0
    for paragraph in paragraphs:
        if placeholder in paragraph:
            table = tables[table_index]
            table_index += 1
            # 如果表格大于max_length，拆分表格
            if len(table) > max_length:
                split_tables = split_large_table(table, max_length)
                result_paragraphs.extend(split_tables)
            else:
                result_paragraphs.append(paragraph.replace(placeholder, table))
        else:
            result_paragraphs.append(paragraph)

    return result_paragraphs


def split_large_table(table, max_length):
    # 拆分大的表格为多个小表格
    lines = table.splitlines()
    header = lines[0]
    split_tables = []
    current_table = header + "\n"

    for line in lines[1:]:
        if len(current_table) + len(line) + 1 > max_length:
            split_tables.append(current_table.strip())
            current_table = header + "\n"
        current_table += line + "\n"

    if current_table.strip():
        split_tables.append(current_table.strip())

    return split_tables


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
