# -*- coding: utf-8 -*-
"""
@file    : controller.py
@date    : 2024-05-26
@author  : leafw
整体流程的控制器
"""
import generator
import doc_finder


def answer(question: str) -> str:
    # 1. 找到对应的段落内容
    finder = doc_finder.DocFinder('')
    finder.finder()
    content = ''

    # 2. 将段落内容送到glm进行回答
    return generator.answer(content, question)