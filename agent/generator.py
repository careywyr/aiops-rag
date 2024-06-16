# -*- coding: utf-8 -*-
"""
@file    : generator.py
@date    : 2024-05-26
@author  : leafw
最终用来回答
"""

from api import glm
from utils import prompt_template


def answer(content: str, question: str) -> str:
    prompt = prompt_template.find_question(content, question)
    return glm.chat(prompt)


def check_relation(content: str, question: str) -> str:
    prompt = prompt_template.check_relationship(question, content)
    return glm.chat(prompt)
