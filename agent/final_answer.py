# -*- coding: utf-8 -*-
"""
@file    : final_answer.py
@date    : 2024-05-26
@author  : leafw
最终用来回答
"""

from api import glm
from utils import prompt_template


def answer(content: str, question: str) -> str:
    prompt = prompt_template.find_question(content, question)
    return glm.chat(prompt)

